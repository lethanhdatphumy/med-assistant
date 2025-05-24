from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Patient as PatientModel
from schemas import PatientCreate, Patient, PatientUpdate
from typing import List

router = APIRouter()


@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(PatientModel).filter(PatientModel.medical_id == patient.medical_id).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Patient with this medical ID already exists")
    new_patient = PatientModel(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=Patient, response_model_exclude_unset=True)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(PatientModel).filter(PatientModel.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(PatientModel).filter(PatientModel.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return None


@router.get("/", response_model=List[Patient])
def list_patients(db: Session = Depends(get_db)):
    return db.query(PatientModel).all()
