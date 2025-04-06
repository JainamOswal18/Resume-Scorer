import requests
import re
import os
from dotenv import load_dotenv
import ollama
import json
import threading
import time

# Load environment variables from .env file
load_dotenv()

# System message for the resume scorer
SYSTEM_PROMPT = """You are a professional resume scorer who evaluates resumes against job descriptions. 
You provide detailed scores in specific categories and give helpful feedback.
Your scores MUST be integers only (no decimals) and follow strict guidelines:
- IMPACT, FORMAT, LANGUAGE, SKILLS: Each must be between 0-5, with a total not exceeding 20
- SIMILARITY: Must be between 0-60
- GITHUB: Must be between 0-20
- TOTAL: Must be the sum of all scores above, and must be between 0-100

For example, if IMPACT=4, FORMAT=4, LANGUAGE=4, SKILLS=4, SIMILARITY=42, GITHUB=15, then TOTAL must equal 73."""

def restart_ollama():
    """
    Tries to restart the Ollama service
    Returns True if successful or False otherwise
    """
    try:
        import subprocess
        print("Attempting to restart Ollama service...")
        # Check if Ollama is running
        ps_result = subprocess.run(
            ["ps", "-ef"], 
            capture_output=True, 
            text=True
        )
        
        if "ollama serve" in ps_result.stdout:
            print("Ollama process found, attempting to restart...")
            # Try killing the process
            subprocess.run(
                ["pkill", "-f", "ollama"], 
                capture_output=True
            )
            # Wait a moment
            time.sleep(2)
        
        # Start Ollama in the background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Give it a moment to start up
        time.sleep(5)
        
        # Check if it's running now
        ps_check = subprocess.run(
            ["ps", "-ef"], 
            capture_output=True, 
            text=True
        )
        
        if "ollama serve" in ps_check.stdout:
            print("Successfully restarted Ollama service!")
            return True
        else:
            print("Failed to restart Ollama service.")
            return False
            
    except Exception as e:
        print(f"Error restarting Ollama: {e}")
        return False

# Function to use Ollama directly for scoring resumes
def score_with_ollama(prompt, model_name="openhermes"):
    """
    Uses Ollama directly to score resumes without smolagents
    """
    try:
        # Add timeout to prevent hanging indefinitely
        response_container = {"response": None, "error": None}
        
        def ollama_request():
            try:
                result = ollama.generate(
                    model=model_name,
                    prompt=f"{SYSTEM_PROMPT}\n\n{prompt}",
                    options={
                        "temperature": 0.2,  # Lower temperature for more consistent scoring
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_gpu": 1,
                        "num_thread": 4
                    }
                )
                response_container["response"] = result
            except Exception as e:
                response_container["error"] = str(e)
        
        # Start Ollama request in a separate thread
        ollama_thread = threading.Thread(target=ollama_request)
        ollama_thread.daemon = True
        ollama_thread.start()
        
        # Wait for response with timeout (30 seconds)
        timeout = 20  # seconds
        start_time = time.time()
        while ollama_thread.is_alive() and time.time() - start_time < timeout:
            time.sleep(0.5)
        
        # Check if we have a response or timed out
        if time.time() - start_time >= timeout:
            print(f"Error: Ollama request timed out after {timeout} seconds")
            
            # Try restarting Ollama
            restart_successful = restart_ollama()
            
            if restart_successful:
                print("Retrying request with restarted Ollama service...")
                # Try the request one more time with a shorter timeout
                new_response_container = {"response": None, "error": None}
                
                def retry_request():
                    try:
                        result = ollama.generate(
                            model=model_name,
                            prompt=f"{SYSTEM_PROMPT}\n\n{prompt}",
                            options={
                                "temperature": 0.2,
                                "top_p": 0.9,
                                "top_k": 40,
                                "num_gpu": 1,
                                "num_thread": 4
                            }
                        )
                        new_response_container["response"] = result
                    except Exception as e:
                        new_response_container["error"] = str(e)
                
                retry_thread = threading.Thread(target=retry_request)
                retry_thread.daemon = True
                retry_thread.start()
                
                # Wait with a shorter timeout
                retry_timeout = 15  # seconds
                retry_start = time.time()
                while retry_thread.is_alive() and time.time() - retry_start < retry_timeout:
                    time.sleep(0.5)
                
                # Check if retry worked
                if new_response_container["response"]:
                    print("Retry successful!")
                    print("\n==== RESPONSE FROM OLLAMA (RETRY) ====")
                    print(new_response_container["response"]['response'])
                    print("==== END OF RESPONSE ====\n")
                    return new_response_container["response"]['response']
            
            # If we get here, both attempts failed or restart failed
            # Use a default scoring mechanism instead
            return generate_default_scoring(prompt)
        
        # Check if there was an error
        if response_container["error"]:
            print(f"Error calling Ollama: {response_container['error']}")
            
            # Try restarting if it's a connection error
            if "connection" in response_container["error"].lower() or "failed" in response_container["error"].lower():
                if restart_ollama():
                    print("Retrying after restart...")
                    # Try one more time with direct call (no threading)
                    try:
                        result = ollama.generate(
                            model=model_name,
                            prompt=f"{SYSTEM_PROMPT}\n\n{prompt}",
                            options={
                                "temperature": 0.2,
                                "top_p": 0.9,
                                "top_k": 40,
                                "num_gpu": 1,
                                "num_thread": 4
                            }
                        )
                        print("\n==== RESPONSE FROM OLLAMA (AFTER RESTART) ====")
                        print(result['response'])
                        print("==== END OF RESPONSE ====\n")
                        return result['response']
                    except Exception as retry_e:
                        print(f"Retry failed after restart: {retry_e}")
            
            return generate_default_scoring(prompt)
        
        if response_container["response"]:
            print("\n==== RESPONSE FROM OLLAMA ====")
            print(response_container["response"]['response'])
            print("==== END OF RESPONSE ====\n")
            return response_container["response"]['response']
        else:
            print("Error: No response received from Ollama")
            return generate_default_scoring(prompt)
            
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return generate_default_scoring(prompt)

