from sqlalchemy.orm import Session
from models import Job
from datetime import datetime


def save_job_to_db(db: Session, job_data: dict, source: str):
    job_id = job_data.get("jobNo") or job_data.get("jobId")

    job = None
    if job_id:
        job = db.query(Job).filter(Job.jobNo == job_id).first()

    updated_at_str = job_data.get("updateAt")
    updated_at_timestamp = job_data.get(
        "interactionRecord", {}).get("lastProcessedResumeAtTime")
    updated_at = None
    if updated_at_str:
        try:
            updated_at = datetime.strptime(updated_at_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            pass
    if updated_at_timestamp:
        try:
            updated_at = datetime.fromtimestamp(updated_at_timestamp)
        except ValueError:
            pass

    if not job:
        job = Job(
            jobNo=job_id,
            title=job_data.get("jobName") or job_data.get("title"),
            description=job_data.get("description"),
            salary=job_data.get(
                "salary") or f"{job_data.get('salaryLow')}-{job_data.get('salaryHigh')}",
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

    return job
