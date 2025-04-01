-- Create persona_cards table
CREATE TABLE IF NOT EXISTS public.persona_cards (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    occupation TEXT,
    background TEXT,
    challenges TEXT,
    dietary_preferences TEXT,
    household_size INTEGER,
    location TEXT,
    climate_impact_concerns TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create guidebooks table
CREATE TABLE IF NOT EXISTS public.guidebooks (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    steps JSONB,
    estimated_time TEXT,
    difficulty_level TEXT,
    key_considerations TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create implementation_plans table
CREATE TABLE IF NOT EXISTS public.implementation_plans (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    steps JSONB,
    timeline TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create community_feedback table
CREATE TABLE IF NOT EXISTS public.community_feedback (
    id BIGSERIAL PRIMARY KEY,
    feedback_type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create climate_impacts table
CREATE TABLE IF NOT EXISTS public.climate_impacts (
    id BIGSERIAL PRIMARY KEY,
    impact_type TEXT NOT NULL,
    description TEXT,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Set up Row Level Security (RLS)
ALTER TABLE public.persona_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.guidebooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.implementation_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.climate_impacts ENABLE ROW LEVEL SECURITY;

-- Create policies for public access
CREATE POLICY "Allow public read access" ON public.persona_cards
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON public.guidebooks
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON public.implementation_plans
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON public.community_feedback
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON public.climate_impacts
    FOR SELECT USING (true);

-- Create policies for insert access
CREATE POLICY "Allow public insert access" ON public.implementation_plans
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert access" ON public.community_feedback
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert access" ON public.climate_impacts
    FOR INSERT WITH CHECK (true); 