from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Visit as VisitModel, Patient as PatientModel
from schemas import VisitCreate, Visit, VisitUpdate
from typing import List

router = APIRouter()


@router.post("/", response_model=Visit)
def create_visit(visit: VisitCreate, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.patient_id == visit.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    new_visit = VisitModel(**visit.dict())
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit


@router.get("/{visit_id}", response_model=Visit)
def get_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(VisitModel).filter(VisitModel.visit_id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.put("/{visit_id}", response_model=Visit, response_model_exclude_unset=True)
def update_visit(visit_id: int, visit: VisitUpdate, db: Session = Depends(get_db)):
    db_visit = db.query(VisitModel).filter(VisitModel.visit_id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    for key, value in visit.dict(exclude_unset=True).items():
        setattr(db_visit, key, value)
    db.commit()
    db.refresh(db_visit)
    return db_visit


@router.delete("/{visit_id}", status_code=204)
def delete_visit(visit_id: int, db: Session = Depends(get_db)):
    db_visit = db.query(VisitModel).filter(VisitModel.visit_id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    db.delete(db_visit)
    db.commit()
    return None


@router.get("/", response_model=List[Visit])
def list_visits(db: Session = Depends(get_db)):
    return db.query(VisitModel).all()
