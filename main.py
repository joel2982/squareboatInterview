# main.py (refactored entry point)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.applications import router as applications_router
from routers.auth import router as auth_router
from routers.jobs import router as jobs_router

# --- FastAPI App ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)  # Ensure database tables are created

# Include routers
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(applications_router)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Job Website API is running."}

# --- Run the application ---
# To run the application, use the command:
# uvicorn main:app --reload