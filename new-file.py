# Importing Dependencies
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# import prediction_model
# from prediction_model import training_pipeline
from prediction_model.predict import generate_predictions
import pandas as pd

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoanPred(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

@app.get("/")
def root():
    return {"message": "Welcome to Loan Prediction App"}

@app.post('/predict_status')
def predict_loan_status(loan_details: LoanPred):
    data = loan_details.model_dump()
    print(f"type of credit history: {type(data['Credit_History'])}")
    prediction = generate_predictions([data])['prediction'][0]
    if prediction == "Y":
        pred = "Approved"
    else :
        pred = "Rejected"
    return {"status":pred}
