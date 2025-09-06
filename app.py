"""import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"


def load_data(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return {}


def find_in_dict(data, disease):
    if not isinstance(data, dict):
        return []
    if disease in data:
        return data[disease]
    for key in data.keys():
        if key.lower() == disease.lower():
            return data[key]
    return []


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)

    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")

    if intent == "diseases_info":
        # Handle array or string for entity
        disease_param = req.get("queryResult", {}).get("parameters", {}).get("disease_sss", "")
        if isinstance(disease_param, list) and disease_param:
            disease = disease_param[0]
        elif isinstance(disease_param, str):
            disease = disease_param
        else:
            disease = ""

        if not disease:
            return jsonify({"fulfillmentText": "Please provide a disease name."})

        # Load files
        symptoms_data = load_data(SYMPTOMS_URL)
        preventions_data = load_data(PREVENTIONS_URL)
        diseases_data = load_data(DISEASES_URL)

        # Build response
        response_text = f"Here is the information I found for **{disease}**:\n\n"

        # Synonyms
        synonyms = find_in_dict(diseases_data, disease)
        if synonyms:
            response_text += "🔍 **Also known as:** " + ", ".join(synonyms) + "\n"

        # Symptoms
        symptoms = find_in_dict(symptoms_data, disease)
        if symptoms:
            response_text += "🩺 **Symptoms:** " + ", ".join(symptoms) + "\n"
        else:
            response_text += "🩺 Symptoms: Not available.\n"

        # Preventions
        preventions = find_in_dict(preventions_data, disease)
        if preventions:
            response_text += "✅ **Preventions:** " + ", ".join(preventions) + "\n"
        else:
            response_text += "✅ Preventions: Not available.\n"

        return jsonify({"fulfillmentText": response_text})

    return jsonify({"fulfillmentText": "Intent not handled."})


if __name__ == "__main__":
    app.run(debug=True)"""

import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------- GITHUB RAW FILES ----------
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"

# ---------- LOAD JSON DATA ----------
def load_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error loading {url}: {e}")
    return {}

diseases_data = load_json(DISEASES_URL)
symptoms_data = load_json(SYMPTOMS_URL)
preventions_data = load_json(PREVENTIONS_URL)

# ---------- WEBHOOK ----------
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    params = req.get("queryResult", {}).get("parameters", {})
    disease_param = params.get("disease_sss", [])

    # normalize disease parameter
    disease = None
    valid_diseases = list(symptoms_data.keys())

    if isinstance(disease_param, list):
        for item in disease_param:
            if item in valid_diseases:
                disease = item
                break
    elif isinstance(disease_param, str) and disease_param in valid_diseases:
        disease = disease_param

    response_text = "Sorry, I couldn't find information for that disease."

    if intent == "diseases_info" and disease:
        # Check symptoms first
        if disease in symptoms_data:
            symptoms = ", ".join(symptoms_data[disease])
            response_text = f"The symptoms of {disease} are: {symptoms}."
        # Optionally add preventions
        elif disease in preventions_data:
            preventions = ", ".join(preventions_data[disease])
            response_text = f"The preventions for {disease} are: {preventions}."

    return jsonify({"fulfillmentText": response_text})


if __name__ == "__main__":
    app.run(debug=True)

