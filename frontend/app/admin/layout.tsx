'use client';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // SQLite backend doesn't have authentication
  // Return the children directly
  return (
    <div className="min-h-screen">
      {children}
    </div>
  );
} 