-- Migration: 20261024000000_create_user_inputs.sql
-- Description: Sets up user_inputs table, indexes, and Row Level Security (RLS) policies

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Create table
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

-- 2. Indexes
CREATE INDEX IF NOT EXISTS idx_user_inputs_timestamp 
    ON public.user_inputs (timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_user_inputs_stress_level 
    ON public.user_inputs (stress_level) 
    WHERE stress_level IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_user_inputs_source 
    ON public.user_inputs (source);

-- 3. Row Level Security (RLS)
ALTER TABLE public.user_inputs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow anonymous insert with validated constraints" ON public.user_inputs;
DROP POLICY IF EXISTS "Allow anonymous read access" ON public.user_inputs;

-- Allow insert with strict input range validation
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

-- Allow select for aggregate telemetry and dashboards
CREATE POLICY "Allow anonymous read access" 
    ON public.user_inputs
    FOR SELECT 
    TO anon, authenticated
    USING (true);
