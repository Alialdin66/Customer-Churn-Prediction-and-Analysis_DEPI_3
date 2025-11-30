from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import os

current_file = os.path.abspath(__file__)
src_dir = os.path.dirname(current_file)
project_root = os.path.dirname(os.path.dirname(src_dir))

models_path = os.path.join(project_root, "models")

XGBoost_path = os.path.join(models_path, "XGBoost.pkl")
with open(XGBoost_path, "rb") as f:
    loaded_model = pickle.load(f)

app = FastAPI()

def make_prediction(input_data: dict):
    input_df = pd.DataFrame([input_data])
    prediction = loaded_model.predict(input_df)[0]
    probability = loaded_model.predict_proba(input_df)[0, 1]
    return "Churn" if prediction == 1 else "No Churn", float(probability)


class PredictionRequest(BaseModel):
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
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
    return {"prediction": prediction, "probability": float(probability)}


