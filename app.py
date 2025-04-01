from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client
import logging
import json
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Supabase client
def get_supabase_client():
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        return create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        raise

# Create Supabase client
try:
    supabase = get_supabase_client()
    logger.info("Successfully initialized Supabase client")
except Exception as e:
    logger.error(f"Failed to create Supabase client: {str(e)}")
    raise

# Error handling
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}')
    return render_template('error.html', error=str(error)), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=str(error)), 404

def check_table_exists(table_name):
    try:
        # Try to select a single row from the table
        response = supabase.table(table_name).select('*').limit(1).execute()
        return True
    except Exception as e:
        if 'relation' in str(e).lower() and 'does not exist' in str(e).lower():
            return False
        raise

def init_database():
    """Initialize the database with required tables and sample data."""
    try:
        # Read the SQL setup file
        with open('supabase_setup.sql', 'r') as file:
            sql_commands = file.read()

        # Execute the SQL commands
        supabase.rpc('exec_sql', {'sql': sql_commands}).execute()
        logger.info("Database tables created successfully")

        # Initialize sample data
        init_sample_data()
        logger.info("Sample data initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def init_sample_data():
    try:
        # Check if data exists in Supabase
        personas_response = supabase.table('persona_cards').select('count').execute()
        if not personas_response.data or personas_response.data[0]['count'] == 0:
            # Add sample personas
            personas_data = [
                {
                    "name": "Sarah Johnson",
                    "age": 35,
                    "occupation": "Single Mother",
                    "background": "Works two part-time jobs to support her family",
                    "challenges": "Limited time for meal preparation, tight budget",
                    "dietary_preferences": "Vegetarian",
                    "household_size": 3,
                    "location": "Urban",
                    "climate_impact_concerns": "Interested in reducing food waste",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                },
                {
                    "name": "Emma Thompson",
                    "age": 42,
                    "occupation": "Food Bank Manager",
                    "background": "10 years experience in food bank operations",
                    "challenges": "Balancing nutritional needs with available donations",
                    "dietary_preferences": "No restrictions",
                    "household_size": 4,
                    "location": "Suburban",
                    "climate_impact_concerns": "Focused on sustainable food sourcing",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            ]
            supabase.table('persona_cards').insert(personas_data).execute()
            logger.info("Sample personas added to Supabase")

        guidebooks_response = supabase.table('guidebooks').select('count').execute()
        if not guidebooks_response.data or guidebooks_response.data[0]['count'] == 0:
            # Add sample guidebooks
            guidebooks_data = [
                {
                    "title": "Reducing Food Waste in Food Banks",
                    "description": "A comprehensive guide to minimizing food waste in food bank operations",
                    "steps": json.dumps([
                        "Audit current waste levels",
                        "Implement inventory tracking",
                        "Optimize storage conditions",
                        "Establish donation guidelines",
                        "Train staff and volunteers"
                    ]),
                    "estimated_time": "3-6 months",
                    "difficulty_level": "Medium",
                    "key_considerations": "Storage capacity, volunteer training needs",
                    "resources_needed": "Inventory management system, storage containers, training materials",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            ]
            supabase.table('guidebooks').insert(guidebooks_data).execute()
            logger.info("Sample guidebooks added to Supabase")
        
        logger.info("Sample data initialization completed successfully!")
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        raise

# Routes
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/personas')
def personas():
    try:
        if not check_table_exists('persona_cards'):
            init_database()
        response = supabase.table('persona_cards').select('*').execute()
        return render_template('personas.html', personas=response.data)
    except Exception as e:
        logger.error(f"Error in personas route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/personas')
def get_personas():
    try:
        if not check_table_exists('persona_cards'):
            init_database()
        response = supabase.table('persona_cards').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error in get_personas route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/guidebooks')
def guidebooks():
    try:
        if not check_table_exists('guidebooks'):
            init_database()
        response = supabase.table('guidebooks').select('*').execute()
        return render_template('guidebooks.html', guidebooks=response.data)
    except Exception as e:
        logger.error(f"Error in guidebooks route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/process')
def process():
    try:
        return render_template('process.html')
    except Exception as e:
        logger.error(f"Error in process route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

# API routes
@app.route('/api/implementation-plans', methods=['POST'])
def create_implementation_plan():
    try:
        if not check_table_exists('implementation_plans'):
            init_database()
        data = request.json
        data['created_at'] = datetime.utcnow().isoformat()
        data['updated_at'] = datetime.utcnow().isoformat()
        response = supabase.table('implementation_plans').insert(data).execute()
        return jsonify(response.data[0])
    except Exception as e:
        logger.error(f"Error creating implementation plan: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/community-feedback', methods=['POST'])
def add_community_feedback():
    try:
        if not check_table_exists('community_feedback'):
            init_database()
        data = request.json
        data['created_at'] = datetime.utcnow().isoformat()
        response = supabase.table('community_feedback').insert(data).execute()
        return jsonify(response.data[0])
    except Exception as e:
        logger.error(f"Error adding feedback: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/climate-impact', methods=['POST'])
def add_climate_impact():
    try:
        if not check_table_exists('climate_impacts'):
            init_database()
        data = request.json
        data['created_at'] = datetime.utcnow().isoformat()
        response = supabase.table('climate_impacts').insert(data).execute()
        return jsonify(response.data[0])
    except Exception as e:
        logger.error(f"Error adding climate impact: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Initialize database if needed
@app.before_first_request
def setup_database():
    try:
        if not check_table_exists('persona_cards'):
            init_database()
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        print(f"Error during database initialization: {str(e)}", file=sys.stderr)

# This is the entry point for Vercel
app = app 