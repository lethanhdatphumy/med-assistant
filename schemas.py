from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import date, datetime


# --------------------- PATIENT ---------------------

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Literal["Male", "Female", "Other"]
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None


class PatientCreate(PatientBase):
    medical_id: str


class PatientUpdate(BaseModel):
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None


class Patient(PatientBase):
    patient_id: int
    medical_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# --------------------- VISIT ---------------------

class VisitBase(BaseModel):
    visit_date: date
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    doctor_id: Optional[int] = None
    department_id: Optional[int] = None
    facility_id: Optional[int] = None


class VisitCreate(VisitBase):
    patient_id: int


class VisitUpdate(BaseModel):
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    doctor_id: Optional[int] = None
    department_id: Optional[int] = None
    facility_id: Optional[int] = None


class Visit(VisitBase):
    visit_id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# --------------------- TEST ---------------------

class TestBase(BaseModel):
    test_name: str
    test_date: date
    test_type: Optional[str] = None
    results: Optional[str] = None
    status: Optional[str] = None
    ordered_by: Optional[int] = None
    ordered_date: Optional[date] = None
    performed_by: Optional[int] = None


class TestCreate(TestBase):
    visit_id: int


class TestUpdate(BaseModel):
    test_name: Optional[str] = None
    test_type: Optional[str] = None
    results: Optional[str] = None
    status: Optional[str] = None
    ordered_by: Optional[int] = None
    ordered_date: Optional[date] = None
    performed_by: Optional[int] = None


class Test(TestBase):
    test_id: int
    visit_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# --------------------- PRESCRIPTION ---------------------

class PrescriptionBase(BaseModel):
    medication_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None
    prescribed_by: Optional[int] = None
    prescribed_date: date
    status: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    visit_id: int


class PrescriptionUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None
    prescribed_by: Optional[int] = None
    prescribed_date: Optional[date] = None
    status: Optional[str] = None


class Prescription(PrescriptionBase):
    prescription_id: int
    visit_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