def generate_default_scoring(prompt):
    """Generate a reasonable default score when Ollama fails to respond"""
    print("Generating default scores based on resume content...")
    
    # Extract portions of the prompt to analyze
    resume_match = re.search(r'Resume:\s*(.*?)(?=GitHub Portfolio:|$)', prompt, re.DOTALL)
    job_match = re.search(r'Job Description:\s*(.*?)(?=Resume:|$)', prompt, re.DOTALL)
    
    resume_text = resume_match.group(1).strip() if resume_match else ""
    job_text = job_match.group(1).strip() if job_match else ""
    
    # Generate reasonable default scores
    # Parameter scores - default to above average
    impact = 4
    format = 4
    language = 4
    skills = 4
    
    # Job similarity - calculate basic keyword matching
    similarity = 30  # Default moderate match
    
    # Try to improve similarity score with basic keyword matching if we have text
    if resume_text and job_text:
        # Convert to lowercase for comparison
        resume_lower = resume_text.lower()
        job_lower = job_text.lower()
        
        # Extract potential keywords from job description (very simple approach)
        job_words = set([w.strip(',.;:()[]{}') for w in job_lower.split() if len(w) > 4])
        matches = sum(1 for word in job_words if word in resume_lower)
        
        # Adjust similarity score based on keyword matches
        if len(job_words) > 0:
            match_percentage = min(matches / len(job_words), 1.0)
            similarity = int(match_percentage * 60)  # Scale to max 60 points
    
    # Default moderate GitHub score
    github = 15
    
    # Calculate total
    total = impact + format + language + skills + similarity + github
    
    # Construct response in the expected format
    return f"""
    IMPACT: {impact}
    FORMAT: {format}
    LANGUAGE: {language}
    SKILLS: {skills}
    SIMILARITY: {similarity}
    GITHUB: {github}
    TOTAL: {total}
    """

# GitHub API token
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

# Headers for GitHub API
HEADERS = {"Authorization": f"token {GITHUB_API_TOKEN}"}

# Use a session for performance
session = requests.Session()
session.headers.update(HEADERS)


def is_github_link(url):
    """Checks if a URL is a valid GitHub link."""
    return re.match(r"https?://github\.com/[\w-]+", url) is not None


def extract_github_details(url):
    """Extracts username and repo (if applicable) from a GitHub URL."""
    parts = url.rstrip('/').split('/')

    if len(parts) == 4:  # Profile link: github.com/username
        return parts[3], None
    elif len(parts) > 4:  # Repo link: github.com/username/repo
        return parts[3], parts[4] if parts[4] not in ["issues", "pulls", "tree", "blob"] else None
    return None, None


def fetch_github_profile(username):
    """Fetches GitHub user profile data."""
    url = f"https://api.github.com/users/{username}"
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "profile_url": data.get("html_url"),
            "name": data.get("name"),
            "bio": data.get("bio"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "following": data.get("following")
        }
    return None


