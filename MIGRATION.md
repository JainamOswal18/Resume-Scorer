# Migration from Supabase to SQLite and Local Storage

This document outlines the migration process from Supabase to SQLite (for database) and local file storage (for resume PDFs).

## Migration Summary

### Backend Changes

1. **SQLAlchemy Models**
   - Created `models.py` with SQLAlchemy ORM models for `Candidate` and `JobDetails`
   - Set up SQLite connection and session management
   - Added helper functions for database operations

2. **Local File Storage**
   - Created `file_storage.py` for handling file uploads to local storage
   - Implemented functions for saving, retrieving, and serving files
   - Added directory creation and management

3. **FastAPI Endpoints**
   - Updated `app.py` to use SQLite via SQLAlchemy instead of Supabase
   - Modified endpoints to use local file storage
   - Added new endpoints for retrieving job details and candidates
   - Implemented a file serving endpoint for downloaded resumes

4. **Database Initialization**
   - Created `init_db.py` to initialize and seed the database
   - Added sample job details for initial data

5. **Setup Script**
   - Created `setup.py` to initialize the entire application
   - Script creates directories, database tables, and template .env file

### Frontend Changes

1. **API Client**
   - Created `frontend/lib/api.ts` as a central client for all API calls
   - Implemented functions for retrieving jobs, candidates, and submitting resumes

2. **Page Updates**
   - Updated `admin/page.tsx` to use the API client instead of Supabase
   - Updated `page.tsx` (home page) to fetch jobs from the API
   - Updated `apply/[id]/page.tsx` to fetch job details and submit resumes via the API

3. **Authentication**
   - Removed Supabase authentication in favor of a simpler approach
   - Admin dashboard now has a basic logout that redirects to home

### Package Updates

1. **Dependencies**
   - Added SQLAlchemy to `requirements.txt`
   - Removed Supabase-related packages from `requirements.txt`
   - Updated environment variable templates

## Folder Structure

```
├── app.py                   # FastAPI application
├── models.py                # SQLAlchemy models
├── file_storage.py          # Local file storage utilities
├── init_db.py               # Database initialization and seeding
├── setup.py                 # Application setup script
├── agents.py                # Resume scoring with Ollama
├── email_service.py         # Email services
├── database/                # SQLite database directory
│   └── resume_scorer.db     # SQLite database file
├── uploads/                 # Local file storage for resumes
├── frontend/
│   ├── app/
│   │   ├── admin/           # Admin dashboard
│   │   ├── apply/           # Application form
│   │   └── page.tsx         # Home page with job listings
│   └── lib/
│       ├── api.ts           # API client
│       └── ...
├── .env                     # Environment variables
└── requirements.txt         # Python dependencies
```

## Running the Application

1. **Initialize the application**
   ```bash
   python setup.py
   ```

2. **Start the backend server**
   ```bash
   python -m uvicorn app:app --reload
   ```

3. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```

## Environment Variables

The required environment variables are:

```
# GitHub API Token (for scraping GitHub profiles during resume evaluation)
GITHUB_API_TOKEN="your_github_token"

# Email service configuration
MAILGUN_API_KEY="your_mailgun_api_key"
MAILGUN_DOMAIN="your_mailgun_domain"

# Ollama configuration (optional)
OLLAMA_MODEL="openhermes"
```

## API Endpoints

The following endpoints are available:

- `GET /` - API status
- `GET /job-details` - Get all job listings
- `GET /job-details/{job_id}` - Get specific job details
- `GET /candidates` - Get all candidates
- `POST /submit-resume` - Submit a resume
- `GET /download/{file_path}` - Download a resume file 