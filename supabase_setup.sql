-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist
DROP TABLE IF EXISTS public.climate_impacts CASCADE;
DROP TABLE IF EXISTS public.community_feedback CASCADE;
DROP TABLE IF EXISTS public.implementation_plans CASCADE;
DROP TABLE IF EXISTS public.guidebooks CASCADE;
DROP TABLE IF EXISTS public.persona_cards CASCADE;

-- Create persona_cards table
CREATE TABLE public.persona_cards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    background TEXT NOT NULL,
    challenges TEXT NOT NULL,
    dietary_preferences VARCHAR(100),
    household_size INTEGER NOT NULL,
    location VARCHAR(50) NOT NULL,
    climate_impact_concerns TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create guidebooks table
CREATE TABLE public.guidebooks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    steps JSONB NOT NULL,
    estimated_time VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20) NOT NULL,
    key_considerations TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create implementation_plans table
CREATE TABLE public.implementation_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    steps JSONB NOT NULL,
    timeline JSONB NOT NULL,
    resources_needed JSONB NOT NULL,
    success_metrics JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'draft' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create community_feedback table
CREATE TABLE public.community_feedback (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    persona_id UUID REFERENCES public.persona_cards(id),
    feedback_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create climate_impacts table
CREATE TABLE public.climate_impacts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    implementation_plan_id UUID REFERENCES public.implementation_plans(id),
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL NOT NULL,
    unit VARCHAR(50) NOT NULL,
    measurement_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.persona_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.guidebooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.implementation_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.climate_impacts ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public read access on persona_cards" ON public.persona_cards;
DROP POLICY IF EXISTS "Allow public read access on guidebooks" ON public.guidebooks;
DROP POLICY IF EXISTS "Allow public read access on implementation_plans" ON public.implementation_plans;
DROP POLICY IF EXISTS "Allow public read access on community_feedback" ON public.community_feedback;
DROP POLICY IF EXISTS "Allow public read access on climate_impacts" ON public.climate_impacts;
DROP POLICY IF EXISTS "Allow public insert access on implementation_plans" ON public.implementation_plans;
DROP POLICY IF EXISTS "Allow public insert access on community_feedback" ON public.community_feedback;
DROP POLICY IF EXISTS "Allow public insert access on climate_impacts" ON public.climate_impacts;

-- Create policies for public read access
CREATE POLICY "Allow public read access on persona_cards" ON public.persona_cards
    FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access on guidebooks" ON public.guidebooks
    FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access on implementation_plans" ON public.implementation_plans
    FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access on community_feedback" ON public.community_feedback
    FOR SELECT TO public USING (true);

CREATE POLICY "Allow public read access on climate_impacts" ON public.climate_impacts
    FOR SELECT TO public USING (true);

-- Create policies for public insert access
CREATE POLICY "Allow public insert access on implementation_plans" ON public.implementation_plans
    FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Allow public insert access on community_feedback" ON public.community_feedback
    FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Allow public insert access on climate_impacts" ON public.climate_impacts
    FOR INSERT TO public WITH CHECK (true);

-- Insert sample data into persona_cards
INSERT INTO public.persona_cards (name, age, occupation, background, challenges, dietary_preferences, household_size, location, climate_impact_concerns)
VALUES
    ('Sarah Johnson', 35, 'Single Mother', 'Works two part-time jobs to support her family. Previously worked in retail management but had to reduce hours to care for her children.', 'Limited time for meal preparation, tight budget, needs quick and nutritious meals for her children', 'Vegetarian', 3, 'Urban', 'Interested in reducing food waste and learning about sustainable food practices'),
    ('Emma Thompson', 42, 'Food Bank Manager', '10 years experience in food bank operations. Previously worked in non-profit management and community development.', 'Balancing nutritional needs with available donations, managing volunteer schedules, coordinating with local farms', 'No restrictions', 4, 'Suburban', 'Focused on sustainable food sourcing and reducing carbon footprint of operations'),
    ('Michael Chen', 28, 'Environmental Activist', 'Recent graduate in Environmental Science. Works with local community gardens and food rescue organizations.', 'Limited funding for projects, coordinating with multiple stakeholders, educating community members', 'Vegan', 2, 'Urban', 'Passionate about reducing food waste and promoting sustainable food systems'),
    ('Lisa Rodriguez', 45, 'Community Organizer', '15 years experience in community development. Founded a local food sharing network.', 'Building trust in the community, managing logistics of food distribution, coordinating volunteers', 'Flexitarian', 5, 'Urban', 'Committed to reducing food waste and building resilient local food systems'),
    ('David Wilson', 38, 'Local Farmer', 'Owns a small organic farm. Supplies produce to local food banks and restaurants.', 'Weather challenges, managing crop yields, balancing commercial and donation needs', 'No restrictions', 4, 'Rural', 'Focused on sustainable farming practices and reducing post-harvest losses');

-- Insert sample data into guidebooks
INSERT INTO public.guidebooks (title, description, steps, estimated_time, difficulty_level, key_considerations, resources_needed)
VALUES
    ('Reducing Food Waste in Food Banks', 'A comprehensive guide to minimizing food waste in food bank operations through improved inventory management and storage practices.', 
    '["Audit current waste levels", "Implement inventory tracking system", "Optimize storage conditions", "Establish donation guidelines", "Train staff and volunteers", "Set up monitoring systems", "Create waste reduction goals"]',
    '3-6 months', 'Medium', 'Storage capacity, volunteer training needs, refrigeration requirements, inventory management system', 
    'Inventory management system, storage containers, training materials, temperature monitoring devices, waste tracking forms'),
    
    ('Community Engagement for Food Waste Reduction', 'A guide to engaging local communities in food waste reduction initiatives through education and participation.',
    '["Identify community stakeholders", "Develop educational materials", "Plan community events", "Create volunteer programs", "Establish feedback mechanisms", "Monitor participation rates"]',
    '4-8 months', 'Medium', 'Community demographics, cultural considerations, language barriers, accessibility needs',
    'Educational materials, event planning resources, volunteer management system, feedback collection tools'),
    
    ('Sustainable Food Storage Solutions', 'Best practices for storing different types of food to maximize shelf life and reduce waste.',
    '["Assess current storage facilities", "Implement temperature controls", "Organize storage areas", "Create storage guidelines", "Train staff on procedures", "Monitor effectiveness"]',
    '2-4 months', 'Easy', 'Temperature requirements, humidity levels, space utilization, pest control',
    'Temperature monitoring devices, storage containers, shelving units, pest control supplies');

-- Insert sample data into implementation_plans
INSERT INTO public.implementation_plans (title, description, steps, timeline, resources_needed, success_metrics, status)
VALUES
    ('Food Bank Waste Reduction Initiative', 'A comprehensive plan to reduce food waste in our food bank operations by 30% within 6 months.',
    '["Conduct waste audit", "Implement inventory system", "Train staff", "Monitor progress", "Adjust procedures"]',
    '{"Phase 1": "Month 1-2", "Phase 2": "Month 3-4", "Phase 3": "Month 5-6"}',
    '{"Equipment": ["Inventory software", "Storage containers"], "Staff": ["Training materials", "Monitoring tools"], "Facilities": ["Storage space", "Refrigeration"]}',
    '{"Waste Reduction": "30%", "Staff Training": "100%", "System Implementation": "Complete"}',
    'in_progress'),
    
    ('Community Education Program', 'A program to educate local communities about food waste reduction and sustainable practices.',
    '["Develop materials", "Plan workshops", "Recruit volunteers", "Conduct sessions", "Gather feedback"]',
    '{"Planning": "Month 1", "Implementation": "Month 2-4", "Evaluation": "Month 5"}',
    '{"Materials": ["Educational content", "Workshop supplies"], "Staff": ["Trainers", "Volunteers"], "Venues": ["Community centers", "Meeting spaces"]}',
    '{"Participant Satisfaction": "90%", "Knowledge Increase": "80%", "Behavior Change": "60%"}',
    'draft');

-- Insert sample data into community_feedback
INSERT INTO public.community_feedback (persona_id, feedback_type, content, rating)
VALUES
    ((SELECT id FROM public.persona_cards WHERE name = 'Sarah Johnson'), 'suggestion', 'Would love to see more quick and easy recipes for busy parents', 4),
    ((SELECT id FROM public.persona_cards WHERE name = 'Emma Thompson'), 'compliment', 'The new inventory system has significantly reduced our waste', 5),
    ((SELECT id FROM public.persona_cards WHERE name = 'Michael Chen'), 'suggestion', 'Consider adding more information about environmental impact', 4),
    ((SELECT id FROM public.persona_cards WHERE name = 'Lisa Rodriguez'), 'compliment', 'The community engagement program has been very effective', 5),
    ((SELECT id FROM public.persona_cards WHERE name = 'David Wilson'), 'suggestion', 'Could use more guidance on handling seasonal produce', 3);

-- Insert sample data into climate_impacts
INSERT INTO public.climate_impacts (implementation_plan_id, metric_name, value, unit, measurement_date)
VALUES
    ((SELECT id FROM public.implementation_plans WHERE title = 'Food Bank Waste Reduction Initiative'), 'Food Waste Reduction', 25.5, 'percentage', CURRENT_DATE),
    ((SELECT id FROM public.implementation_plans WHERE title = 'Food Bank Waste Reduction Initiative'), 'Carbon Emissions Saved', 1500, 'kg CO2', CURRENT_DATE),
    ((SELECT id FROM public.implementation_plans WHERE title = 'Community Education Program'), 'Participants Trained', 250, 'people', CURRENT_DATE),
    ((SELECT id FROM public.implementation_plans WHERE title = 'Community Education Program'), 'Knowledge Retention Rate', 85, 'percentage', CURRENT_DATE); 