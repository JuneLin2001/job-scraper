from sqlalchemy.orm import Session
from models import Job, Label
from datetime import datetime
from utils import extract_labels_from_description
from sqlalchemy.orm.attributes import flag_modified


def save_job_to_db(db: Session, job_data: dict, source: str):
    job_title = job_data.get("jobName") or job_data.get("title")
    company_name = job_data.get("custName") or job_data.get("companyName")
    if not (job_title and company_name):
        return None

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

    job_title_std = job_title.strip().lower()
    company_name_std = company_name.strip().lower()
    job = db.query(Job).filter(
        Job.title.ilike(job_title_std),
        Job.company_name.ilike(company_name_std)
    ).first()

    if not job:
        job = Job(
            jobNo=job_data.get("jobNo") or job_data.get("jobId"),
            title=job_title,
            description=description,
            salary=salary,
            company_name=company_name,
            location=job_data.get("jobAddrNoDesc") or job_data.get(
                "workCity", {}).get("name"),
            links=[f"https://www.1111.com.tw/job/{job_data.get('jobId')}"] if source == "1111" else [
                job_data.get("link", {}).get("job")],
            updated_at=updated_at,
            source=[source]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
    else:

        new_link = None
        if source == "1111" and job_data.get("jobId"):
            new_link = f"https://www.1111.com.tw/job/{job_data.get('jobId')}"
        elif source == "104" and job_data.get("link", {}).get("job"):
            new_link = job_data.get("link", {}).get("job")

        if source not in job.source:
            job.source.append(source)
            job.links.append(new_link)

        flag_modified(job, "source")
        flag_modified(job, "links")
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
