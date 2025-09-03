import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------- GITHUB RAW FILE LINKS ----------
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"

# ---------- HELPER FUNCTION ----------
def load_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ---------- WEBHOOK ROUTE ----------
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    parameters = req.get("queryResult", {}).get("parameters", {})
    disease = parameters.get("disease_sss", "").lower()

    response_text = "Sorry, I could not find any information."

    if intent == "diseases_info":
        data = load_data(DISEASES_URL)
        if isinstance(data, dict) and "error" in data:
            response_text = "Error loading diseases data."
        else:
            for item in data:
                if item["name"].lower() == disease or disease in [s.lower() for s in item.get("synonyms", [])]:
                    response_text = f"Disease: {item['name']}\nSynonyms: {', '.join(item.get('synonyms', []))}"
                    break

    elif intent == "symptoms_info":
        data = load_data(SYMPTOMS_URL)
        if isinstance(data, dict) and "error" in data:
            response_text = "Error loading symptoms data."
        else:
            for item in data:
                if item["name"].lower() == disease:
                    response_text = f"Symptoms of {item['name']}: {', '.join(item['symptoms'])}"
                    break

    elif intent == "preventions_info":
        data = load_data(PREVENTIONS_URL)
        if isinstance(data, dict) and "error" in data:
            response_text = "Error loading preventions data."
        else:
            for item in data:
                if item["name"].lower() == disease:
                    response_text = f"Preventions for {item['name']}: {', '.join(item['preventions'])}"
                    break

    return jsonify({"fulfillmentText": response_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
