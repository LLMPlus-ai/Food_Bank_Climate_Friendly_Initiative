from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client
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
supabase: Client = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)
logger.info("Successfully initialized Supabase client")

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
        response = supabase.table(table_name).select("*").limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"Error checking table {table_name}: {str(e)}")
        return False

def init_database():
    """Initialize the database with required tables and sample data."""
    try:
        # Read and execute SQL setup file
        with open('supabase_setup.sql', 'r') as file:
            sql_commands = file.read()
            # Execute SQL commands in Supabase
            supabase.rpc('exec_sql', {'sql': sql_commands}).execute()
        logger.info("Database initialized successfully")

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
        # Check if persona_cards table exists
        if not check_table_exists('persona_cards'):
            init_database()
        
        # Get sample persona for the homepage
        response = supabase.table('persona_cards').select("*").limit(1).execute()
        sample_persona = response.data[0] if response.data else None
        
        return render_template('index.html', sample_persona=sample_persona)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template('index.html', error=str(e))

@app.route('/personas')
def personas():
    try:
        # Check if persona_cards table exists
        if not check_table_exists('persona_cards'):
            init_database()
        
        # Get all personas
        response = supabase.table('persona_cards').select("*").execute()
        personas = response.data if response.data else []
        
        # Process personas data
        processed_personas = []
        for persona in personas:
            processed_persona = {
                'id': persona['id'],
                'name': persona['name'],
                'age': persona['age'],
                'occupation': persona['occupation'],
                'background': persona['background'],
                'challenges': persona['challenges'],
                'dietary_preferences': persona['dietary_preferences'],
                'household_size': persona['household_size'],
                'location': persona['location'],
                'climate_impact_concerns': persona['climate_impact_concerns']
            }
            processed_personas.append(processed_persona)
        
        return render_template('personas.html', personas=processed_personas)
    except Exception as e:
        logger.error(f"Error in personas route: {str(e)}")
        return render_template('personas.html', error=str(e))

@app.route('/guidebooks')
def guidebooks():
    try:
        # Check if guidebooks table exists
        if not check_table_exists('guidebooks'):
            init_database()
        
        # Get all guidebooks
        response = supabase.table('guidebooks').select("*").execute()
        guidebooks = response.data if response.data else []
        
        # Process guidebooks data
        processed_guidebooks = []
        for guidebook in guidebooks:
            # Parse the steps JSONB into a list
            steps = json.loads(guidebook['steps']) if isinstance(guidebook['steps'], str) else guidebook['steps']
            
            processed_guidebook = {
                'id': guidebook['id'],
                'title': guidebook['title'],
                'description': guidebook['description'],
                'steps': steps,
                'estimated_time': guidebook['estimated_time'],
                'difficulty_level': guidebook['difficulty_level'],
                'key_considerations': guidebook['key_considerations'],
                'resources_needed': guidebook['resources_needed']
            }
            processed_guidebooks.append(processed_guidebook)
        
        return render_template('guidebooks.html', guidebooks=processed_guidebooks)
    except Exception as e:
        logger.error(f"Error in guidebooks route: {str(e)}")
        return render_template('guidebooks.html', error=str(e))

@app.route('/implementation-plans')
def implementation_plans():
    try:
        # Check if implementation_plans table exists
        if not check_table_exists('implementation_plans'):
            init_database()
        
        # Get all implementation plans
        response = supabase.table('implementation_plans').select("*").execute()
        plans = response.data if response.data else []
        
        # Process implementation plans data
        processed_plans = []
        for plan in plans:
            processed_plan = {
                'id': plan['id'],
                'title': plan['title'],
                'description': plan['description'],
                'steps': plan['steps'],
                'timeline': plan['timeline'],
                'resources_needed': plan['resources_needed'],
                'success_metrics': plan['success_metrics'],
                'status': plan['status']
            }
            processed_plans.append(processed_plan)
        
        return render_template('implementation_plans.html', plans=processed_plans)
    except Exception as e:
        logger.error(f"Error in implementation_plans route: {str(e)}")
        return render_template('implementation_plans.html', error=str(e))

