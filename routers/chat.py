from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import Patient, Visit, Test
from dotenv import load_dotenv
import openai
import os
import re
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment variables.")

logging.basicConfig(level=logging.ERROR)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_with_gpt(request: ChatRequest, db: Session = Depends(get_db)):
    user_input = request.message.lower()

    patient_data = ""
    visit_info = ""
    test_info = ""

    patient_match = re.search(r'\bpatient\s+(\d+)\b', user_input)
    visit_match = re.search(r'\bvisit\s+(\d+)\b', user_input)
    test_match = re.search(r'\btest\s+(\d+)\b', user_input)

    try:
        if patient_match:
            patient_id = int(patient_match.group(1))
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if patient:
                patient_data = (
                    f"Patient ID: {patient.patient_id}, "
                    f"Name: {patient.first_name} {patient.last_name}, "
                    f"Date of Birth: {patient.date_of_birth}, "
                    f"Gender: {patient.gender}\n"
                )
            else:
                patient_data = "No patient found with that ID.\n"

        if visit_match:
            visit_id = int(visit_match.group(1))
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            if visit:
                visit_info = (
                    f"Visit ID: {visit.visit_id}, "
                    f"Date: {visit.visit_date}, "
                    f"Symptoms: {visit.symptoms}, "
                    f"Diagnosis: {visit.diagnosis}, "
                    f"Notes: {visit.notes}, "
                    f"Status: {visit.status}\n"
                )
            else:
                visit_info = "No visit found with that ID.\n"

        if test_match:
            test_id = int(test_match.group(1))
            test = db.query(Test).filter(Test.test_id == test_id).first()
            if test:
                test_info = (
                    f"Test ID: {test.test_id}, "
                    f"Test Name: {test.test_name}, "
                    f"Result: {test.results}, "
                    f"Status: {test.status}\n"
                )
            else:
                test_info = "No test found with that ID.\n"

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred.") from e

    full_context = "\n".join(filter(None, [patient_data, visit_info, test_info]))

    system_prompt = "You are a medical assistant chatbot. Use the patient data provided if available."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{full_context}\n{user_input}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        bot_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with OpenAI API.") from e

    return {"response": bot_response}