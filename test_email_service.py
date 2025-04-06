import os
import sys
from datetime import datetime
import pytest
from email_service import send_interview_invitation, send_rejection_feedback, generate_interview_slots

# Add the parent directory to the path so we can import the email_service module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_environment_variables():
    """Test if required environment variables are set"""
    assert os.getenv('MAILGUN_API_KEY') is not None, "MAILGUN_API_KEY environment variable is not set"
    assert os.getenv('MAILGUN_DOMAIN') is not None, "MAILGUN_DOMAIN environment variable is not set"

def test_send_interview_invitation():
    """Test sending interview invitation email"""
    # Skip test if environment variables are not set
    if not os.getenv('MAILGUN_API_KEY') or not os.getenv('MAILGUN_DOMAIN'):
        pytest.skip("Skipping email tests - environment variables not set")
    
    # Test data
    candidate_name = "Test Candidate"
    candidate_email = "jainamoswal1811@gmail.com"  # Replace with your test email
    job_title = "Software Engineer"
    
    # Send the email
    result = send_interview_invitation(candidate_name, candidate_email, job_title)
    
    # Assert that the email was sent successfully
    assert result is True, "Failed to send interview invitation email"

def test_send_rejection_feedback():
    """Test sending rejection feedback email"""
    # Skip test if environment variables are not set
    if not os.getenv('MAILGUN_API_KEY') or not os.getenv('MAILGUN_DOMAIN'):
        pytest.skip("Skipping email tests - environment variables not set")
    
    # Test data
    candidate_name = "Test Candidate"
    candidate_email = "jainamoswal1811@gmail.com"  # Replace with your test email
    job_title = "Software Engineer"
    areas_of_improvement = """
- Improve your technical skills in Python and SQL
- Add more projects to your GitHub profile
- Gain more experience in software development
"""
    
    # Send the email
    result = send_rejection_feedback(candidate_name, candidate_email, job_title, areas_of_improvement)
    
    # Assert that the email was sent successfully
    assert result is True, "Failed to send rejection feedback email"

def test_email_content():
    """Test the content of generated emails"""
    # Test data
    candidate_name = "Test Candidate"
    job_title = "Software Engineer"
    
    # Test interview slots generation
    slots = generate_interview_slots()
    
    # Assert that we have 3 slots
    assert len(slots) == 3, "Should generate exactly 3 interview slots"
    
    # Assert that dates are in the future
    for slot in slots:
        slot_date = datetime.strptime(slot['date'], '%B %d, %Y')
        assert slot_date > datetime.now(), "Interview slots should be in the future"
    
    # Assert that times are valid
    valid_times = ['10:00 AM', '2:00 PM', '4:00 PM']
    for slot in slots:
        assert slot['time'] in valid_times, "Invalid time slot"
    
    # Assert that formats are valid
    valid_formats = ['Technical Interview', 'HR Interview', 'Technical + HR Interview']
    for slot in slots:
        assert slot['format'] in valid_formats, "Invalid interview format"

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 