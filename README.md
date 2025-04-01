# Food Bank Climate-Friendly Initiative Tool

A simple proof-of-concept dashboard to help food bank managers become more climate-friendly without negative financial or social impacts.

## Features

- Persona Cards: Explore fictionalized profiles of food bank users
- Guidebooks: Access practical guides for implementing climate-friendly initiatives
- Process Guide: Step-by-step implementation process

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
  - `base.html`: Base template with common layout
  - `index.html`: Home page
  - `personas.html`: Persona cards view
  - `guidebooks.html`: Guidebooks view
  - `process.html`: Implementation process view
- `foodbank.db`: SQLite database (created automatically)

## Development

This is a proof-of-concept implementation. Future development could include:

- User authentication
- Custom persona card creation
- Interactive guidebook templates
- Progress tracking
- Community feedback system
- Mobile-responsive design improvements 