def fetch_github_repo(username, repo):
    """Fetches GitHub repository data."""
    repo_url = f"https://api.github.com/repos/{username}/{repo}"
    response = session.get(repo_url)

    if response.status_code == 200:
        data = response.json()
        return {
            "repo_url": data.get("html_url"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "language": data.get("language")
        }
    return None


def fetch_readme(username, repo):
    """Fetches the README.md content for a repository."""
    url = f"https://api.github.com/repos/{username}/{repo}/readme"
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        readme_content = session.get(data["download_url"]).text
        return re.sub(r"[\n\r]+", " ", readme_content)[:500]  # Clean & limit to 500 chars
    return "README not found"


def fetch_profile_readme(username):
    """Fetches profile README (from username/username repo)."""
    return fetch_readme(username, username)  # Profile README is stored in a repo with the same name as username


def fetch_languages(username, repo):
    """Fetches languages used in a repository."""
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    response = session.get(url)

    if response.status_code == 200:
        return list(response.json().keys())  # List of languages
    return []


def fetch_contributions(username):
    """Fetches user contributions from GitHub API (approximation)."""
    url = f"https://api.github.com/users/{username}/events"
    response = session.get(url)

    if response.status_code == 200:
        return len(response.json())  # Approximate count
    return 0


def scrape_github_data(links):
    """Extracts and scrapes relevant GitHub data."""
    github_data = {"profiles": [], "projects": []}

    for link in links:
        if not is_github_link(link):
            continue  # Skip non-GitHub links

        username, repo = extract_github_details(link)

        if username and not repo:  # It's a profile
            profile_data = fetch_github_profile(username)
            if profile_data:
                profile_data["contributions"] = fetch_contributions(username)
                profile_data["profile_readme"] = fetch_profile_readme(username)
                github_data["profiles"].append(profile_data)

        elif username and repo:  # It's a repository
            repo_data = fetch_github_repo(username, repo)
            if repo_data:
                repo_data["languages"] = fetch_languages(username, repo)
                repo_data["readme"] = fetch_readme(username, repo)
                github_data["projects"].append(repo_data)

    return github_data


def score_resume(resume_text, job_description, extracted_links):
    try:
        # Prepare the prompt for Ollama
        scoring_prompt = f"""
        Score this resume in three parts, strictly adhering to the point allocations below:

        PART 1: RESUME PARAMETERS (20 points total)
        Score each parameter from 0-5 (total must not exceed 20):
        1. Impact: Measurable achievements and results
        2. Format: Clear structure and professional presentation
        3. Language: Grammar, spelling, and professional writing
        4. Skills: Demonstrated technical and soft skills

        PART 2: JOB SIMILARITY (60 points total)
        Compare resume with job requirements:
        - Required Skills Match (30 points)
        - Experience Level Match (15 points)
        - Education Match (15 points)

        PART 3: GITHUB PROJECTS (20 points total)
        Evaluate GitHub portfolio, awarding a total between 0-20 points:
        - Project Relevance (8 points)
        - Technical Complexity (6 points)
        - Code Quality (6 points)

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        GitHub Portfolio:
        {json.dumps(scrape_github_data(extracted_links), indent=2)}

        IMPORTANT: You MUST output EXACTLY in this format, with no additional text:
        IMPACT: <score 0-5>
        FORMAT: <score 0-5>
        LANGUAGE: <score 0-5>
        SKILLS: <score 0-5>
        SIMILARITY: <score 0-60>
        GITHUB: <score 0-20>
        TOTAL: <sum between 0-100>

        All scores must be integers, not decimals. 
        The total score MUST be equal to the sum of all individual scores.
        
        For example, if:
        IMPACT: 4
        FORMAT: 4
        LANGUAGE: 4
        SKILLS: 4
        SIMILARITY: 42
        GITHUB: 15
        
        Then:
        TOTAL: 73  (because 4+4+4+4+42+15=73)
        """

        print("\n==== PROMPT SENT TO OLLAMA ====")
        print(scoring_prompt)
        print("==== END OF PROMPT ====\n")
        
        # Get response directly from Ollama
        response = score_with_ollama(scoring_prompt)
        
        # Parse the string response into a dictionary
        scores = {}
        if isinstance(response, str):
            # First, try to find a JSON string in case Ollama returns one
            try:
                # Look for JSON-like structure with regex
                import re
                json_match = re.search(r'({[\s\S]*})', response)
                if json_match:
                    json_str = json_match.group(1)
                    # Try to parse as JSON
                    try:
                        json_data = json.loads(json_str)
                        # Check if this is a valid scores dict
                        if any(k in json_data for k in ['IMPACT', 'FORMAT', 'LANGUAGE', 'SKILLS', 'SIMILARITY', 'GITHUB', 'TOTAL']):
                            scores = {k.upper(): v for k, v in json_data.items()}
                            print("Successfully extracted scores from JSON in response")
                    except json.JSONDecodeError:
                        print("Found JSON-like structure but couldn't parse it")
            except Exception as e:
                print(f"Error trying to extract JSON: {e}")
            
            # If JSON extraction didn't work, fall back to line-by-line parsing
            if not scores:
                print("Falling back to line-by-line parsing")
                # Split by newlines and process each line
                for line in response.split('\n'):
                    line = line.strip()
                    # Skip empty lines or lines without a colon
                    if not line or ':' not in line:
                        continue
                        
                    # Extract key and value
                    parts = line.split(':', 1)
                    if len(parts) != 2:
                        continue
                    
                    key = parts[0].strip().upper()  # Normalize keys to uppercase
                    value_text = parts[1].strip()
                    
                    # Skip if key is not one of our expected keys
                    if key not in ['IMPACT', 'FORMAT', 'LANGUAGE', 'SKILLS', 'SIMILARITY', 'GITHUB', 'TOTAL']:
                        continue
                    
                    # Extract numeric value from the text
                    try:
                        # Find all digits in the value text
                        number_match = re.search(r'\b(\d+)\b', value_text)
                        if number_match:
                            scores[key] = int(number_match.group(1))
                        else:
                            print(f"No numeric value found in: {line}")
                            # Will be handled by the default value logic below
                    except ValueError as e:
                        print(f"Error parsing value in line '{line}': {e}")
        else:
            scores = response  # In case it's already a dictionary
        
        print("\n==== EXTRACTED SCORES ====")
        print(scores)
        print("==== END OF EXTRACTED SCORES ====\n")
        
        # Ensure all required keys exist with valid values
        for key in ['IMPACT', 'FORMAT', 'LANGUAGE', 'SKILLS']:
            if key not in scores or not isinstance(scores[key], (int, float)) or scores[key] < 0 or scores[key] > 5:
                scores[key] = 4  # Default reasonable value
        
        # Calculate parameter score (sum of the individual parameter scores)
        parameter_score = scores.get('IMPACT', 0) + scores.get('FORMAT', 0) + scores.get('LANGUAGE', 0) + scores.get('SKILLS', 0)
        # Make sure parameter score doesn't exceed 20
        parameter_score = min(parameter_score, 20)
        
        # Fix GitHub score
        if 'GITHUB' not in scores or not isinstance(scores['GITHUB'], (int, float)) or scores['GITHUB'] < 0 or scores['GITHUB'] > 20:
            scores['GITHUB'] = 15  # Default to 75% of max
        else:
            # Ensure GitHub score is capped at 20
            scores['GITHUB'] = min(scores['GITHUB'], 20)

        # Fix Similarity score - this is often where hallucinations happen
        if 'SIMILARITY' not in scores or not isinstance(scores['SIMILARITY'], (int, float)) or scores['SIMILARITY'] < 0 or scores['SIMILARITY'] > 60:
            # If the similarity score is invalid (like being too low with a high total),
            # we'll generate a reasonable score based on other scores
            if 'TOTAL' in scores and scores['TOTAL'] > 75:
                # For high total scores, similarity should be at least 70% of max (42)
                scores['SIMILARITY'] = 42
            elif 'TOTAL' in scores and scores['TOTAL'] > 50:
                # For medium-high total scores, similarity should be around 60% of max (36)
                scores['SIMILARITY'] = 36
            else:
                # Default case
                scores['SIMILARITY'] = 30  # 50% of max
        else:
            # Ensure Similarity score is capped at 60
            scores['SIMILARITY'] = min(scores['SIMILARITY'], 60)
        
        # Calculate expected total based on component scores
        expected_total = parameter_score + scores.get('SIMILARITY', 0) + scores.get('GITHUB', 0)
        
        # If there's a significant discrepancy between provided total and calculated total,
        # or if no total was provided, use the calculated total
        if 'TOTAL' not in scores or abs(scores.get('TOTAL', 0) - expected_total) > 5:
            scores['TOTAL'] = expected_total
        
        # Ensure total never exceeds 100
        scores['TOTAL'] = min(scores['TOTAL'], 100)
        
        # Final check: if total still doesn't match components, adjust similarity to make it consistent
        final_expected_total = parameter_score + scores.get('SIMILARITY', 0) + scores.get('GITHUB', 0)
        if abs(scores.get('TOTAL', 0) - final_expected_total) > 0:
            # Adjust similarity to make total match expected total
            similarity_adjustment = scores.get('TOTAL', 0) - (parameter_score + scores.get('GITHUB', 0))
            # Ensure adjusted similarity is within bounds
            scores['SIMILARITY'] = max(0, min(60, similarity_adjustment))
            
        # Final compilation of results
        evaluation = {
            "Parameter Score": int(parameter_score),
            "Job Similarity Score": int(scores.get('SIMILARITY', 0)),
            "GitHub Score": int(scores.get('GITHUB', 0)),
            "Total Score": int(scores.get('TOTAL', 0))
        }
        
        # Generate feedback based on the score
        evaluation["Feedback"] = generate_feedback(
            evaluation["Total Score"],
            evaluation["Parameter Score"],
            evaluation["Job Similarity Score"], 
            evaluation["GitHub Score"],
            job_description
        )
        
        # Log the final scores for debugging
        print("\n==== PARSED SCORES ====")
        print(f"Parameter Score: {evaluation['Parameter Score']}")
        print(f"Job Similarity Score: {evaluation['Job Similarity Score']}")
        print(f"GitHub Score: {evaluation['GitHub Score']}")
        print(f"Total Score: {evaluation['Total Score']}")
        # Verify that scores add up correctly
        print(f"Sum of components: {parameter_score + scores.get('SIMILARITY', 0) + scores.get('GITHUB', 0)}")
        print("==== END OF PARSED SCORES ====\n")
        
        return evaluation

    except Exception as e:
        print(f"Error in score_resume: {e}")
        # Provide a default evaluation in case of errors
        return {
            "Parameter Score": 16,
            "Job Similarity Score": 45,
            "GitHub Score": 15,
            "Total Score": 76,
            "Feedback": "We encountered an error while processing your resume. Please try again or contact support if the issue persists."
        }


# Test case (Only runs when executed directly)
if __name__ == "__main__":
    sample_resume = "Experienced Data Scientist with ML expertise."
    sample_job_description = "Looking for a Data Scientist with Python and ML experience."
    sample_links = ["https://github.com/jainamoswal18/"]

    result = score_resume(sample_resume, sample_job_description, sample_links)
    print(result)

def clean_text(text):
    """Clean text from model outputs to ensure consistent formatting."""
    if not text:
        return ""
    
    # Remove any markdown or code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    # Remove any JSON formatting marks
    text = re.sub(r'[\'"{}\[\]]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common prefixes/suffixes that models might add
    prefixes = [
        'Here is my feedback:', 'Feedback:', 'I would provide the following feedback:',
        'Based on the evaluation:', 'The candidate feedback is:', 'Final feedback:',
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    return text

def generate_feedback(total_score, parameter_score, similarity_score, github_score, job_description):
    """Generate personalized feedback based on candidate scores"""
    
    # Extract job title from description for more personalized feedback
    job_title = "this position"
    title_match = re.search(r"Job Title:\s*([^\n]+)", job_description)
    if title_match:
        job_title = title_match.group(1).strip()
    
    # Extract key skills from job description
    skills_section = ""
    skills_match = re.search(r"Skills Requirements:(.*?)(?=\n\n|$)", job_description, re.DOTALL)
    if skills_match:
        skills_section = skills_match.group(1).strip()
    
    # Base feedback on total score
    if total_score >= 85:
        overall = f"Congratulations! Your profile is an excellent match for {job_title}. Your resume demonstrates strong qualifications that align well with our requirements."
    elif total_score >= 70:
        overall = f"Your profile shows good potential for {job_title}. You meet many of our key requirements, though there may be areas for improvement."
    elif total_score >= 50:
        overall = f"Thank you for your interest in {job_title}. While you have some relevant qualifications, your profile doesn't fully align with our current requirements."
    else:
        overall = f"Thank you for your application for {job_title}. Unfortunately, your current qualifications don't match our requirements for this particular role."
    
    # Specific feedback on resume parameters
    if parameter_score >= 16:
        resume_feedback = "Your resume is well-structured with clear achievements and professional presentation."
    elif parameter_score >= 12:
        resume_feedback = "Your resume is satisfactory but could be improved with more quantifiable achievements and clearer organization."
    else:
        resume_feedback = "Your resume would benefit from significant improvements in structure, clarity, and highlighting specific achievements."
    
    # Specific feedback on job similarity
    job_match_percent = round((similarity_score / 60) * 100)
    if similarity_score >= 45:
        similarity_feedback = f"Your skills and experience are {job_match_percent}% aligned with our requirements for this role."
    elif similarity_score >= 30:
        similarity_feedback = f"Your background shows some alignment ({job_match_percent}%) with our requirements, but there are some key skills or experiences missing."
    else:
        similarity_feedback = f"Your current skill set shows limited alignment ({job_match_percent}%) with the specific requirements for this position."
    
    # Specific feedback on GitHub projects
    if github_score >= 16:
        github_feedback = "Your GitHub portfolio demonstrates impressive technical skills directly relevant to this position."
    elif github_score >= 10:
        github_feedback = "Your GitHub projects show good technical capabilities, though more relevant work would strengthen your application."
    elif github_score > 0:
        github_feedback = "While you have some GitHub projects, they don't strongly demonstrate the technical skills we're looking for."
    else:
        github_feedback = "Adding relevant technical projects to a public repository would significantly strengthen your application."
    
    # Combine all feedback
    full_feedback = f"{overall}\n\n{resume_feedback} {similarity_feedback} {github_feedback}"
    
    # Add next steps based on total score
    if total_score >= 70:
        next_steps = "\n\nWe'd like to invite you to the next stage of our interview process. Our team will contact you shortly with more details."
        full_feedback += next_steps
    else:
        # Generate personalized improvement suggestions for rejected candidates
        suggestions = generate_improvement_suggestions(parameter_score, similarity_score, github_score, job_description, skills_section)
        full_feedback += f"\n\n{suggestions}"
    
    return full_feedback

def generate_improvement_suggestions(parameter_score, similarity_score, github_score, job_description, skills_section):
    """Generate specific improvement suggestions based on candidate's weak areas"""
    
    suggestions = []
    
    # Identify the weakest area
    scores = {
        "resume": parameter_score / 20,  # Normalize to 0-1
        "skills": similarity_score / 60,  # Normalize to 0-1
        "github": github_score / 20      # Normalize to 0-1
    }
    
    weakest_area = min(scores, key=scores.get)
    
    # Resume-specific suggestions
    if weakest_area == "resume" or scores["resume"] < 0.6:
        if parameter_score < 10:
            suggestions.append("Your resume would benefit from a complete overhaul. Consider using industry-standard templates and focusing on quantifiable achievements rather than just listing responsibilities.")
        else:
            suggestions.append("To improve your resume: Add specific metrics and outcomes to your achievements, ensure consistent formatting, and tailor your experience descriptions to highlight relevant skills.")
    
    # Skills-specific suggestions
    if weakest_area == "skills" or scores["skills"] < 0.5:
        # Extract key skills from job description if available
        key_skills = []
        if skills_section:
            # Simple extraction of bullet points or comma-separated skills
            skills_lines = skills_section.split('\n')
            for line in skills_lines:
                if '-' in line or '•' in line:
                    skill = re.sub(r'^[•\-\s]+', '', line).strip()
                    if skill:
                        key_skills.append(skill)
        
        if key_skills:
            skill_suggestions = ", ".join(key_skills[:3])  # Limit to first 3 skills
            suggestions.append(f"Focus on developing these key skills that were missing from your application: {skill_suggestions}")
        else:
            suggestions.append("Review the job requirements carefully and focus on acquiring the specific technical skills mentioned in the posting.")
    
    # GitHub-specific suggestions
    if weakest_area == "github" or scores["github"] < 0.5:
        if github_score == 0:
            suggestions.append("Creating a GitHub portfolio with projects relevant to this role would significantly strengthen future applications.")
        else:
            suggestions.append("Improve your GitHub portfolio by adding more projects that demonstrate the specific technical skills required for this position, ensuring they have clear documentation and follow best practices.")
    
    # Add a general encouraging note
    encouragement = "We encourage you to apply for future positions that better match your skill set and experience level."
    
    # Combine all suggestions
    if suggestions:
        return "For future applications, we recommend the following improvements:\n• " + "\n• ".join(suggestions) + f"\n\n{encouragement}"
    else:
        return f"For future applications, consider focusing on developing skills in specific areas mentioned in the job description and showcasing relevant projects. {encouragement}"
