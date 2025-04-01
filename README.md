# Food Bank Climate-Friendly Initiative

A web application designed to help food bank managers adopt climate-friendly practices through persona cards, guidebooks, and implementation processes.

## Features

- **Persona Cards**: Understand different user profiles and their barriers to climate-friendly diets
- **Guidebooks**: Step-by-step guides for implementing climate-friendly practices
- **Implementation Process**: Interactive timeline for planning and tracking progress
- **Community Feedback**: System for gathering and analyzing community input
- **Climate Impact Tracking**: Monitor and measure environmental impact

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- Bootstrap 5
- jQuery
- Chart.js

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/food-bank-climate.git
cd food-bank-climate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
food-bank-climate/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── personas.html  # Persona cards page
│   ├── guidebooks.html # Guidebooks page
│   └── process.html   # Implementation process page
└── static/           # Static files (CSS, JS, images)
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

