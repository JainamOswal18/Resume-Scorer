'use client';

import { useEffect, useState } from 'react';
import { Briefcase, ChevronRight, Code, GraduationCap, Clock, Search, Building } from 'lucide-react';
import Link from 'next/link';
import { getJobs } from '@/lib/api';

interface JobDetails {
  job_id: number;
  job_title: string;
  job_details: string;
  skills_requirement: string;
  education_requirement: string;
  experience_requirement: string;
  additional_requirements: string | null;
  created_at: string;
}

export default function Home() {
  const [jobs, setJobs] = useState<JobDetails[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchJobs() {
      try {
        const data = await getJobs();
        setJobs(data || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching jobs:', error);
        setLoading(false);
      }
    }

    fetchJobs();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-secondary/20 to-background">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background">
      {/* Header with Admin Link */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-end">
          <Link
            href="/admin"
            className="inline-flex items-center px-4 py-2 bg-secondary/80 text-secondary-foreground rounded-lg hover:bg-secondary/70 transition-all duration-200 shadow-md"
          >
            <Building className="mr-2 h-4 w-4" />
            Admin Dashboard
          </Link>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-16">
        <div className="text-center max-w-3xl mx-auto mb-8 sm:mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent mb-4 sm:mb-6">
            YourHR
          </h1>
          <p className="text-lg sm:text-xl text-muted-foreground leading-relaxed px-4">
            Our AI-powered resume analysis tool matches your skills and experience to our open positions.
            {jobs.length === 1 
              ? " Explore our current opening and take the next step in your career journey."
              : ` Explore our ${jobs.length} open positions and take the next step in your career journey.`
            }
          </p>
        </div>

        {/* Jobs Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto px-4">
          {jobs.map((job) => (
            <div 
              key={job.job_id}
              className="bg-card rounded-lg shadow-lg border border-border/50 hover:border-primary/30 hover:shadow-xl transition-all duration-300 overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="bg-primary/10 p-3 rounded-lg">
                    <Briefcase className="h-6 w-6 text-primary" />
                  </div>
                  <h2 className="text-xl font-bold text-card-foreground">{job.job_title}</h2>
                </div>
                
                <p className="text-muted-foreground mb-6 line-clamp-3">
                  {job.job_details}
                </p>
                
                <div className="space-y-3 mb-6">
                  <div className="flex items-center gap-2 text-sm">
                    <Code className="h-4 w-4 text-primary/70" />
                    <span className="text-muted-foreground line-clamp-1">
                      {job.skills_requirement}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm">
                    <GraduationCap className="h-4 w-4 text-primary/70" />
                    <span className="text-muted-foreground line-clamp-1">
                      {job.education_requirement}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="h-4 w-4 text-primary/70" />
                    <span className="text-muted-foreground line-clamp-1">
                      {job.experience_requirement}
                    </span>
                  </div>
                </div>
                
                <Link 
                  href={`/apply/${job.job_id}`}
                  className="flex items-center justify-center gap-2 w-full py-3 bg-primary/10 text-primary hover:bg-primary/20 rounded-md transition-colors duration-200"
                >
                  <span className="font-medium">Apply Now</span>
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}