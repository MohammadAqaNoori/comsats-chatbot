from flask import Flask, send_from_directory, request, jsonify
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

# Load university data
try:
    with open('comsats_data.json', 'r') as f:
        university_data = json.load(f)
except FileNotFoundError:
    university_data = {}
    print("Warning: comsats_data.json not found. Using empty data.")

# Predefined course list for concise, structured response
COURSES = [
    "Engineering (Electrical, Computer, Mechanical, Civil)",
    "Computer Science & IT (Computer Science, Software Engineering, AI)",
    "Business Administration (BBA, MBA, Accounting & Finance)",
    "Sciences (Mathematics, Physics, Chemistry)",
    "Biosciences (Bioinformatics, Pharmacy, Molecular Biology)",
    "Architecture & Design (Architecture, Interior Design)",
    "Arts & Social Sciences (English, Psychology, Economics)"
]

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower().strip()
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})

    # Check university data with structured responses
    university = university_data.get('university', {})
    response = None
    if any(keyword in user_message for keyword in ['name', 'university', 'comsats']):
        response = f"**University Name**: {university.get('name', 'No name found.')}"
    elif any(keyword in user_message for keyword in ['description', 'about', 'info', 'overview']):
        response = f"**About COMSATS**: {university.get('description', 'No description found.')}"
    elif any(keyword in user_message for keyword in ['contact', 'email', 'phone', 'reach', 'get in touch']):
        response = f"**Contact Information**: {university.get('contact', 'No contact info found.')}"
    elif any(keyword in user_message for keyword in ['website', 'url', 'site', 'web']):
        response = f"**Website**: {university.get('website', 'No website found.')}"
    elif any(keyword in user_message for keyword in ['course', 'csc', 'class', 'subject', 'program', 'department', 'faculty']):
        response = "**COMSATS Programs**:\n" + "\n".join(f"- {course}" for course in COURSES) + "\n\nVisit the COMSATS website for detailed course information."

    if response:
        return jsonify({'response': response})

    # Fallback to Gemini API with structured prompt
    try:
        prompt = (
            f"You are an assistant for COMSATS University Islamabad. "
            f"Answer the question '{user_message}' in a clear, concise, and professional manner. "
            f"Use 2-3 bullet points for lists or a single short paragraph (2-3 sentences) for explanations. "
            f"Ensure the answer is accurate, relevant, and avoids unnecessary details. "
            f"If the question is ambiguous, provide a brief, informative response."
        )
        response = model.generate_content(prompt)
        return jsonify({'response': response.text.strip()})
    except Exception as e:
        return jsonify({'response': f'**Error**: Unable to contact Gemini API: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)