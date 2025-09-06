import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------- GITHUB RAW FILE LINKS ----------
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"


# ---------- Helper to fetch JSON ----------
def load_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {}


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)

    intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
    parameters = req.get("queryResult", {}).get("parameters", {})

    # Load JSON files
    diseases_data = load_json(DISEASES_URL)
    symptoms_data = load_json(SYMPTOMS_URL)
    preventions_data = load_json(PREVENTIONS_URL)

   // reply_text = "Sorry, I could not find the information."

    if intent == "diseases_info":
        disease = parameters.get("diseases_sss")
        symptom = parameters.get("symptoms")

        # If disease is asked, return its symptoms
        if disease:
            for item in symptoms_data.get("symptoms", []):
                if item["name"].lower() == disease.lower():
                    reply_text = f"Symptoms of {disease}: {', '.join(item['symptoms'])}"
                    break

        # If symptom is asked, return possible diseases
        elif symptom:
            matching_diseases = []
            for item in symptoms_data.get("symptoms", []):
                if symptom.lower() in [s.lower() for s in item["symptoms"]]:
                    matching_diseases.append(item["name"])
            if matching_diseases:
                reply_text = f"Diseases with symptom '{symptom}': {', '.join(matching_diseases)}"

    return jsonify({"fulfillmentText": reply_text})


if __name__ == "__main__":
    app.run(debug=True)
