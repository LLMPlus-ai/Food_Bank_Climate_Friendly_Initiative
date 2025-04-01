from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client
import logging
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Verify environment variables
required_env_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-for-development')

# Initialize Supabase client with custom options for Vercel
try:
    supabase: Client = create_client(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY'),
        options={
            'headers': {
                'X-Client-Info': 'supabase-flask/1.0.0'
            }
        }
    )
    # Test the connection
    response = supabase.table('persona_cards').select("count").execute()
    logger.info("Successfully connected to Supabase!")
except Exception as e:
    logger.error(f"Failed to connect to Supabase: {str(e)}")
    raise

# Error handling
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}')
    return render_template('error.html', error=str(error)), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=str(error)), 404

def init_sample_data():
    try:
        # Check if data exists in Supabase
        personas_response = supabase.table('persona_cards').select("count").execute()
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
                },
                {
                    "name": "David Kumar",
                    "age": 28,
                    "occupation": "Graduate Student",
                    "background": "International student on limited budget",
                    "challenges": "Dietary restrictions, unfamiliar with local food system",
                    "dietary_preferences": "Vegan",
                    "household_size": 1,
                    "location": "Urban",
                    "climate_impact_concerns": "Passionate about reducing carbon footprint",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            ]
            supabase.table('persona_cards').insert(personas_data).execute()
            logger.info("Sample personas added to Supabase")
        
        guidebooks_response = supabase.table('guidebooks').select("count").execute()
        if not guidebooks_response.data or guidebooks_response.data[0]['count'] == 0:
            # Add sample guidebooks
            guidebooks_data = [
                {
                    "title": "Reducing Food Waste in Food Banks",
                    "description": "A comprehensive guide to minimizing food waste in food bank operations",
                    "steps": "1. Audit current waste levels\n2. Implement inventory tracking\n3. Optimize storage conditions\n4. Establish donation guidelines\n5. Train staff and volunteers",
                    "estimated_time": "3-6 months",
                    "difficulty_level": "Medium",
                    "key_considerations": "Storage capacity, volunteer training needs",
                    "resources_needed": "Inventory management system, storage containers, training materials",
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                },
                {
                    "title": "Establishing a New Food Bank",
                    "description": "Step-by-step guide to setting up a climate-friendly food bank",
                    "steps": "1. Community needs assessment\n2. Location selection\n3. Equipment procurement\n4. Volunteer recruitment\n5. Partnership development",
                    "estimated_time": "6-12 months",
                    "difficulty_level": "High",
                    "key_considerations": "Location accessibility, storage requirements",
                    "resources_needed": "Facility, refrigeration units, transport vehicles",
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
        response = supabase.table('persona_cards').select("*").execute()
        return render_template('personas.html', personas=response.data)
    except Exception as e:
        logger.error(f"Error in personas route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/personas')
def get_personas():
    try:
        response = supabase.table('persona_cards').select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error in get_personas route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/guidebooks')
def guidebooks():
    try:
        response = supabase.table('guidebooks').select("*").execute()
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

@app.route('/api/implementation-plans', methods=['POST'])
def create_implementation_plan():
    try:
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
        data = request.json
        data['created_at'] = datetime.utcnow().isoformat()
        response = supabase.table('climate_impacts').insert(data).execute()
        return jsonify(response.data[0])
    except Exception as e:
        logger.error(f"Error adding climate impact: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Initialize sample data if running in development
if not os.environ.get('VERCEL_ENV') == 'production':
    try:
        init_sample_data()
    except Exception as e:
        logger.error(f"Error during sample data initialization: {str(e)}")
        print(f"Error during sample data initialization: {str(e)}", file=sys.stderr)

# This is the entry point for Vercel
app = app 