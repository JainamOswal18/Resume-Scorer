#!/usr/bin/env python3
"""
Setup script for Resume Scorer

This script initializes all required components:
1. Creates the SQLite database and tables
2. Creates required directories
3. Seeds initial data
"""

import os
import shutil
from pathlib import Path

# Create directories
dirs_to_create = [
    'database',
    'uploads',
]

for directory in dirs_to_create:
    os.makedirs(directory, exist_ok=True)
    print(f"Created {directory}/ directory")

# Initialize database
from init_db import create_tables, seed_job_details
create_tables()
print("Created database tables")
seed_job_details()
print("Seeded job details")

# Create .env file if it doesn't exist
env_template = """# GitHub API Token (for scraping GitHub profiles during resume evaluation)
GITHUB_API_TOKEN="your_github_token"

# Email service configuration
MAILGUN_API_KEY="your_mailgun_api_key"
MAILGUN_DOMAIN="your_mailgun_domain"

# Ollama configuration (optional)
OLLAMA_MODEL="openhermes"
"""

env_file = Path('.env')
if not env_file.exists():
    with open(env_file, 'w') as f:
        f.write(env_template)
    print("Created .env file template")
else:
    print(".env file already exists, not overwriting")

print("\nSetup complete! You can now run the application with:")
print("python -m uvicorn app:app --reload")
print("\nDon't forget to fill in your GitHub API token and email service credentials in the .env file.") 