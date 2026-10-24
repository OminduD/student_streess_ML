-- =============================================================================
-- Supabase Database Schema for Student Stress Predictor
-- =============================================================================
-- This script sets up the PostgreSQL database in Supabase:
-- 1. Creates the user_inputs table with data integrity constraints
-- 2. Creates query performance indexes
-- 3. Enables Row Level Security (RLS) with strict, secure access policies
-- =============================================================================

-- Enable UUID extension (usually enabled by default in Supabase)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Create the user_inputs table
CREATE TABLE IF NOT EXISTS public.user_inputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sleep_quality INTEGER NOT NULL CHECK (sleep_quality BETWEEN 1 AND 5),
    headaches_per_week INTEGER NOT NULL CHECK (headaches_per_week BETWEEN 0 AND 7),
    academic_performance INTEGER NOT NULL CHECK (academic_performance BETWEEN 1 AND 5),
    study_load INTEGER NOT NULL CHECK (study_load BETWEEN 1 AND 5),
    extracurricular_frequency INTEGER NOT NULL CHECK (extracurricular_frequency BETWEEN 0 AND 7),
    stress_level INTEGER CHECK (stress_level IS NULL OR stress_level BETWEEN 0 AND 5),
    predicted_stress INTEGER CHECK (predicted_stress IS NULL OR predicted_stress BETWEEN 0 AND 5),
    confidence NUMERIC(5, 2) CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100)),
    source VARCHAR(50) DEFAULT 'streamlit_app',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Comment on table and columns for schema documentation
COMMENT ON TABLE public.user_inputs IS 'Stores anonymous student stress survey inputs and model predictions.';
COMMENT ON COLUMN public.user_inputs.sleep_quality IS 'Rating of sleep quality (1=Very Poor to 5=Excellent)';
COMMENT ON COLUMN public.user_inputs.headaches_per_week IS 'Frequency of headaches per week (0-7)';
COMMENT ON COLUMN public.user_inputs.academic_performance IS 'Rating of academic performance (1=Poor to 5=Excellent)';
COMMENT ON COLUMN public.user_inputs.study_load IS 'Perceived study workload (1=Very Light to 5=Overwhelming)';
COMMENT ON COLUMN public.user_inputs.extracurricular_frequency IS 'Days per week participating in extracurriculars (0-7)';
COMMENT ON COLUMN public.user_inputs.stress_level IS 'User-reported actual stress level (0-5)';

-- 2. Create performance indexes
CREATE INDEX IF NOT EXISTS idx_user_inputs_timestamp 
    ON public.user_inputs (timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_user_inputs_stress_level 
    ON public.user_inputs (stress_level) 
    WHERE stress_level IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_user_inputs_source 
    ON public.user_inputs (source);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================================================

-- Enable Row Level Security on the table
ALTER TABLE public.user_inputs ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (idempotent setup)
DROP POLICY IF EXISTS "Allow anonymous insert with validated constraints" ON public.user_inputs;
DROP POLICY IF EXISTS "Allow anonymous read access" ON public.user_inputs;
DROP POLICY IF EXISTS "Prevent public update" ON public.user_inputs;
DROP POLICY IF EXISTS "Prevent public delete" ON public.user_inputs;

-- Policy 1: Allow anyone (anon key) to INSERT new student assessments
-- Strict WITH CHECK ensures all values adhere to acceptable boundary ranges
CREATE POLICY "Allow anonymous insert with validated constraints" 
    ON public.user_inputs
    FOR INSERT 
    TO anon, authenticated
    WITH CHECK (
        sleep_quality BETWEEN 1 AND 5
        AND headaches_per_week BETWEEN 0 AND 7
        AND academic_performance BETWEEN 1 AND 5
        AND study_load BETWEEN 1 AND 5
        AND extracurricular_frequency BETWEEN 0 AND 7
        AND (stress_level IS NULL OR stress_level BETWEEN 0 AND 5)
    );

-- Policy 2: Allow read access for public dashboard statistics
CREATE POLICY "Allow anonymous read access" 
    ON public.user_inputs
    FOR SELECT 
    TO anon, authenticated
    USING (true);

-- Note: No UPDATE or DELETE policies are granted to 'anon'.
-- By default in Postgres RLS, any operation without an explicit policy is DENIED.
-- This ensures malicious actors cannot tamper with or delete submitted student data.
