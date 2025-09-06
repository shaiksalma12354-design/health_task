import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------- GITHUB RAW FILES ----------
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"


def load_data(url):
    """Fetch JSON data from GitHub raw link"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return {}


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # Get intent name
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
    
    # Process only diseases_info intent
    if intent == "diseases_info":
        # Extract disease entity
        disease = req.get("queryResult", {}).get("parameters", {}).get("disease_sss", "").lower()
        
        if not disease:
            return jsonify({"fulfillmentText": "Please provide a disease name."})

        # Load JSON data from GitHub
        diseases_data = load_data(DISEASES_URL)
        symptoms_data = load_data(SYMPTOMS_URL)
        preventions_data = load_data(PREVENTIONS_URL)

        response_text = f"Here is the information I found for **{disease.title()}**:\n\n"

        # Symptoms
        symptoms = symptoms_data.get(disease, [])
        if symptoms:
            response_text += "🩺 **Symptoms:** " + ", ".join(symptoms) + "\n"
        else:
            response_text += "🩺 Symptoms: Not available.\n"

        # Preventions
        preventions = preventions_data.get(disease, [])
        if preventions:
            response_text += "✅ **Preventions:** " + ", ".join(preventions) + "\n"
        else:
            response_text += "✅ Preventions: Not available.\n"

        return jsonify({"fulfillmentText": response_text})

    # Default fallback
    return jsonify({"fulfillmentText": "Sorry, I couldn't process that request."})


if __name__ == "__main__":
    app.run(debug=True)
