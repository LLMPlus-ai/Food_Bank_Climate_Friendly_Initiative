from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodbank.db'
db = SQLAlchemy(app)

class PersonaCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Text, nullable=False)
    barriers = db.Column(db.Text, nullable=False)
    cultural_context = db.Column(db.Text, nullable=False)
    socioeconomic_status = db.Column(db.String(100), nullable=False)
    dietary_preferences = db.Column(db.Text)
    household_size = db.Column(db.String(50))
    location = db.Column(db.String(100))
    climate_impact_concerns = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Guidebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    estimated_time = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    key_considerations = db.Column(db.Text)
    resources_needed = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ImplementationPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    guidebook_id = db.Column(db.Integer, db.ForeignKey('guidebook.id'), nullable=False)
    timeline = db.Column(db.String(100), nullable=False)
    stakeholders = db.Column(db.Text, nullable=False)
    resources = db.Column(db.Text, nullable=False)
    success_metrics = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    guidebook = db.relationship('Guidebook', backref=db.backref('implementation_plans', lazy=True))

class CommunityFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    implementation_plan_id = db.Column(db.Integer, db.ForeignKey('implementation_plan.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona_card.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    implementation_plan = db.relationship('ImplementationPlan', backref=db.backref('community_feedback', lazy=True))
    persona = db.relationship('PersonaCard', backref=db.backref('community_feedback', lazy=True))

class ClimateImpact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    implementation_plan_id = db.Column(db.Integer, db.ForeignKey('implementation_plan.id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    date_measured = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    implementation_plan = db.relationship('ImplementationPlan', backref=db.backref('climate_impacts', lazy=True))

# Sample data
SAMPLE_PERSONAS = [
    {
        'name': 'Sarah Chen',
        'profile': 'Single mother of two, working part-time in retail',
        'barriers': 'Limited time for meal planning, budget constraints, lack of cooking facilities',
        'cultural_context': 'Chinese-Canadian, traditional cooking methods',
        'socioeconomic_status': 'Low income, working poor',
        'dietary_preferences': 'Vegetarian, prefers traditional Chinese cooking methods',
        'household_size': '3 (2 children)',
        'location': 'Urban apartment',
        'climate_impact_concerns': 'Interested in reducing food waste, concerned about packaging'
    },
    {
        'name': 'Michael Rodriguez',
        'profile': 'Retired senior living alone',
        'barriers': 'Limited mobility, small portions needed, dietary restrictions',
        'cultural_context': 'Hispanic, traditional family cooking',
        'socioeconomic_status': 'Fixed income, pension',
        'dietary_preferences': 'Traditional Hispanic cuisine, low-sodium diet',
        'household_size': '1',
        'location': 'Suburban home',
        'climate_impact_concerns': 'Worries about food waste due to small portions'
    },
    {
        'name': 'Emma Thompson',
        'profile': 'Recent immigrant, working in hospitality',
        'barriers': 'Language barriers, unfamiliar with local food systems, irregular work hours',
        'cultural_context': 'British, adapting to Canadian food culture',
        'socioeconomic_status': 'New immigrant, entry-level job',
        'dietary_preferences': 'Flexible, learning local cuisine',
        'household_size': '2 (with partner)',
        'location': 'Downtown apartment',
        'climate_impact_concerns': 'Strong interest in sustainable practices from home country'
    },
    {
        'name': 'David Kumar',
        'profile': 'Student, part-time worker',
        'barriers': 'Limited budget, shared kitchen, irregular schedule',
        'cultural_context': 'South Asian, vegetarian',
        'socioeconomic_status': 'Student, part-time employment',
        'dietary_preferences': 'Strict vegetarian, spicy food preference',
        'household_size': '4 (shared student housing)',
        'location': 'University area',
        'climate_impact_concerns': 'Very concerned about climate change, active in environmental groups'
    }
]

SAMPLE_GUIDEBOOKS = [
    {
        'title': 'Working with a New Supplier/Partner',
        'description': 'Guide for establishing and maintaining relationships with new food suppliers while considering climate-friendly options',
        'steps': '1. Assess current suppliers\n2. Identify potential new partners\n3. Evaluate climate impact\n4. Develop partnership criteria\n5. Create implementation plan',
        'estimated_time': '2-3 months',
        'difficulty_level': 'Medium',
        'key_considerations': 'Supplier reliability, climate impact metrics, cost implications, community impact',
        'resources_needed': 'Supplier database, climate impact assessment tools, partnership agreements'
    },
    {
        'title': 'Evolving Your Food Bank\'s Offering/Services',
        'description': 'Guide for adapting services to meet unmet needs while maintaining climate-friendly practices',
        'steps': '1. Identify service gaps\n2. Analyze community needs\n3. Design new services\n4. Plan resource allocation\n5. Implement changes',
        'estimated_time': '3-6 months',
        'difficulty_level': 'High',
        'key_considerations': 'Community feedback, resource constraints, staff training needs',
        'resources_needed': 'Community survey tools, staff training materials, implementation timeline'
    },
    {
        'title': 'Establishing a New Food Bank',
        'description': 'Comprehensive guide for setting up a new food bank with climate-friendly practices from the start',
        'steps': '1. Community assessment\n2. Location selection\n3. Infrastructure planning\n4. Partner identification\n5. Launch preparation',
        'estimated_time': '6-12 months',
        'difficulty_level': 'High',
        'key_considerations': 'Community needs, climate impact, sustainable practices, partnerships',
        'resources_needed': 'Community assessment tools, facility planning templates, partnership agreements'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personas')
def personas():
    personas = PersonaCard.query.all()
    return render_template('personas.html', personas=personas)

@app.route('/guidebooks')
def guidebooks():
    guidebooks = Guidebook.query.all()
    return render_template('guidebooks.html', guidebooks=guidebooks)

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/api/personas')
def api_personas():
    personas = PersonaCard.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'profile': p.profile,
        'barriers': p.barriers,
        'cultural_context': p.cultural_context,
        'socioeconomic_status': p.socioeconomic_status,
        'dietary_preferences': p.dietary_preferences,
        'household_size': p.household_size,
        'location': p.location,
        'climate_impact_concerns': p.climate_impact_concerns
    } for p in personas])

@app.route('/api/implementation-plans', methods=['POST'])
def create_implementation_plan():
    data = request.json
    plan = ImplementationPlan(
        name=data['name'],
        guidebook_id=data['guidebook_id'],
        timeline=data['timeline'],
        stakeholders=data['stakeholders'],
        resources=data['resources'],
        success_metrics=data['success_metrics']
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'id': plan.id, 'message': 'Implementation plan created successfully'})

@app.route('/api/community-feedback', methods=['POST'])
def add_community_feedback():
    data = request.json
    feedback = CommunityFeedback(
        implementation_plan_id=data['implementation_plan_id'],
        persona_id=data['persona_id'],
        feedback_text=data['feedback_text'],
        rating=data['rating']
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'id': feedback.id, 'message': 'Feedback added successfully'})

@app.route('/api/climate-impact', methods=['POST'])
def add_climate_impact():
    data = request.json
    impact = ClimateImpact(
        implementation_plan_id=data['implementation_plan_id'],
        metric_name=data['metric_name'],
        metric_value=data['metric_value'],
        unit=data['unit'],
        date_measured=datetime.strptime(data['date_measured'], '%Y-%m-%d')
    )
    db.session.add(impact)
    db.session.commit()
    return jsonify({'id': impact.id, 'message': 'Climate impact data added successfully'})

def init_db():
    with app.app_context():
        # Drop all tables first to ensure clean slate
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Add sample data
        for persona in SAMPLE_PERSONAS:
            db.session.add(PersonaCard(**persona))
            
        for guidebook in SAMPLE_GUIDEBOOKS:
            db.session.add(Guidebook(**guidebook))
            
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 