COMSATS Chatbot
A simple chatbot for COMSATS University, built with Flask, HTML, CSS, and JavaScript. It uses comsats_data.json for university-specific responses and the Google Generative AI (Gemini) API for general queries.
Setup

Activate the virtual environment:.\venv\Scripts\Activate.ps1


Install dependencies:pip install -r requirements.txt


Run the server:python app.py


Open http://localhost:5000 in a browser.

Deployment

Deploy to Heroku:heroku create
heroku config:set GOOGLE_API_KEY=your_key_here
git push heroku main



Files

app.py: Flask backend with Gemini API and JSON integration.
static/index.html: Chat interface.
static/css/style.css: Styling.
static/js/script.js: Frontend logic.
comsats_data.json: University data.
.env: Stores GOOGLE_API_KEY.
