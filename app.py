from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import google.api_core.exceptions
import time
import re

app = Flask(__name__)
CORS(app)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response_cache = {}  # In-memory cache for responses

# List of identity-related question patterns
IDENTITY_PATTERNS = [
    r"who\s+are\s+you",
    r"what\s+are\s+you",
    r"who\s+created\s+you",
    r"who\s+is\s+your\s+owner",
    r"who\s+made\s+you",
    r"who\s+built\s+you",
    r"what\s+is\s+your\s+name",
    r"tell\s+me\s+about\s+yourself"
]

# Pattern for queries about Mohammad Aqa Noori
NOORI_PATTERN = r"who\s+is\s+mohammad\s+aqa\s+noori"

# Custom response for Mohammad Aqa Noori
NOORI_RESPONSE = (
    "Mohammad Aqa Noori is the creator and owner of COMSATS Chatbot. "
    "He is a talented student at COMSATS University Islamabad, skilled in web development, UI/UX design, and AI-driven solutions. "
    "Passionate about technology and education, Noori built this chatbot to assist users with information about COMSATS University, "
    "reflecting his commitment to innovation and community engagement."
)

# Owner name
OWNER_NAME = "Mohammad Aqa Noori"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message").strip()
    
    # Check cache
    if user_message in response_cache:
        return jsonify({"response": response_cache[user_message]})
    
    # Check if the question is about Mohammad Aqa Noori
    if re.search(NOORI_PATTERN, user_message.lower()):
        response_cache[user_message] = NOORI_RESPONSE
        return jsonify({"response": NOORI_RESPONSE})
    
    # Check if the question is identity-related
    is_identity_question = any(re.search(pattern, user_message.lower()) for pattern in IDENTITY_PATTERNS)
    
    # Modify the prompt for identity questions
    if is_identity_question:
        modified_prompt = (
            f"You are COMSATS Chatbot, created by {OWNER_NAME} for COMSATS University. "
            f"Do not mention Gemini or Google. Respond to the following user query as COMSATS Chatbot: {user_message}"
        )
    else:
        modified_prompt = user_message
    
    retries = 3
    for attempt in range(retries):
        try:
            response = model.generate_content(modified_prompt)
            response_text = response.text
            
            # Post-process to replace any stray mentions of Gemini or Google
            response_text = re.sub(r'\bGemini\b', 'COMSATS Chatbot', response_text, flags=re.IGNORECASE)
            response_text = re.sub(r'\bGoogle\b', OWNER_NAME, response_text, flags=re.IGNORECASE)
            
            response_cache[user_message] = response_text
            return jsonify({"response": response_text})
        except google.api_core.exceptions.ResourceExhausted as e:
            if attempt < retries - 1:
                time.sleep(46)  # Retry after delay
                continue
            return jsonify({"error": "Rate limit exceeded. Please try again later or contact support to increase the quota."}), 429
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)