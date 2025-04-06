#!/usr/bin/env python3
"""
Reset and reinitialize the database.
This script deletes the existing database and recreates it with fresh job details.
"""

import os
import shutil
from pathlib import Path

# Remove existing database
db_file = Path('database/resume_scorer.db')
if db_file.exists():
    os.remove(db_file)
    print("Removed existing database")

# Initialize database
from init_db import create_tables, seed_job_details
create_tables()
print("Created database tables")
seed_job_details()
print("Seeded job details")

print("\nDatabase reset complete! You can now run the application with:")
print("python -m uvicorn app:app --reload") 