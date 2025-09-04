import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------- GITHUB RAW FILES ----------
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = 
PREVENTIONS_URL = "


# ---------- HELPER FUNCTION ----------
def load_json_from_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")

    # Load data
    diseases = load_json_from_github(DISEASES_URL)
    symptoms = load_json_from_github(SYMPTOMS_URL)
    preventions = load_json_from_github(PREVENTIONS_URL)  # not used now

    reply_text = "Sorry, I could not find information."

    if intent == "diseases_info":
        parameters = req.get("queryResult", {}).get("parameters", {})
        disease_name = parameters.get("disease_sss", "")

        if disease_name:
            disease_name = disease_name.strip()

            # ✅ Check disease exists in both diseases.json AND symptoms.json
            if disease_name in diseases and disease_name in symptoms:
                disease_symptoms = symptoms[disease_name]
                reply_text = f"Symptoms of {disease_name}: {', '.join(disease_symptoms)}"
            else:
                reply_text = f"Sorry, I don’t have symptoms for {disease_name}."

    return jsonify({"fulfillmentText": reply_text})


if __name__ == "__main__":
    app.run(debug=True)
