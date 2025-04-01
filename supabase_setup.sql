-- Create tables
CREATE TABLE IF NOT EXISTS public.persona_cards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    occupation TEXT,
    background TEXT,
    challenges TEXT,
    dietary_preferences TEXT,
    household_size INTEGER,
    location TEXT,
    climate_impact_concerns TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.guidebooks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    steps JSONB,
    estimated_time TEXT,
    difficulty_level TEXT,
    key_considerations TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.implementation_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    steps JSONB,
    timeline TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.community_feedback (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    feedback_type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.climate_impacts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    impact_type TEXT NOT NULL,
    description TEXT,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.persona_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.guidebooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.implementation_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.climate_impacts ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Allow public read access on persona_cards"
    ON public.persona_cards FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow public read access on guidebooks"
    ON public.guidebooks FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow public read access on implementation_plans"
    ON public.implementation_plans FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow public read access on community_feedback"
    ON public.community_feedback FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow public read access on climate_impacts"
    ON public.climate_impacts FOR SELECT
    TO public
    USING (true);

-- Create policies for public insert access
CREATE POLICY "Allow public insert access on implementation_plans"
    ON public.implementation_plans FOR INSERT
    TO public
    WITH CHECK (true);

CREATE POLICY "Allow public insert access on community_feedback"
    ON public.community_feedback FOR INSERT
    TO public
    WITH CHECK (true);

CREATE POLICY "Allow public insert access on climate_impacts"
    ON public.climate_impacts FOR INSERT
    TO public
    WITH CHECK (true); 