import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Alzheimer's Prediction", layout="wide")

st.markdown("""
<style>
    .main { background-color: #1a1a2e; color: white; }
    .stSelectbox label, .stSlider label, .stNumberInput label {
        background-color: #4a4a8a;
        color: white;
        padding: 4px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }
    .stButton>button {
        background-color: #6c63ff;
        color: white;
        width: 100%;
        padding: 12px;
        font-size: 18px;
        border-radius: 8px;
        border: none;
        margin-top: 20px;
    }
    .stButton>button:hover { background-color: #5a52d5; }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin: 10px 0;
    }
    .positive { background-color: #ff4b4b; color: white; }
    .negative { background-color: #00c853; color: white; }
    .metric-box {
        background-color: #2a2a4a;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

model2 = pickle.load(open("alzheimers_rf.pkl", "rb"))

st.markdown("## 🧠 Alzheimer's Disease Prediction System")
st.write("Enter patient health details to check Alzheimer risk")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Patient Info")
    age = st.slider("Age", 40, 100, 60)
    gender = st.selectbox("Gender (0=Male, 1=Female)", [0, 1])
    ethnicity = st.selectbox("Ethnicity", [0, 1, 2, 3])
    education = st.selectbox("Education Level", [0, 1, 2, 3])
    bmi = st.slider("BMI", 10.0, 40.0, 22.0)
    smoking = st.selectbox("Smoking", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    alcohol = st.slider("Alcohol Consumption", 0.0, 20.0, 5.0)
    physical = st.slider("Physical Activity (hrs/week)", 0.0, 10.0, 5.0)
    diet = st.slider("Diet Quality (0-10)", 0.0, 10.0, 5.0)
    sleep = st.slider("Sleep Quality (0-10)", 0.0, 10.0, 5.0)

with col2:
    st.markdown("### Medical History")
    family_history = st.selectbox("Family History Alzheimer's", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    cardiovascular = st.selectbox("Cardiovascular Disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    diabetes = st.selectbox("Diabetes", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    depression = st.selectbox("Depression", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    head_injury = st.selectbox("Head Injury", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    systolic_bp = st.slider("Systolic BP", 0, 200, 120)
    diastolic_bp = st.slider("Diastolic BP", 0, 150, 80)

with col3:
    st.markdown("### Clinical Measurements")
    cholesterol_total = st.slider("Total Cholesterol", 0.0, 300.0, 200.0)
    cholesterol_ldl = st.slider("LDL", 0.0, 200.0, 100.0)
    cholesterol_hdl = st.slider("HDL", 0.0, 100.0, 50.0)
    cholesterol_trig = st.slider("Triglycerides", 0.0, 300.0, 150.0)
    mmse = st.slider("MMSE Score (0-30)", 0.0, 30.0, 20.0)
    functional = st.slider("Functional Assessment (0-10)", 0.0, 10.0, 5.0)
    memory = st.selectbox("Memory Complaints", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    behavioral = st.selectbox("Behavioral Problems", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    adl = st.slider("ADL Score (0-10)", 0.0, 10.0, 5.0)
    confusion = st.selectbox("Confusion", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    disorientation = st.selectbox("Disorientation", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    personality = st.selectbox("Personality Changes", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    difficulty_tasks = st.selectbox("Difficulty Completing Tasks", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    forgetfulness = st.selectbox("Forgetfulness", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

if st.button("🔍 Predict Alzheimer's Risk"):
    test_data = np.array([[age, gender, ethnicity, education, bmi, smoking, alcohol,
                           physical, diet, sleep, family_history, cardiovascular,
                           diabetes, depression, head_injury, hypertension, systolic_bp,
                           diastolic_bp, cholesterol_total, cholesterol_ldl, cholesterol_hdl,
                           cholesterol_trig, mmse, functional, memory, behavioral, adl,
                           confusion, disorientation, personality, difficulty_tasks, forgetfulness]])

    prediction = model2.predict(test_data)
    risk_proba = model2.predict_proba(test_data)[0][1] * 100

    if risk_proba < 30:
        risk_level = "Low Risk"
    elif 30 <= risk_proba < 70:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    st.markdown("---")
    st.markdown("## Results")

    r1, r2, r3 = st.columns(3)
    with r1:
        if prediction[0] == 1:
            st.markdown('<div class="result-box positive">Positive — Disease Detected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box negative">Negative — No Disease</div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="metric-box"><h3 style="color:white">Risk Percentage</h3><h1 style="color:#6c63ff">{risk_proba:.1f}%</h1></div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="metric-box"><h3 style="color:white">Risk Level</h3><h1 style="color:#6c63ff">{risk_level}</h1></div>', unsafe_allow_html=True)

    st.markdown("### Risk Chart")
    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    bars = ax.bar(["No Disease Risk", "Disease Risk"],
                  [100 - risk_proba, risk_proba],
                  color=["#00c853", "#ff4b4b"])
    ax.set_ylabel("Percentage %", color="white")
    ax.set_ylim(0, 100)
    ax.tick_params(colors="white")
    for bar, val in zip(bars, [100 - risk_proba, risk_proba]):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1,
                f"{val:.1f}%", ha="center", color="white", fontweight="bold")
    st.pyplot(fig)

    if prediction[0] == 1 or risk_proba > 50:
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

    st.markdown("### Precautions / Recommendations")
    for p in precautions:
        st.markdown(f"✅ {p}")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Alzheimer's Disease Prediction Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(190, 10, txt=f"Prediction: {'Positive' if prediction[0] == 1 else 'Negative'}", ln=True)
    pdf.cell(190, 10, txt=f"Risk Percentage: {risk_proba:.2f}%", ln=True)
    pdf.cell(190, 10, txt=f"Risk Level: {risk_level}", ln=True)
    pdf.ln(5)
    pdf.cell(190, 10, txt="Recommended Precautions:", ln=True)
    pdf.set_font("Arial", size=11)
    for p in precautions:
        pdf.multi_cell(190, 10, f"- {p}")
    pdf.output("patient_report.pdf")

    with open("patient_report.pdf", "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="patient_report.pdf")