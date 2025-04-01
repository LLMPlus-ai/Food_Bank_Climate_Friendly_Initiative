-- Create persona_cards table
CREATE TABLE IF NOT EXISTS persona_cards (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    occupation VARCHAR(100),
    background TEXT,
    challenges TEXT,
    dietary_preferences VARCHAR(100),
    household_size INTEGER,
    location VARCHAR(100),
    climate_impact_concerns TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create guidebooks table
CREATE TABLE IF NOT EXISTS guidebooks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    steps TEXT,
    estimated_time VARCHAR(50),
    difficulty_level VARCHAR(20),
    key_considerations TEXT,
    resources_needed TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create implementation_plans table
CREATE TABLE IF NOT EXISTS implementation_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    guidebook_id INTEGER REFERENCES guidebooks(id),
    timeline VARCHAR(100),
    stakeholders TEXT,
    resources TEXT,
    success_metrics TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create community_feedback table
CREATE TABLE IF NOT EXISTS community_feedback (
    id SERIAL PRIMARY KEY,
    implementation_plan_id INTEGER REFERENCES implementation_plans(id),
    feedback_text TEXT,
    rating INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create climate_impacts table
CREATE TABLE IF NOT EXISTS climate_impacts (
    id SERIAL PRIMARY KEY,
    implementation_plan_id INTEGER REFERENCES implementation_plans(id),
    metric_name VARCHAR(100),
    value FLOAT,
    unit VARCHAR(20),
    date_measured TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_persona_cards_updated_at
    BEFORE UPDATE ON persona_cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_guidebooks_updated_at
    BEFORE UPDATE ON guidebooks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_implementation_plans_updated_at
    BEFORE UPDATE ON implementation_plans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 