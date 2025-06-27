from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import JobCreate, ApplicationOut, JobOut
from models import Job, Application, User
from utils.auth import get_current_user
from database import get_db
from typing import List

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobOut, status_code=201)
async def post_job(job: JobCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can post jobs")
    job_obj = Job(title=job.title, description=job.description, recruiter_id=current_user.id)
    db.add(job_obj)
    db.commit()
    db.refresh(job_obj)
    return job_obj

@router.get("/", response_model=List[JobOut])
def list_jobs(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "recruiter":
        jobs = db.query(Job).filter(Job.recruiter_id == current_user.id).all()
    if current_user.role == "candidate":
        jobs = db.query(Job).all()
    return jobs

@router.get("/applied", response_model=List[ApplicationOut])
def list_applied_jobs(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can view applied jobs")
    print(f"Current user ID: {current_user.id}")
    return db.query(Application).filter(Application.candidate_id == current_user.id).all()
