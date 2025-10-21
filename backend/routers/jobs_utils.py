from sqlalchemy.orm import Session
from models import Job


def save_job_to_db(db: Session, job_data: dict, source: str):
    job_id = job_data.get("jobNo") or job_data.get("jobId")

    job = None
    if job_id:
        job = db.query(Job).filter(Job.jobNo == job_id).first()

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
            link=job_data.get("link", {}).get("job") or job_data.get("link"),
            source=source
        )
        db.add(job)
        db.commit()
        db.refresh(job)

    return job
