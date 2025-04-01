from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-development')

# Use SQLite for development and in-memory SQLite for production
if os.environ.get('VERCEL_ENV') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True  # Show errors in production
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodbank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PersonaCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(100))
    background = db.Column(db.Text)
    challenges = db.Column(db.Text)
    dietary_preferences = db.Column(db.String(100))
    household_size = db.Column(db.Integer)
    location = db.Column(db.String(100))
    climate_impact_concerns = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Guidebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(db.Text)
    estimated_time = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    key_considerations = db.Column(db.Text)
    resources_needed = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ImplementationPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    guidebook_id = db.Column(db.Integer, db.ForeignKey('guidebook.id'))
    timeline = db.Column(db.String(100))
    stakeholders = db.Column(db.Text)
    resources = db.Column(db.Text)
    success_metrics = db.Column(db.Text)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CommunityFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    implementation_plan_id = db.Column(db.Integer, db.ForeignKey('implementation_plan.id'))
    feedback_text = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClimateImpact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    implementation_plan_id = db.Column(db.Integer, db.ForeignKey('implementation_plan.id'))
    metric_name = db.Column(db.String(100))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    date_measured = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Error handling
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html', error=error), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=error), 404

def init_db():
    try:
        with app.app_context():
            # Drop all tables
            db.drop_all()
            # Create all tables
            db.create_all()
            
            # Add sample personas
            personas = [
                PersonaCard(
                    name="Sarah Johnson",
                    age=35,
                    occupation="Single Mother",
                    background="Works two part-time jobs to support her family",
                    challenges="Limited time for meal preparation, tight budget",
                    dietary_preferences="Vegetarian",
                    household_size=3,
                    location="Urban",
                    climate_impact_concerns="Interested in reducing food waste"
                ),
                PersonaCard(
                    name="Emma Thompson",
                    age=42,
                    occupation="Food Bank Manager",
                    background="10 years experience in food bank operations",
                    challenges="Balancing nutritional needs with available donations",
                    dietary_preferences="No restrictions",
                    household_size=4,
                    location="Suburban",
                    climate_impact_concerns="Focused on sustainable food sourcing"
                ),
                PersonaCard(
                    name="David Kumar",
                    age=28,
                    occupation="Graduate Student",
                    background="International student on limited budget",
                    challenges="Dietary restrictions, unfamiliar with local food system",
                    dietary_preferences="Vegan",
                    household_size=1,
                    location="Urban",
                    climate_impact_concerns="Passionate about reducing carbon footprint"
                )
            ]
            
            # Add sample guidebooks
            guidebooks = [
                Guidebook(
                    title="Reducing Food Waste in Food Banks",
                    description="A comprehensive guide to minimizing food waste in food bank operations",
                    steps="1. Audit current waste levels\n2. Implement inventory tracking\n3. Optimize storage conditions\n4. Establish donation guidelines\n5. Train staff and volunteers",
                    estimated_time="3-6 months",
                    difficulty_level="Medium",
                    key_considerations="Storage capacity, volunteer training needs",
                    resources_needed="Inventory management system, storage containers, training materials"
                ),
                Guidebook(
                    title="Establishing a New Food Bank",
                    description="Step-by-step guide to setting up a climate-friendly food bank",
                    steps="1. Community needs assessment\n2. Location selection\n3. Equipment procurement\n4. Volunteer recruitment\n5. Partnership development",
                    estimated_time="6-12 months",
                    difficulty_level="High",
                    key_considerations="Location accessibility, storage requirements",
                    resources_needed="Facility, refrigeration units, transport vehicles"
                )
            ]
            
            db.session.add_all(personas)
            db.session.add_all(guidebooks)
            db.session.commit()
            app.logger.info("Database initialized successfully!")
    except Exception as e:
        app.logger.error(f"Error initializing database: {str(e)}")
        raise

# Routes
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error in index route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/personas')
def personas():
    try:
        personas = PersonaCard.query.all()
        return render_template('personas.html', personas=personas)
    except Exception as e:
        app.logger.error(f"Error in personas route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/personas')
def get_personas():
    try:
        personas = PersonaCard.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'occupation': p.occupation,
            'background': p.background,
            'challenges': p.challenges,
            'dietary_preferences': p.dietary_preferences,
            'household_size': p.household_size,
            'location': p.location,
            'climate_impact_concerns': p.climate_impact_concerns
        } for p in personas])
    except Exception as e:
        app.logger.error(f"Error in get_personas route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/guidebooks')
def guidebooks():
    try:
        guidebooks = Guidebook.query.all()
        return render_template('guidebooks.html', guidebooks=guidebooks)
    except Exception as e:
        app.logger.error(f"Error in guidebooks route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/process')
def process():
    try:
        return render_template('process.html')
    except Exception as e:
        app.logger.error(f"Error in process route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

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
        value=data['value'],
        unit=data['unit'],
        date_measured=datetime.strptime(data['date_measured'], '%Y-%m-%d')
    )
    db.session.add(impact)
    db.session.commit()
    return jsonify({'id': impact.id, 'message': 'Climate impact data added successfully'})

# Initialize database
with app.app_context():
    try:
        db.create_all()
        # Only add sample data if tables are empty
        if not PersonaCard.query.first() and not Guidebook.query.first():
            init_db()
    except Exception as e:
        app.logger.error(f"Error during database initialization: {str(e)}")
        print(f"Error during database initialization: {str(e)}", file=sys.stderr)

if __name__ == '__main__':
    app.run(debug=True) 