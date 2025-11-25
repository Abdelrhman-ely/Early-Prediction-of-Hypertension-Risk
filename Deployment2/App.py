import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------------------------
# Load Pipeline
# ---------------------------
with open("xgb_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# ---------------------------
# Session State for Theme
# ---------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ---------------------------
# Theme Colors
# ---------------------------
def get_colors():
    if st.session_state.dark_mode:
        return {
            "bg": "#121212",
            "text": "#FFFFFF",
            "input_bg": "#1E1E1E",
            "card_safe": "#1B5E20",
            "card_danger": "#B71C1C",
            "header": "#3498DB",
            "label": "#FFFFFF",
        }
    else:
        return {
            "bg": "#F5F5F5",
            "text": "#000000",
            "input_bg": "#FFFFFF",
            "card_safe": "#28B463",
            "card_danger": "#E74C3C",
            "header": "#2E86C1",
            "label": "#000000",
        }

colors = get_colors()

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        .title {{
            text-align: center;
            font-size: 46px !important;
            font-weight: bold;
            color: {colors['header']};
        }}
        .subtitle {{
            text-align: center;
            font-size: 24px !important;
            margin-bottom: 25px;
            color: {colors['header']};
        }}
        .result-card {{
            padding: 30px; 
            border-radius: 18px;
            margin-top: 20px;
            font-size: 22px;
            text-align:center;
            color:white;
        }}
        .stButton button {{
            width: auto;
            min-width: 200px;
            height: 40px;
            border-radius: 12px;
            font-size: 18px !important;
            background-color: {colors['header']};
            color: white;
            margin-bottom: 10px;
        }}
        .stButton button:hover {{
            background-color: #21618C;
            color: white;
        }}
        /* Input Labels */
        label {{
            color: {colors['label']} !important;
            font-size: 20px !important;
        }}
        /* Remove slider background */
        .stSlider div[role="slider"] {{
            background: none !important;
        }}
        /* Inputs background */
        .stNumberInput input, select {{
            background-color: {colors['input_bg']};
            color: {colors['text']};
            font-size: 20px !important;
        }}
        hr {{
            border: 1px solid {colors['text']};
        }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Theme Toggle Button
# ---------------------------
st.button("🌙 Toggle Night/Light Mode", on_click=toggle_theme)

# ---------------------------
# Header
# ---------------------------
st.markdown("<h1 class='title'>🫀 Hypertension Risk Classification</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter your health information to analyze your risk level</p>", unsafe_allow_html=True)

# ---------------------------
# Expected columns
# ---------------------------
expected_columns = [
    'Diabetes', 'Triglycerides', 'Employment_Status', 'Heart_Rate', 'Smoking_Status',
    'Sleep_Duration', 'Salt_Intake', 'Cholesterol', 'LDL', 'Family_History',
    'Physical_Activity_Level', 'Alcohol_Intake', 'Education_Level', 'HDL',
    'Systolic_BP', 'Diastolic_BP', 'Glucose', 'Age', 'BMI', 'Stress_Level',
    'Gender'
]

# ---------------------------
# User Inputs
# ---------------------------
st.subheader("✨ Enter Your Data")

age = st.number_input("Age:", 1, 120, 30)
bmi = st.number_input("BMI:", 10.0, 60.0, 22.5)
stress = st.slider("Stress Level (0 - 10):", 0, 10, 5)
heart_rate = st.number_input("Heart Rate:", 40, 200, 70)
systolic_bp = st.number_input("Systolic BP:", 80, 200, 120)
diastolic_bp = st.number_input("Diastolic BP:", 50, 130, 80)
cholesterol = st.number_input("Cholesterol:", 100, 400, 180)
hdl = st.number_input("HDL:", 20, 100, 50)
ldl = st.number_input("LDL:", 50, 250, 100)
triglycerides = st.number_input("Triglycerides:", 50, 500, 150)
glucose = st.number_input("Glucose:", 50, 300, 90)
sleep_duration = st.slider("Sleep Duration (hours):", 0.0, 24.0, 7.0)
salt_intake = st.slider("Salt Intake (grams):", 0.0, 15.0, 10.0, 0.1)
alcohol_intake = st.slider("Alcohol Intake (units):", 0.0, 35.0, 0.0, 0.1)

gender = st.selectbox("Gender:", ["Male", "Female"])
smoking_status = st.selectbox("Smoking Status:", ["Never", "Former", "Current"])
diabetes = st.selectbox("Diabetes:", ["Yes", "No"])
employment_status = st.selectbox("Employment Status:", ["Employed", "Unemployed", "Retired"])
family_history = st.selectbox("Family History of Hypertension:", ["Yes", "No"])
physical_activity = st.selectbox("Physical Activity Level:", ["Low", "Medium", "High"])
education_level = st.selectbox("Education Level:", ["None", "Primary", "Secondary", "Tertiary"])

# ---------------------------
# Prepare Data
# ---------------------------
user_input = {
    'Diabetes': diabetes,
    'Triglycerides': triglycerides,
    'Employment_Status': employment_status,
    'Heart_Rate': heart_rate,
    'Smoking_Status': smoking_status,
    'Sleep_Duration': sleep_duration,
    'Salt_Intake': salt_intake,
    'Cholesterol': cholesterol,
    'LDL': ldl,
    'Family_History': family_history,
    'Physical_Activity_Level': physical_activity,
    'Alcohol_Intake': alcohol_intake,
    'Education_Level': education_level,
    'HDL': hdl,
    'Systolic_BP': systolic_bp,
    'Diastolic_BP': diastolic_bp,
    'Glucose': glucose,
    'Age': age,
    'BMI': bmi,
    'Stress_Level': stress,
    'Gender': gender,
}

data = pd.DataFrame([user_input])

for col in expected_columns:
    if col not in data.columns:
        data[col] = np.nan
data = data[expected_columns]

# Manual Encoding
data['Diabetes'] = data['Diabetes'].map({'Yes': 1, 'No': 0})
data['Family_History'] = data['Family_History'].map({'Yes': 1, 'No': 0})
data['Gender'] = data['Gender'].map({'Male': 1, 'Female': 0})
data['Physical_Activity_Level'] = data['Physical_Activity_Level'].map({'Low': 0, 'Medium': 1, 'High': 2})
data['Education_Level'] = data['Education_Level'].map({'None': 0, 'Primary': 1, 'Secondary': 2, 'Tertiary': 3})
data['Employment_Status'] = data['Employment_Status'].map({'Unemployed': 0, 'Employed': 1, 'Retired': 2})
data['Smoking_Status'] = data['Smoking_Status'].map({'Never': 0, 'Former': 1, 'Current': 2})

numeric_cols = [
    'Triglycerides','Heart_Rate','Sleep_Duration','Salt_Intake','Cholesterol','LDL',
    'HDL','Systolic_BP','Diastolic_BP','Glucose','Age','BMI','Stress_Level','Alcohol_Intake'
]
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# ---------------------------
# Prediction
# ---------------------------
if st.button("🔍 Analyze Risk"):
    try:
        prediction = pipeline.predict(data)[0]
        probability = pipeline.predict_proba(data)[0][1]

        if prediction == 1:
            st.markdown(f"""
                <div style='background-color:{colors['card_danger']}; padding:30px; border-radius:18px; font-size:22px; text-align:center; color:white;'>
                    ⚠️ High Risk Detected<br>
                    Risk Probability: <b>{probability*100:.2f}%</b>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color:{colors['card_safe']}; padding:30px; border-radius:18px; font-size:22px; text-align:center; color:white;'>
                    🟢 Low Risk<br>
                    Risk Probability: <b>{probability*100:.2f}%</b>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error during analysis: {e}")

# ---------------------------
# Footer
# ---------------------------
st.markdown(f"""
    <hr>
    <p style='text-align:center; font-size:20px; color:{colors['text']};'>
        🔧 Developed with Streamlit + XGBoost
    </p>
""", unsafe_allow_html=True)
