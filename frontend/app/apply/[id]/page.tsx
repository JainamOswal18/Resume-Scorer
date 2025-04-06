'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Loader2, CheckCircle2, ArrowLeft, Briefcase, Code, GraduationCap, Clock, Plus } from 'lucide-react';
import Link from 'next/link';
import { getJob, submitResume } from '@/lib/api';

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

interface JobDetails {
  job_title: string;
  job_details: string;
  skills_requirement: string;
  education_requirement: string;
  experience_requirement: string;
  additional_requirements: string | null;
}

export default function ApplyPage() {
  const params = useParams();
  const router = useRouter();
  const [job, setJob] = useState<JobDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingSubmit, setLoadingSubmit] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    resume: null as File | null,
  });
  const [formErrors, setFormErrors] = useState({
    name: '',
    email: '',
    resume: '',
  });

  useEffect(() => {
    async function fetchJob() {
      try {
        if (!params.id) return;
        
        const jobId = Number(params.id);
        if (isNaN(jobId)) {
          router.push('/');
          return;
        }
        
        const jobData = await getJob(jobId);
        setJob(jobData);
      } catch (error) {
        console.error('Error fetching job:', error);
        router.push('/');
      } finally {
        setLoading(false);
      }
    }

    fetchJob();
  }, [params.id, router]);

  const validateForm = () => {
    let valid = true;
    const errors = {
      name: '',
      email: '',
      resume: '',
    };

    if (!formData.name.trim()) {
      errors.name = 'Name is required';
      valid = false;
    }

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email is invalid';
      valid = false;
    }

    if (!formData.resume) {
      errors.resume = 'Resume is required';
      valid = false;
    } else if (formData.resume.type !== 'application/pdf') {
      errors.resume = 'Resume must be a PDF file';
      valid = false;
    }

    setFormErrors(errors);
    return valid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoadingSubmit(true);

    try {
      const data = new FormData();
      data.append('name', formData.name);
      data.append('email', formData.email);
      const jobId = Number(params.id);
      data.append('job_id', jobId.toString());
      if (formData.resume) {
        data.append('resume', formData.resume);
      }

      console.log(`Submitting application for job ID: ${jobId}`);
      const response = await submitResume(data);
      
      if (response.error) {
        throw new Error(response.error);
      }

      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting resume:', error);
      alert('Failed to submit resume. Please try again.');
    } finally {
      setLoadingSubmit(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFormData((prev) => ({ ...prev, resume: e.target.files?.[0] || null }));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-background to-secondary">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-secondary py-12 flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-4">
          <div className="bg-card rounded-lg shadow-lg p-8 text-center">
            <div className="flex justify-center mb-4">
              <div className="bg-green-100 rounded-full p-4">
                <CheckCircle2 className="h-16 w-16 text-green-500" />
              </div>
            </div>
            <h1 className="text-3xl font-bold text-card-foreground mb-4">Application Submitted!</h1>
            <p className="text-muted-foreground mb-8">
              Thank you for applying to {job?.job_title}. We have received your application and will contact you soon.
            </p>
            <Link
              href="/"
              className="inline-flex items-center justify-center px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all duration-200 shadow-lg"
            >
              Return to Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary py-12">
      <div className="max-w-2xl mx-auto px-4">
        <Link
          href="/"
          className="inline-flex items-center text-primary hover:text-primary/80 mb-8"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Job Listings
        </Link>

        <div className="bg-card rounded-lg shadow-lg p-8">
          <div className="flex items-center mb-6">
            <Briefcase className="h-8 w-8 text-primary mr-3" />
            <h1 className="text-2xl font-bold text-card-foreground">
              Apply for {job?.job_title}
            </h1>
          </div>

          <div className="mb-8 space-y-6">
            <div className="bg-gradient-to-r from-primary/10 to-transparent p-6 rounded-lg shadow-sm">
              <h2 className="text-xl font-bold text-primary mb-4">Job Description</h2>
              <div className="prose prose-sm max-w-none text-card-foreground whitespace-pre-line">
                {job?.job_details}
              </div>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-secondary/20 p-5 rounded-lg shadow-sm">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="p-2 bg-primary/10 rounded-full">
                    <Code className="h-5 w-5 text-primary" />
                  </div>
                  <h3 className="font-semibold text-card-foreground">Required Skills</h3>
                </div>
                <p className="text-sm text-muted-foreground">{job?.skills_requirement}</p>
              </div>
              
              <div className="bg-secondary/20 p-5 rounded-lg shadow-sm">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="p-2 bg-primary/10 rounded-full">
                    <GraduationCap className="h-5 w-5 text-primary" />
                  </div>
                  <h3 className="font-semibold text-card-foreground">Education</h3>
                </div>
                <p className="text-sm text-muted-foreground">{job?.education_requirement}</p>
              </div>
              
              <div className="bg-secondary/20 p-5 rounded-lg shadow-sm">
                <div className="flex items-center space-x-2 mb-3">
                  <div className="p-2 bg-primary/10 rounded-full">
                    <Clock className="h-5 w-5 text-primary" />
                  </div>
                  <h3 className="font-semibold text-card-foreground">Experience</h3>
                </div>
                <p className="text-sm text-muted-foreground">{job?.experience_requirement}</p>
              </div>
              
              {job?.additional_requirements && (
                <div className="bg-secondary/20 p-5 rounded-lg shadow-sm">
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="p-2 bg-primary/10 rounded-full">
                      <Plus className="h-5 w-5 text-primary" />
                    </div>
                    <h3 className="font-semibold text-card-foreground">Additional Requirements</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">{job.additional_requirements}</p>
                </div>
              )}
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-card-foreground mb-1">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 rounded-lg border ${
                    formErrors.name ? 'border-red-500' : 'border-border'
                  } bg-background text-card-foreground focus:outline-none focus:ring-2 focus:ring-primary/50`}
                  placeholder="Enter your full name"
                />
                {formErrors.name && (
                  <p className="mt-1 text-sm text-red-500">{formErrors.name}</p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-card-foreground mb-1">
                  Email Address <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className={`w-full px-4 py-2 rounded-lg border ${
                    formErrors.email ? 'border-red-500' : 'border-border'
                  } bg-background text-card-foreground focus:outline-none focus:ring-2 focus:ring-primary/50`}
                  placeholder="Enter your email address"
                />
                {formErrors.email && (
                  <p className="mt-1 text-sm text-red-500">{formErrors.email}</p>
                )}
              </div>

              <div>
                <label htmlFor="resume" className="block text-sm font-medium text-card-foreground mb-1">
                  Resume (PDF) <span className="text-red-500">*</span>
                </label>
                <input
                  type="file"
                  id="resume"
                  name="resume"
                  onChange={handleFileChange}
                  accept="application/pdf"
                  className={`w-full px-4 py-2 rounded-lg border ${
                    formErrors.resume ? 'border-red-500' : 'border-border'
                  } bg-background text-card-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0 file:text-sm file:font-semibold
                  file:bg-primary/10 file:text-primary
                  hover:file:bg-primary/20`}
                />
                {formErrors.resume && (
                  <p className="mt-1 text-sm text-red-500">{formErrors.resume}</p>
                )}
                <p className="mt-1 text-xs text-muted-foreground">
                  Upload your resume in PDF format. Maximum file size: 5MB.
                </p>
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all duration-200 shadow-md flex items-center justify-center"
                  disabled={loadingSubmit}
                >
                  {loadingSubmit ? (
                    <>
                      <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                      Submitting...
                    </>
                  ) : (
                    'Submit Application'
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}