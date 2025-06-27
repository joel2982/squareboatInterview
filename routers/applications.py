from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from models import Application, Job, User
from utils.auth import get_current_user
from utils.email_stub import send_email_stub
from database import get_db, UPLOAD_DIR
import os, shutil


router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/apply/{job_id}")
async def apply_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    resume: UploadFile = File(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if db.query(Application).filter(Application.candidate_id == current_user.id, Application.job_id == job_id).first():
        raise HTTPException(status_code=400, detail="Already applied to this job")
    resume_path = None
    if resume:
        resume_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
    application = Application(candidate_id=current_user.id, job_id=job_id, resume=resume_path)
    db.add(application)
    db.commit()
    db.refresh(application)
    background_tasks.add_task(send_email_stub, current_user.email, "Job Application Submitted", f"You applied to {job.title}")
    background_tasks.add_task(send_email_stub, job.recruiter.email, "New Applicant", f"{current_user.email} applied to your job: {job.title}")
    return {"message": "Applied successfully"}

@router.get("/{job_id}")
async def list_applicants(job_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can view applicants")
    job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return [{"candidate": a.candidate.email, "applied_at": a.timestamp, "resume": a.resume} for a in applications]
