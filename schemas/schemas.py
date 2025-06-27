from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str = StringConstraints(min_length=6, strip_whitespace=True)
    role: str = StringConstraints(to_lower=True)
    # profile_pic: Optional[str] = None  # URL or path to the profile picture
    
    @field_validator('role')
    def validate_role(cls, v):
        if v not in ["candidate", "recruiter"]:
            raise ValueError("Role must be either 'candidate' or 'recruiter'")
        return v

class CurrentUser(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    profile_pic: Optional[str]
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class JobCreate(BaseModel):
    title: str
    description: str

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    recruiter_id: int
    class Config:
        from_attributes = True

class ApplicationOut(BaseModel):
    id: int
    job: JobOut
    timestamp: datetime
    resume: Optional[str]
    class Config:
        from_attributes = True

class ApplicationsList(BaseModel):
    applications: List[ApplicationOut] = []

    class Config:
        from_attributes = True

class JobList(BaseModel):
    jobs: List[JobOut] = []

    class Config:
        from_attributes = True
