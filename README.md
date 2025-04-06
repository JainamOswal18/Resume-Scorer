# Resume Scorer

An AI-powered resume scoring system that evaluates resumes against job descriptions and GitHub portfolios, providing personalized feedback to candidates.

## Features

- Resume analysis against job descriptions with detailed parameter scoring
- Similarity matching between resume and job requirements
- GitHub portfolio evaluation for technical skills assessment
- Personalized feedback with tailored improvement suggestions
- Automated email notifications for accepted/rejected candidates
- Interactive web interface for job listings and applications
- Local LLM support with Ollama with resilient fallback mechanisms
- SQLite database for easy setup and portability

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm 8+
- GitHub API token (for GitHub portfolio analysis)
- Mailgun API key (for email notifications)
- Ollama installed with OpenHermes model (or alternative LLM)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/JainamOswal18/TheBetterHack2025.git
   cd TheBetterHack2025
   ```

2. **Set up environment variables**

   Create an environment file:

   `.env` (for backend):
   ```env
   GITHUB_API_TOKEN="your_github_token"
   MAILGUN_API_KEY="your_mailgun_api_key"
   MAILGUN_DOMAIN="your_mailgun_domain"
   ```

3. **Install Ollama and download the OpenHermes model**
   ```bash
   # Install Ollama first from https://ollama.com
   # Then download the OpenHermes model
   ollama pull openhermes
   ```

4. **Set up the backend**
   ```bash
   # Install dependencies (Arch Linux example)
   sudo pacman -S python-sqlalchemy python-fastapi python-uvicorn python-pip python-pymupdf python-requests
   
   # Or using pip
   pip install fastapi uvicorn sqlalchemy pymupdf requests python-dotenv
   
   # Initialize the database
   python reset_db.py
   ```

5. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. **Start the Ollama service**
   ```bash
   ollama serve
   ```

2. **Start the backend server**
   ```bash
   python -m uvicorn app:app --reload
   ```

3. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```

4. Open `http://localhost:3000` in your browser

## System Architecture

### Backend Components
- **FastAPI Server**: Handles HTTP requests and serves the API
- **SQLite Database**: Stores job listings and candidate submissions
- **Scoring Engine**: Evaluates resumes using LLM and GitHub analysis
- **Email Service**: Sends notifications to candidates

### Frontend Components
- **Next.js Application**: Responsive web interface
- **API Client**: Communicates with the backend
- **Job Application Form**: For resume submission
- **Job Listings Page**: Displays available positions

## Scoring Mechanism

The scoring system evaluates candidates on three main criteria:

1. **Parameter Score (20 points)**
   - Impact: Achievements and results (0-5)
   - Format: Resume structure and presentation (0-5)
   - Language: Writing quality and clarity (0-5)
   - Skills: Technical and soft skills (0-5)

2. **Job Similarity Score (60 points)**
   - Required Skills Match (30 points)
   - Experience Level Match (15 points)
   - Education Match (15 points)

3. **GitHub Score (20 points)**
   - Project Relevance (8 points)
   - Technical Complexity (6 points)
   - Code Quality (6 points)

Candidates with a total score of 70% or higher receive an interview invitation, while others receive personalized feedback.

## Environment Variables

### Required
- `GITHUB_API_TOKEN`: GitHub personal access token for repository analysis
- `MAILGUN_API_KEY`: API key for Mailgun email service
- `MAILGUN_DOMAIN`: Your Mailgun domain for sending emails

### Optional
- `OPENAI_API_KEY` or `GEMINI_API_KEY`: Only needed if not using Ollama

## Advanced Configuration

### Switching LLM Providers
This application primarily uses Ollama with OpenHermes, but can be configured to use other LLM providers by modifying the `agents.py` file.

### Customizing Job Descriptions
Edit the `init_db.py` file to add or modify job descriptions.

### Resetting the Database
Use `reset_db.py` to clear the database and reinitialize with fresh job descriptions.

## Troubleshooting

- **Ollama not responding**: The application includes an auto-restart mechanism, but you can manually restart with `ollama serve`
- **Slow responses**: Consider using a smaller model like `openhermes:3b` or `llama3:8b`
- **Email not sending**: Verify your Mailgun API key and authorized recipients
- **Scoring issues**: Check the logs for details on score parsing and calculation

## Development

- Backend API runs on `http://localhost:8000`
- Frontend development server runs on `http://localhost:3000`
- API documentation available at `http://localhost:8000/docs`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.