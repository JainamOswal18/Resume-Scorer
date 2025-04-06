// This is a dummy/mock file to satisfy imports
// We're transitioning away from Supabase to SQLite,
// but some components might still import this file

const mockSupabase = {
  auth: {
    getSession: async () => ({ data: { session: null } }),
    onAuthStateChange: () => ({ 
      data: { 
        subscription: { unsubscribe: () => {} } 
      } 
    }),
    signInWithPassword: async () => ({ error: null }),
    signOut: async () => ({ error: null })
  },
  from: () => ({
    select: () => ({
      eq: () => ({
        single: async () => ({ data: null }),
        order: () => ({
          limit: () => ({
            data: []
          })
        }),
      }),
    }),
  }),
  storage: {
    from: () => ({
      upload: async () => ({ data: { path: '' }, error: null }),
      getPublicUrl: () => ({ data: { publicUrl: '' } }),
    }),
  },
};

export default mockSupabase; 