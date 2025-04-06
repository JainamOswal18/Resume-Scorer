import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

def generate_interview_slots():
    """Generate random interview slots for the next week"""
    base_date = datetime.now() + timedelta(days=2)  # Start from 2 days from now
    slots = []
    
    for i in range(3):  # Generate 3 slots
        date = base_date + timedelta(days=i)
        time = random.choice(['10:00 AM', '2:00 PM', '4:00 PM'])
        format_type = random.choice(['Technical Interview', 'HR Interview', 'Technical + HR Interview'])
        slots.append({
            'date': date.strftime('%B %d, %Y'),
            'time': time,
            'format': format_type
        })
    return slots

def send_email(to_email, subject, body):
    """Send email using Mailgun sandbox domain"""
    try:
        # Mailgun sandbox configuration
        api_key = os.getenv('MAILGUN_API_KEY')
        sandbox_domain = "sandboxe84f1f2b58134ac68fff83c29c58485e.mailgun.org"
        
        # Mailgun API endpoint
        url = f"https://api.mailgun.net/v3/{sandbox_domain}/messages"
        
        # Send request
        response = requests.post(
            url,
            auth=("api", api_key),
            data={
                "from": f"Mailgun Sandbox <postmaster@{sandbox_domain}>",
                "to": to_email,
                "subject": subject,
                "text": body
            }
        )
        
        return response.status_code == 200
    except Exception as e:
        return False

def send_interview_invitation(candidate_name, candidate_email, job_title):
    """Send interview invitation email to shortlisted candidates"""
    slots = generate_interview_slots()
    
    # Format the slots for email
    slots_text = "\n".join([
        f"- {slot['date']} at {slot['time']} ({slot['format']})"
        for slot in slots
    ])
    
    subject = f'Interview Invitation for {job_title} Position'
    body = f"""
Dear {candidate_name},

Congratulations! We are impressed with your application for the {job_title} position. 
Your profile has been shortlisted for the next round of interviews.

We would like to invite you for an interview. Please choose one of the following slots:

{slots_text}

Please reply to this email with your preferred slot. If none of these slots work for you, 
please let us know your availability for the next week.

Looking forward to meeting you!

Best regards,
Hiring Team
"""
    
    return send_email(candidate_email, subject, body)

def send_rejection_feedback(candidate_name, candidate_email, job_title, feedback):
    """Send rejection email with feedback to candidates"""
    subject = f'Application Update for {job_title} Position'
    body = f"""
Dear {candidate_name},

Thank you for applying for the {job_title} position. After careful consideration, 
we regret to inform you that we will not be moving forward with your application at this time.

We appreciate the time and effort you put into your application. Please find below personalized feedback on your application:

{feedback}

Best regards,
Hiring Team
"""
    
    return send_email(candidate_email, subject, body)