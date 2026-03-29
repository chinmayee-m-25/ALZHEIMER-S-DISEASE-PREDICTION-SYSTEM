from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

model2 = pickle.load(open("alzheimers_rf.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_data = np.array([[
        data["age"], data["gender"], data["ethnicity"], data["education"],
        data["bmi"], data["smoking"], data["alcohol"], data["physical"],
        data["diet"], data["sleep"], data["family_history"], data["cardiovascular"],
        data["diabetes"], data["depression"], data["head_injury"], data["hypertension"],
        data["systolic_bp"], data["diastolic_bp"], data["cholesterol_total"],
        data["cholesterol_ldl"], data["cholesterol_hdl"], data["cholesterol_trig"],
        data["mmse"], data["functional"], data["memory"], data["behavioral"],
        data["adl"], data["confusion"], data["disorientation"], data["personality"],
        data["difficulty_tasks"], data["forgetfulness"]
    ]])

    prediction = model2.predict(input_data)[0]
    risk_proba = round(model2.predict_proba(input_data)[0][1] * 100, 2)

    if risk_proba < 30:
        risk_level = "Low Risk"
    elif 30 <= risk_proba < 70:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    if prediction == 1 or risk_proba > 50:
        precautions = [
            "Maintain a balanced diet rich in omega-3 and antioxidants.",
            "Engage in regular physical exercise and cognitive activities.",
            "Ensure consistent sleep patterns.",
            "Manage cardiovascular risk factors.",
            "Consult a neurologist for further assessment."
        ]
    else:
        precautions = [
            "Maintain a healthy lifestyle and diet.",
            "Engage in routine brain-stimulating activities.",
            "Schedule regular health check-ups."
        ]

    return jsonify({
        "prediction": int(prediction),
        "risk_proba": risk_proba,
        "risk_level": risk_level,
        "precautions": precautions
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
