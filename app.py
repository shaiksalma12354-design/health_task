from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# JSON file links (replace with your actual links)
DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"


def load_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
    parameters = req.get("queryResult", {}).get("parameters", {})

    disease_name = parameters.get("disease_sss")
    response_text = "Sorry, I couldn't find information."

    if disease_name:
        disease_name = disease_name.lower()

        # Load JSON fresh each request (optional: cache for performance)
        diseases_data = load_json_from_url(DISEASES_URL)
        symptoms_data = load_json_from_url(SYMPTOMS_URL)
        preventions_data = load_json_from_url(PREVENTIONS_URL)

        if intent == "diseases_info":
            if disease_name in symptoms_data:
                response_text = f"Symptoms of {disease_name.title()}: {', '.join(symptoms_data[disease_name])}"
            elif disease_name in preventions_data:
                response_text = f"Preventions for {disease_name.title()}: {', '.join(preventions_data[disease_name])}"
            elif disease_name in diseases_data:
                response_text = f"Other names for {disease_name.title()}: {', '.join(diseases_data[disease_name])}"

    return jsonify({"fulfillmentText": response_text})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
