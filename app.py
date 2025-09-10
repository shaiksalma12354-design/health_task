
# if __name__ == "__main__":
#     app.run(debug=True)

# import json
# import requests
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # ---------- GITHUB RAW FILES ----------
# DISEASES_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/diseases.json"
# SYMPTOMS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/symptoms.json"
# PREVENTIONS_URL = "https://raw.githubusercontent.com/shaiksalma12354-design/health_task/main/preventions.json"

# # ---------- LOAD JSON DATA ----------
# def load_json(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#     except Exception as e:
#         print(f"Error loading {url}: {e}")
#     return {}

# diseases_data = load_json(DISEASES_URL)
# symptoms_data = load_json(SYMPTOMS_URL)
# preventions_data = load_json(PREVENTIONS_URL)

# valid_diseases = set(symptoms_data.keys()) | set(preventions_data.keys())

# # ---------- WEBHOOK ----------
# @app.route("/webhook", methods=["POST"])
# def webhook():
#     req = request.get_json(silent=True, force=True)

#     intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
#     params = req.get("queryResult", {}).get("parameters", {})
#     disease_param = params.get("disease_sss", [])

#     disease = None

#     # --- strict validation ---
#     if isinstance(disease_param, list):
#         for item in disease_param:
#             if item in valid_diseases:
#                 disease = item
#                 break
#     elif isinstance(disease_param, str) and disease_param in valid_diseases:
#         disease = disease_param

#     response_text = "Sorry, I couldn't find information for that disease."

#     if intent == "diseases_info" and disease:
#         if disease in symptoms_data:
#             symptoms = ", ".join(symptoms_data[disease])
#             response_text = f"The symptoms of {disease} are: {symptoms}."
#         elif disease in preventions_data:
#             preventions = ", ".join(preventions_data[disease])
#             response_text = f"The preventions for {disease} are: {preventions}."

#     return jsonify({"fulfillmentText": response_text})

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

diseases_data = load_json(DISEASES_URL)        # Disease -> Symptoms
symptoms_data = load_json(SYMPTOMS_URL)        # Symptom -> Diseases
preventions_data = load_json(PREVENTIONS_URL)  # Disease -> Preventions

valid_diseases = set(diseases_data.keys()) | set(preventions_data.keys())
valid_symptoms = set(symptoms_data.keys())

# ---------- WEBHOOK ----------
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    params = req.get("queryResult", {}).get("parameters", {})

    disease_param = params.get("disease_sss", [])
    symptoms_param = params.get("symptoms", [])

    # Normalize inputs
    if isinstance(disease_param, str):
        disease_param = [disease_param]
    if isinstance(symptoms_param, str):
        symptoms_param = [symptoms_param]

    response_text = "Sorry, I couldn't find information for that."

    # ----------------- Auto Detection -----------------
    detected_disease = None
    detected_symptoms = []

    # Check if disease given
    for d in disease_param:
        if d in valid_diseases:
            detected_disease = d
            break

    # Check if symptoms given
    for s in symptoms_param:
        if s in valid_symptoms:
            detected_symptoms.append(s)

    # ----------------- 1️⃣ Disease → Symptoms / Preventions -----------------
    if detected_disease:
        if detected_disease in diseases_data:
            symptoms = ", ".join(diseases_data[detected_disease])
            response_text = f"The symptoms of {detected_disease} are: {symptoms}."
        elif detected_disease in preventions_data:
            preventions = ", ".join(preventions_data[detected_disease])
            response_text = f"The preventions for {detected_disease} are: {preventions}."

    # ----------------- 2️⃣ Symptoms → Diseases -----------------
    elif detected_symptoms:
        possible_diseases = set()
        for symptom in detected_symptoms:
            diseases = symptoms_data.get(symptom, [])
            possible_diseases.update(diseases)

        if possible_diseases:
            response_text = f"Based on your symptoms, possible diseases are: {', '.join(possible_diseases)}."
        else:
            response_text = "Sorry, I couldn’t find any diseases matching your symptoms."

    return jsonify({"fulfillmentText": response_text})


if __name__ == "__main__":
    app.run(debug=True)
