import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
df = pd.read_csv("alzheimers_disease_data.csv")

# Check columns
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

# Clean data
df = df.dropna()

# Remove non-useful columns if present
if 'PatientID' in df.columns:
    df = df.drop("PatientID", axis=1)
if 'DoctorInCharge' in df.columns:
    df = df.drop("DoctorInCharge", axis=1)

# Features and target
X = df.drop("Diagnosis", axis=1)
y = df["Diagnosis"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully!")
