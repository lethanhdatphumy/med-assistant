from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Test as TestModel, Visit as VisitModel
from schemas import TestCreate, Test, TestUpdate
from typing import List

router = APIRouter()


@router.post("/", response_model=Test)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    visit = db.query(VisitModel).filter(VisitModel.visit_id == test.visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    new_test = TestModel(**test.dict())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


@router.get("/{test_id}", response_model=Test)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.put("/{test_id}", response_model=Test, response_model_exclude_unset=True)
def update_test(test_id: int, test: TestUpdate, db: Session = Depends(get_db)):
    db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    for key, value in test.dict(exclude_unset=True).items():
        setattr(db_test, key, value)
    db.commit()
    db.refresh(db_test)
    return db_test


@router.delete("/{test_id}", status_code=204)
def delete_test(test_id: int, db: Session = Depends(get_db)):
    db_test = db.query(TestModel).filter(TestModel.test_id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(db_test)
    db.commit()
    return None


@router.get("/", response_model=List[Test])
def list_tests(db: Session = Depends(get_db)):
    return db.query(TestModel).all()
