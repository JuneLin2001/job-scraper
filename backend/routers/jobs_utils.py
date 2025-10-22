from sqlalchemy.orm import Session
from models import Job, Label
from datetime import datetime
from utils import extract_labels_from_description


def save_job_to_db(db: Session, job_data: dict, source: str):
    job_id = job_data.get("jobNo") or job_data.get("jobId")
    if not job_id:
        return None

    job = db.query(Job).filter(Job.jobNo == job_id).first()

    updated_at_str = job_data.get("updateAt")
    updated_at_timestamp = job_data.get(
        "interactionRecord", {}).get("lastProcessedResumeAtTime")
    updated_at = None

    if updated_at_timestamp:
        try:
            updated_at = datetime.fromtimestamp(updated_at_timestamp)
        except (ValueError, OSError):
            pass
    elif updated_at_str:
        try:
            updated_at = datetime.strptime(updated_at_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            pass

    description = job_data.get("description", "")
    labels_list = extract_labels_from_description(description)

    salary_low = job_data.get("salaryLow")
    salary_high = job_data.get("salaryHigh")
    raw_salary = job_data.get("salary") or f"{salary_low}-{salary_high}"

    if raw_salary in ["0-0", "面議（經常性薪資達4萬元或以上）", ""]:
        salary = "面議"
    elif salary_high == 9999999:
        salary = f"{salary_low}+"
    else:
        salary = raw_salary

    if not job:
        job = Job(
            jobNo=job_id,
            title=job_data.get("jobName") or job_data.get("title"),
            description=description,
            salary=salary,
            company_name=job_data.get(
                "custName") or job_data.get("companyName"),
            location=job_data.get("jobAddrNoDesc") or job_data.get(
                "workCity", {}).get("name"),
            link=f"https://www.1111.com.tw/job/{job_id}" if source == "1111" else job_data.get(
                "link", {}).get("job"),
            updated_at=updated_at,
            source=source
        )
        db.add(job)
        db.commit()
        db.refresh(job)

    existing_labels = {label.name: label for label in db.query(
        Label).filter(Label.name.in_(labels_list)).all()}
    new_labels = [Label(name=name)
                  for name in labels_list if name not in existing_labels]

    if new_labels:
        db.add_all(new_labels)
        db.commit()
        for l in new_labels:
            db.refresh(l)

    for name in labels_list:
        label = existing_labels.get(name) or next(
            (l for l in new_labels if l.name == name), None)
        if label and label not in job.labels:
            job.labels.append(label)

    db.commit()
    db.refresh(job)
    return job
