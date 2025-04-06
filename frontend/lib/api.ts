/**
 * API client for the Resume Scorer backend
 */

// API base URL - use environment variable in production
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * Get all job listings
 */
export async function getJobs() {
  const response = await fetch(`${API_BASE_URL}/job-details`);
  
  if (!response.ok) {
    throw new Error(`Error fetching jobs: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get a specific job by ID
 */
export async function getJob(jobId: number) {
  const response = await fetch(`${API_BASE_URL}/job-details/${jobId}`);
  
  if (!response.ok) {
    throw new Error(`Error fetching job: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get all candidates
 */
export async function getCandidates() {
  const response = await fetch(`${API_BASE_URL}/candidates`);
  
  if (!response.ok) {
    throw new Error(`Error fetching candidates: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Submit a resume
 */
export async function submitResume(formData: FormData) {
  const response = await fetch(`${API_BASE_URL}/submit-resume`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Error submitting resume: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get download URL for a resume
 */
export function getDownloadUrl(filePath: string) {
  return `${API_BASE_URL}/download/${filePath.replace('/uploads/', '')}`;
} 