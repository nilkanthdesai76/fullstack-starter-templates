import { createClient } from "@supabase/supabase-js";

/**
 * Creates and initializes a typed Supabase client singleton.
 *
 * @param {string} supabaseUrl
 * @param {string} supabaseAnonKey
 */
export function initSupabase(supabaseUrl, supabaseAnonKey) {
  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error("Missing SUPABASE_URL or SUPABASE_ANON_KEY");
  }
  return createClient(supabaseUrl, supabaseAnonKey);
}

/**
 * Authentication helper utilities
 */
export class SupabaseAuthHelper {
  constructor(client) {
    this.client = client;
  }

  async signUp(email, password) {
    const { data, error } = await this.client.auth.signUp({ email, password });
    if (error) throw error;
    return data;
  }

  async signIn(email, password) {
    const { data, error } = await this.client.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data;
  }

  async signOut() {
    const { error } = await this.client.auth.signOut();
    if (error) throw error;
  }

  async getSession() {
    const { data, error } = await this.client.auth.getSession();
    if (error) throw error;
    return data.session;
  }
}

/**
 * Storage upload and signed URL helper
 */
export class SupabaseStorageHelper {
  constructor(client, defaultBucket = "documents") {
    this.client = client;
    this.bucket = defaultBucket;
  }

  async uploadFile(path, file, upsert = false) {
    const { data, error } = await this.client.storage
      .from(this.bucket)
      .upload(path, file, { upsert });
    if (error) throw error;
    return data;
  }

  async getPublicUrl(path) {
    const { data } = this.client.storage.from(this.bucket).getPublicUrl(path);
    return data.publicUrl;
  }
}
