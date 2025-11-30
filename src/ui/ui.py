import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

st.markdown(
    "<h2 style='text-align: center; color: #257180;'>Customer Churn Prediction</h2>",
    unsafe_allow_html=True
)
st.markdown("---")

if "prediction" not in st.session_state:
    st.session_state.prediction = None
    st.session_state.prob = None

if st.session_state.prediction:
    st.markdown(
        f"<h3 style='text-align: center; color: #257180;'>Prediction: {st.session_state.prediction}</h3>",
        unsafe_allow_html=True
    )
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.prob * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Churn Probability (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#257180"},
            'steps': [
                {'range': [0, 40], 'color': "#2ECC71"},
                {'range': [40, 70], 'color': "#F39C12"},
                {'range': [70, 100], 'color': "#E74C3C"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    SeniorCitizen = col1.selectbox("Senior Citizen", [0, 1], key="SeniorCitizen")
    Partner = col1.selectbox("Partner", ["Yes", "No"], key="Partner")
    Dependents = col1.selectbox("Dependents", ["Yes", "No"], key="Dependents")
    tenure = col1.number_input("Tenure (months)", min_value=0, max_value=100, value=12, key="tenure")
    

with col2:
    InternetService = col2.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key="InternetService")
    OnlineSecurity = col2.selectbox("Online Security", ["Yes", "No", "No internet service"], key="OnlineSecurity")
    OnlineBackup = col2.selectbox("Online Backup", ["Yes", "No", "No internet service"], key="OnlineBackup")
    DeviceProtection = col2.selectbox("Device Protection", ["Yes", "No", "No internet service"], key="DeviceProtection")

with col3:
    TechSupport = col3.selectbox("Tech Support", ["Yes", "No", "No internet service"], key="TechSupport")
    StreamingTV = col3.selectbox("Streaming TV", ["Yes", "No", "No internet service"], key="StreamingTV")
    StreamingMovies = col3.selectbox("Streaming Movies", ["Yes", "No", "No internet service"], key="StreamingMovies")
    MonthlyCharges = col3.number_input("Monthly Charges", min_value=0.0, value=70.0, key="MonthlyCharges")

with col4:
    Contract = col4.selectbox("Contract", ["Month-to-month", "One year", "Two year"], key="Contract")
    PaperlessBilling = col4.selectbox("Paperless Billing", ["Yes", "No"], key="PaperlessBilling")
    PaymentMethod = col4.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        key="PaymentMethod"
    )
    TotalCharges = col4.number_input("Total Charges", min_value=0.0, value=1000.0, key="TotalCharges")
    is_long_term = col4.selectbox("Long Term Customer?", [0, 1], key="is_long_term")
    
if st.button("Predict Churn", use_container_width=True):
    payload = {
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges,
        "is_long_term": is_long_term
    }

    try:
        response = requests.post("http://api:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.session_state.prediction = result['prediction']
            st.session_state.prob = float(result['probability'])
            st.rerun()
        else:
            st.error("Error calling the API. Make sure FastAPI server is running.")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")

    