@app.route('/community-feedback')
def community_feedback():
    try:
        # Check if community_feedback table exists
        if not check_table_exists('community_feedback'):
            init_database()
        
        # Get all community feedback
        response = supabase.table('community_feedback').select("*").execute()
        feedback = response.data if response.data else []
        
        # Process community feedback data
        processed_feedback = []
        for entry in feedback:
            processed_entry = {
                'id': entry['id'],
                'persona_id': entry['persona_id'],
                'feedback_type': entry['feedback_type'],
                'content': entry['content'],
                'rating': entry['rating']
            }
            processed_feedback.append(processed_entry)
        
        return render_template('community_feedback.html', feedback=processed_feedback)
    except Exception as e:
        logger.error(f"Error in community_feedback route: {str(e)}")
        return render_template('community_feedback.html', error=str(e))

@app.route('/climate-impacts')
def climate_impacts():
    try:
        # Check if climate_impacts table exists
        if not check_table_exists('climate_impacts'):
            init_database()
        
        # Get all climate impacts
        response = supabase.table('climate_impacts').select("*").execute()
        impacts = response.data if response.data else []
        
        # Process climate impacts data
        processed_impacts = []
        for impact in impacts:
            processed_impact = {
                'id': impact['id'],
                'implementation_plan_id': impact['implementation_plan_id'],
                'metric_name': impact['metric_name'],
                'value': impact['value'],
                'unit': impact['unit'],
                'measurement_date': impact['measurement_date']
            }
            processed_impacts.append(processed_impact)
        
        return render_template('climate_impacts.html', impacts=processed_impacts)
    except Exception as e:
        logger.error(f"Error in climate_impacts route: {str(e)}")
        return render_template('climate_impacts.html', error=str(e))

@app.route('/api/personas')
def api_personas():
    try:
        # Check if persona_cards table exists
        if not check_table_exists('persona_cards'):
            init_database()
        
        # Get all personas
        response = supabase.table('persona_cards').select("*").execute()
        return jsonify(response.data if response.data else [])
    except Exception as e:
        logger.error(f"Error in api_personas route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/guidebooks')
def api_guidebooks():
    try:
        # Check if guidebooks table exists
        if not check_table_exists('guidebooks'):
            init_database()
        
        # Get all guidebooks
        response = supabase.table('guidebooks').select("*").execute()
        return jsonify(response.data if response.data else [])
    except Exception as e:
        logger.error(f"Error in api_guidebooks route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/implementation-plans')
def api_implementation_plans():
    try:
        # Check if implementation_plans table exists
        if not check_table_exists('implementation_plans'):
            init_database()
        
        # Get all implementation plans
        response = supabase.table('implementation_plans').select("*").execute()
        return jsonify(response.data if response.data else [])
    except Exception as e:
        logger.error(f"Error in api_implementation_plans route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/community-feedback')
def api_community_feedback():
    try:
        # Check if community_feedback table exists
        if not check_table_exists('community_feedback'):
            init_database()
        
        # Get all community feedback
        response = supabase.table('community_feedback').select("*").execute()
        return jsonify(response.data if response.data else [])
    except Exception as e:
        logger.error(f"Error in api_community_feedback route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/climate-impacts')
def api_climate_impacts():
    try:
        # Check if climate_impacts table exists
        if not check_table_exists('climate_impacts'):
            init_database()
        
        # Get all climate impacts
        response = supabase.table('climate_impacts').select("*").execute()
        return jsonify(response.data if response.data else [])
    except Exception as e:
        logger.error(f"Error in api_climate_impacts route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/implementation-plans', methods=['POST'])
def create_implementation_plan():
    try:
        data = request.get_json()
        response = supabase.table('implementation_plans').insert(data).execute()
        return jsonify(response.data[0] if response.data else None)
    except Exception as e:
        logger.error(f"Error creating implementation plan: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/community-feedback', methods=['POST'])
def create_community_feedback():
    try:
        data = request.get_json()
        response = supabase.table('community_feedback').insert(data).execute()
        return jsonify(response.data[0] if response.data else None)
    except Exception as e:
        logger.error(f"Error creating community feedback: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/climate-impacts', methods=['POST'])
def create_climate_impact():
    try:
        data = request.get_json()
        response = supabase.table('climate_impacts').insert(data).execute()
        return jsonify(response.data[0] if response.data else None)
    except Exception as e:
        logger.error(f"Error creating climate impact: {str(e)}")
        return jsonify({"error": str(e)}), 500

# This is the entry point for Vercel
app = app 