'use client';

import { useEffect, useState } from 'react';
import { FileText, GitBranch, Percent, Star, ExternalLink } from 'lucide-react';
import { Briefcase } from 'lucide-react';
import { toast } from 'sonner';
import Link from 'next/link';
import { getCandidates, getDownloadUrl } from '@/lib/api';

interface Candidate {
  id: number;
  job_id: number;
  user_name: string;
  user_email: string;
  resume_url: string;
  parameter_score: number | null;
  job_similarity_score: number | null;
  github_score: number | null;
  total_score: number | null;
  match_percentage: number | null;
}

// ScoreCard component definition
const ScoreCard = ({ icon, title, score, colorClass }: { 
  icon: React.ReactNode; 
  title: string; 
  score: number | null; 
  colorClass: string 
}) => (
  <div className={`flex flex-col items-center justify-center bg-card rounded-xl p-6 ${colorClass} transition-all duration-300`}>
    {icon}
    <span className="text-sm font-medium mt-2">{title}</span>
    <span className="text-3xl font-bold mt-1">{typeof score === 'number' ? score.toFixed(1) : 'N/A'}</span>
  </div>
);

export default function AdminDashboard() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(true); // No Supabase auth, so we'll just set this to true

  useEffect(() => {
    async function fetchCandidates() {
      try {
        setLoading(true);
        const data = await getCandidates();
        console.log('Fetched data:', data);
        setCandidates(data || []);
        setLoading(false);
      } catch (error) {
        console.error('Error in fetchCandidates:', error);
        toast.error('Failed to fetch candidates');
        setLoading(false);
      }
    }

    fetchCandidates();
  }, []);

  const handleLogout = async () => {
    try {
      // Since we're not using Supabase auth anymore,
      // we'll just redirect to the home page
      window.location.href = '/';
      toast.success('Logged out successfully');
    } catch (error) {
      console.error('Error logging out:', error);
      toast.error('Failed to logout');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row gap-6 lg:gap-0 lg:justify-between items-start lg:items-center mb-8 sm:mb-12 bg-card rounded-2xl p-4 sm:p-6 shadow-lg border border-border/50">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              Admin Dashboard
            </h1>
            <p className="text-muted-foreground mt-2">View candidate applications</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start sm:items-center w-full lg:w-auto">
            <div className="bg-primary/10 rounded-2xl p-4 sm:p-6 shadow-inner w-full sm:w-auto">
              <p className="text-sm text-primary/70 font-medium">Total Applications</p>
              <p className="text-3xl sm:text-4xl font-bold text-primary mt-1">{candidates.length}</p>
            </div>
            <div className="flex flex-row sm:flex-col gap-3 w-full sm:w-auto">
              <Link
                href="/"
                className="flex-1 sm:flex-none bg-secondary/80 text-secondary-foreground px-4 sm:px-6 py-2.5 rounded-lg hover:bg-secondary/70 transition-all duration-200 flex items-center justify-center gap-2 shadow-md"
              >
                <Briefcase className="h-4 w-4" />
                <span>Home</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex-1 sm:flex-none bg-primary/90 text-primary-foreground px-4 sm:px-6 py-2.5 rounded-lg hover:bg-primary/80 transition-all duration-200 flex items-center justify-center gap-2 shadow-md"
              >
                <ExternalLink className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>

        {/* Candidates Grid */}
        <div className="grid gap-4 sm:gap-6">
          {candidates.map((candidate) => (
            <div
              key={candidate.id}
              className="bg-card rounded-xl sm:rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border border-border/50 hover:border-border group"
            >
              <div className="p-4 sm:p-8">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 lg:gap-8">
                  {/* Candidate Info Section */}
                  <div className="flex-1 min-w-0 lg:min-w-[300px]">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="bg-primary/10 rounded-2xl p-4 group-hover:bg-primary/20 transition-colors duration-300">
                        <span className="text-2xl font-bold text-primary">
                          {candidate.user_name.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div>
                        <h2 className="text-2xl font-semibold text-card-foreground">
                          {candidate.user_name}
                        </h2>
                        <p className="text-muted-foreground flex items-center gap-2 mt-1">
                          <Briefcase className="h-4 w-4" />
                          {candidate.user_email}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-sm bg-secondary/30 rounded-lg px-4 py-2 w-fit">
                      <Star className="h-4 w-4 text-primary" />
                      <span>Job ID: {candidate.job_id}</span>
                    </div>
                  </div>

                  {/* Scores Section */}
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 flex-1">
                    <ScoreCard
                      icon={<Star className="h-6 w-6" />}
                      title="Parameter Score"
                      score={candidate.parameter_score}
                      colorClass="bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20"
                    />
                    <ScoreCard
                      icon={<FileText className="h-6 w-6" />}
                      title="Job Match"
                      score={candidate.job_similarity_score}
                      colorClass="bg-green-500/10 text-green-500 hover:bg-green-500/20"
                    />
                    <ScoreCard
                      icon={<GitBranch className="h-6 w-6" />}
                      title="GitHub Score"
                      score={candidate.github_score}
                      colorClass="bg-purple-500/10 text-purple-500 hover:bg-purple-500/20"
                    />
                    <div className="flex flex-col items-center justify-center bg-primary/10 rounded-xl p-6 hover:bg-primary/20 transition-all duration-300">
                      <Percent className="h-6 w-6 text-primary mb-2" />
                      <span className="text-sm text-primary font-medium">Total Score</span>
                      <span className="text-3xl font-bold text-primary mt-1">
                        {typeof candidate.total_score === 'number' ? candidate.total_score.toFixed(1) : 'N/A'}
                      </span>
                    </div>
                  </div>

                  {/* Actions Section */}
                  <div className="flex flex-row lg:flex-col gap-2 lg:gap-3 min-w-0 lg:min-w-[160px]">
                    <div className="flex gap-2 flex-1 lg:flex-none">
                      <a
                        href={getDownloadUrl(candidate.resume_url)}
                        download={`${candidate.user_name}_resume.pdf`}
                        className="flex-1 inline-flex items-center justify-center gap-2 px-3 sm:px-4 py-2 sm:py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all duration-200 shadow-md hover:shadow-lg text-sm sm:text-base"
                      >
                        <FileText className="h-4 w-4 sm:h-5 sm:w-5" />
                        <span className="hidden sm:inline">Download Resume</span>
                      </a>
                    </div>
                    {/* Email Status Indicator */}
                    {candidate.total_score !== null && (
                      <div className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm ${
                        candidate.total_score >= 70 
                          ? 'bg-green-500/10 text-green-500' 
                          : 'bg-red-500/10 text-red-500'
                      }`}>
                        {candidate.total_score >= 70 
                          ? 'Interview Invitation Sent'
                          : 'Rejection Feedback Sent'
                        }
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}