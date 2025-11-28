from fastapi import FastAPI, Form
from pydantic import BaseModel
import pandas as pd
import pickle


import os
import pickle

# Get the directory where this script is located, then navigate to project root
current_file = os.path.abspath(__file__)
src_dir = os.path.dirname(current_file)
project_root = os.path.dirname(os.path.dirname(src_dir))

models_path = os.path.join(project_root, "models")

encoders_path = os.path.join(models_path, "encoder.pkl")
scaler_path = os.path.join(models_path, "scaler.pkl")
Random_Forest_path = os.path.join(models_path, "Random_Forest.pkl")


# Load the model
with open(Random_Forest_path, "rb") as f:
    loaded_model = pickle.load(f)
with open(encoders_path, 'rb') as encoders_file:
    encoders = pickle.load(encoders_file)
with open(scaler_path, 'rb') as scaler_file:
    scaler_data = pickle.load(scaler_file)

# Initialize FastAPI app
app = FastAPI()

def make_prediction(input_data):
    input_df = pd.DataFrame([input_data])

    for col, encoder in encoders.items():
        input_df[col] = encoder.transform(input_df[col])

    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    input_df[numerical_cols] = scaler_data.transform(input_df[numerical_cols])

    prediction = loaded_model.predict(input_df)[0]
    probability = loaded_model.predict_proba(input_df)[0, 1]
    return "Churn" if prediction == 1 else "No Churn", probability

class PredictionRequest(BaseModel):
    
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float
    is_long_term: int

@app.post("/predict")
async def predict(data: PredictionRequest):
    input_data = data.dict()
    prediction, probability = make_prediction(input_data)
    return {"prediction": prediction, "probability": probability}
