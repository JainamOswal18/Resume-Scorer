from fastapi import FastAPI, UploadFile, Form, File, Depends, HTTPException, Response, Request
import fitz  # PyMuPDF
import io
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from sqlalchemy.orm import Session
from typing import List
import logging

# Import our modules
from models import get_db, JobDetails, Candidate
from file_storage import save_upload_file, serve_file
from agents import score_resume  # Importing the scoring function
from email_service import send_interview_invitation, send_rejection_feedback
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Resume Scorer API")

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory for serving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")  
def read_root():  
    return {"message": "HR Analytics API is running!"}

@app.get("/job-details", response_model=List[dict])
async def get_job_details(db: Session = Depends(get_db)):
    """Get all job details"""
    jobs = db.query(JobDetails).order_by(JobDetails.created_at.desc()).all()
    return [job.to_dict() for job in jobs]

@app.get("/job-details/{job_id}", response_model=dict)
async def get_job_detail(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job detail"""
    job = db.query(JobDetails).filter(JobDetails.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()

@app.get("/candidates", response_model=List[dict])
async def get_candidates(db: Session = Depends(get_db)):
    """Get all candidates"""
    candidates = db.query(Candidate).order_by(Candidate.id.desc()).all()
    return [candidate.to_dict() for candidate in candidates]

@app.post("/submit-resume")
async def submit_resume(
    name: str = Form(...),
    email: str = Form(...),
    job_id: int = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Starting resume submission for {name} ({email}) for job ID {job_id}")
        
        # Read the PDF file
        pdf_content = await resume.read()
        pdf_file = io.BytesIO(pdf_content)
        
        # Use PyMuPDF to extract text and links
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        
        # Extract text from all pages
        text_content = ""
        links = []
        
        for page in doc:
            # Extract text
            text_content += page.get_text()
            
            # Extract links
            page_links = page.get_links()
            for link in page_links:
                if 'uri' in link:
                    links.append(link['uri'])

        doc.close()
        logger.debug("PDF text and links extracted successfully")

        # Save the resume file locally
        file_name = f"{email}_resume.pdf"
        try:
            # Reset the file pointer
            await resume.seek(0)
            # Save the file
            file_path, resume_url = await save_upload_file(resume, file_name)
            logger.debug(f"Resume saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            return {"error": f"Failed to save file: {str(e)}"}

        # Get job details from database based on job_id
        job = db.query(JobDetails).filter(JobDetails.job_id == job_id).first()
        if not job:
            logger.error(f"Job with ID {job_id} not found in database")
            return {"error": f"Job with ID {job_id} not found"}
        
        job_description = f"""📌 Job Title: {job.job_title}

            🔍 Job Requirements
            1️⃣ Skills (Technical & Soft Skills):
            {job.skills_requirement}

            2️⃣ Experience:
            {job.experience_requirement}

            3️⃣ Educational Qualifications:
            {job.education_requirement}

            4️⃣ Additional Requirements:
            {job.additional_requirements or "None"}
            """

        logger.debug(f"Using job description for {job.job_title} (ID: {job_id})")
        
        # Call the score_resume function
        scoring_result = score_resume(text_content, job_description, links)
        logger.debug(f"Resume scored successfully: {scoring_result}")

        # Prepare candidate data
        candidate_data = Candidate(
            job_id=job.job_id,
            user_name=name,
            user_email=email,
            resume_url=resume_url,
            parameter_score=scoring_result["Parameter Score"],
            job_similarity_score=scoring_result["Job Similarity Score"],
            github_score=scoring_result["GitHub Score"],
            total_score=scoring_result["Total Score"]
        )
        
        # Store in database
        try:
            db.add(candidate_data)
            db.commit()
            logger.debug("Candidate data stored in database")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to store in database: {str(e)}")
            return {"error": f"Failed to store in database: {str(e)}"}

        # Calculate total score as a percentage
        total_score_percentage = (scoring_result["Total Score"] / 100) * 100
        logger.debug(f"Total score percentage: {total_score_percentage}%")

        # Send appropriate email based on score
        if total_score_percentage >= 70:
            logger.debug(f"Score is above threshold. Sending interview invitation to {email}")
            # Send interview invitation
            email_sent = send_interview_invitation(name, email, job.job_title)
            if email_sent:
                print(f"\n==== EMAIL SENT ====")
                print(f"Invitation email sent to {name} ({email})")
                print(f"Total Score: {total_score_percentage}% - QUALIFIED FOR INTERVIEW")
                print(f"==== END OF EMAIL INFO ====\n")
            else:
                print(f"\n==== EMAIL FAILED ====")
                print(f"Failed to send invitation email to {name} ({email})")
                print(f"==== END OF EMAIL INFO ====\n")
        else:
            logger.debug(f"Score is below threshold. Sending rejection to {email}")
            
            # Use the feedback generated by our scoring function
            feedback = scoring_result.get("Feedback", "")
            
            # Send rejection email with feedback
            email_sent = send_rejection_feedback(
                name, 
                email, 
                job.job_title,
                feedback
            )
            
            if email_sent:
                print(f"\n==== EMAIL SENT ====")
                print(f"Rejection email sent to {name} ({email})")
                print(f"Total Score: {total_score_percentage}% - NOT QUALIFIED FOR INTERVIEW")
                print(f"Feedback: {feedback[:100]}...")  # Print first 100 chars of feedback
                print(f"==== END OF EMAIL INFO ====\n")
            else:
                print(f"\n==== EMAIL FAILED ====")
                print(f"Failed to send rejection email to {name} ({email})")
                print(f"==== END OF EMAIL INFO ====\n")

        return {
            "name": name,
            "email": email,
            "job_id": job_id,
            "job_title": job.job_title,
            "resume_url": resume_url,
            "extracted_text": text_content,
            "extracted_links": links,
            "evaluation": scoring_result,
            "message": "Resume uploaded, stored, and evaluated successfully."
        }
    except Exception as e:
        logger.error(f"Error in submit_resume: {str(e)}")
        return {"error": f"Failed to process resume: {str(e)}"}

@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """Serve a file from the uploads directory"""
    file_url = f"/uploads/{file_path}"
    response = serve_file(file_url)
    if not response:
        raise HTTPException(status_code=404, detail="File not found")
    return response

# Run server with: uvicorn main:app --reload  
