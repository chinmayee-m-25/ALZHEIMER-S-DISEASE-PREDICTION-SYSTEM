import React, { useState } from "react";
import "./App.css";
import jsPDF from "jspdf";

function App() {
  const [formData, setFormData] = useState({
    age: 60, gender: 0, ethnicity: 0, education: 0,
    bmi: 22, smoking: 0, alcohol: 5, physical: 5,
    diet: 5, sleep: 5, family_history: 0, cardiovascular: 0,
    diabetes: 0, depression: 0, head_injury: 0, hypertension: 0,
    systolic_bp: 120, diastolic_bp: 80, cholesterol_total: 200,
    cholesterol_ldl: 100, cholesterol_hdl: 50, cholesterol_trig: 150,
    mmse: 20, functional: 5, memory: 0, behavioral: 0,
    adl: 5, confusion: 0, disorientation: 0, personality: 0,
    difficulty_tasks: 0, forgetfulness: 0
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };
const downloadPDF = () => {
  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text("Alzheimer's Disease Prediction Report", 20, 20);
  doc.setFontSize(12);
  doc.text(`Prediction: ${result.prediction === 1 ? "Positive - Disease Detected" : "Negative - No Disease"}`, 20, 40);
  doc.text(`Risk Percentage: ${result.risk_proba}%`, 20, 55);
  doc.text(`Risk Level: ${result.risk_level}`, 20, 70);
  doc.text("Precautions:", 20, 90);
  result.precautions.forEach((p, i) => {
    doc.text(`- ${p}`, 20, 105 + i * 15);
  });
  doc.save("patient_report.pdf");
};
  const handlePredict = async () => {
    try {
      const response = await fetch("https://alzheimer-s-disease-prediction-system.onrender.com", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error connecting to backend. Make sure Flask is running!");
    }
  };

  const sliderFields = [
    { name: "age", label: "Age", min: 40, max: 100 },
    { name: "bmi", label: "BMI", min: 10, max: 40 },
    { name: "alcohol", label: "Alcohol Consumption", min: 0, max: 20 },
    { name: "physical", label: "Physical Activity (hrs/week)", min: 0, max: 10 },
    { name: "diet", label: "Diet Quality (0-10)", min: 0, max: 10 },
    { name: "sleep", label: "Sleep Quality (0-10)", min: 0, max: 10 },
    { name: "systolic_bp", label: "Systolic BP", min: 90, max: 200 },
    { name: "diastolic_bp", label: "Diastolic BP", min: 60, max: 120 },
    { name: "cholesterol_total", label: "Total Cholesterol", min: 100, max: 300 },
    { name: "cholesterol_ldl", label: "LDL", min: 0, max: 200 },
    { name: "cholesterol_hdl", label: "HDL", min: 0, max: 100 },
    { name: "cholesterol_trig", label: "Triglycerides", min: 0, max: 300 },
    { name: "mmse", label: "MMSE Score (0-30)", min: 0, max: 30 },
    { name: "functional", label: "Functional Assessment (0-10)", min: 0, max: 10 },
    { name: "adl", label: "ADL Score (0-10)", min: 0, max: 10 },
  ];

  const dropdownFields = [
    { name: "gender", label: "Gender", options: ["Male", "Female"] },
    { name: "ethnicity", label: "Ethnicity", options: ["0", "1", "2", "3"] },
    { name: "education", label: "Education Level", options: ["0", "1", "2", "3"] },
    { name: "smoking", label: "Smoking", options: ["No", "Yes"] },
    { name: "family_history", label: "Family History Alzheimer's", options: ["No", "Yes"] },
    { name: "cardiovascular", label: "Cardiovascular Disease", options: ["No", "Yes"] },
    { name: "diabetes", label: "Diabetes", options: ["No", "Yes"] },
    { name: "depression", label: "Depression", options: ["No", "Yes"] },
    { name: "head_injury", label: "Head Injury", options: ["No", "Yes"] },
    { name: "hypertension", label: "Hypertension", options: ["No", "Yes"] },
    { name: "memory", label: "Memory Complaints", options: ["No", "Yes"] },
    { name: "behavioral", label: "Behavioral Problems", options: ["No", "Yes"] },
    { name: "confusion", label: "Confusion", options: ["No", "Yes"] },
    { name: "disorientation", label: "Disorientation", options: ["No", "Yes"] },
    { name: "personality", label: "Personality Changes", options: ["No", "Yes"] },
    { name: "difficulty_tasks", label: "Difficulty Completing Tasks", options: ["No", "Yes"] },
    { name: "forgetfulness", label: "Forgetfulness", options: ["No", "Yes"] },
  ];

  return (
    <div className="app">
      <h1>🧠 Alzheimer's Disease Prediction System</h1>
      <p className="subtitle">Enter patient health details to check Alzheimer risk</p>

      <div className="form-grid">
        <div className="card">
          <h2>Patient Info</h2>
          {sliderFields.slice(0, 6).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label} <span>{formData[f.name]}</span></label>
              <input type="range" name={f.name} min={f.min} max={f.max}
                value={formData[f.name]} onChange={handleChange} />
            </div>
          ))}
          {dropdownFields.slice(0, 4).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label}</label>
              <select name={f.name} value={formData[f.name]} onChange={handleChange}>
                {f.options.map((o, i) => <option value={i} key={i}>{o}</option>)}
              </select>
            </div>
          ))}
        </div>

        <div className="card">
          <h2>Medical History</h2>
          {dropdownFields.slice(4, 10).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label}</label>
              <select name={f.name} value={formData[f.name]} onChange={handleChange}>
                {f.options.map((o, i) => <option value={i} key={i}>{o}</option>)}
              </select>
            </div>
          ))}
          {sliderFields.slice(6, 8).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label} <span>{formData[f.name]}</span></label>
              <input type="range" name={f.name} min={f.min} max={f.max}
                value={formData[f.name]} onChange={handleChange} />
            </div>
          ))}
        </div>

        <div className="card">
          <h2>Clinical Measurements</h2>
          {sliderFields.slice(8).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label} <span>{formData[f.name]}</span></label>
              <input type="range" name={f.name} min={f.min} max={f.max}
                value={formData[f.name]} onChange={handleChange} />
            </div>
          ))}
          {dropdownFields.slice(10).map((f) => (
            <div className="field" key={f.name}>
              <label>{f.label}</label>
              <select name={f.name} value={formData[f.name]} onChange={handleChange}>
                {f.options.map((o, i) => <option value={i} key={i}>{o}</option>)}
              </select>
            </div>
          ))}
        </div>
      </div>

      <button className="predict-btn" onClick={handlePredict}>
        🔍 Predict Alzheimer's Risk
      </button>

      {result && (
        <div className="results">
          <h2>Results</h2>
          <div className="result-cards">
            <div className={`result-box ${result.prediction === 1 ? "positive" : "negative"}`}>
              {result.prediction === 1 ? "Positive — Disease Detected" : "Negative — No Disease"}
            </div>
            <div className="metric-box">
              <p>Risk Percentage</p>
              <h1>{result.risk_proba}%</h1>
            </div>
            <div className="metric-box">
              <p>Risk Level</p>
              <h1>{result.risk_level}</h1>
            </div>
          </div>
<button className="predict-btn" onClick={downloadPDF}>
  📄 Download PDF Report
</button>
          <div className="precautions">
            <h3>Precautions / Recommendations</h3>
            {result.precautions.map((p, i) => (
              <p key={i}>✅ {p}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;