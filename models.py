from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "emr_patients"

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    medical_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum("Male", "Female", "Other"), nullable=False)
    address = Column(Text, nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    visits = relationship("Visit", back_populates="patient")


class Visit(Base):
    __tablename__ = "emr_visits"

    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("emr_patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, nullable=True)
    department_id = Column(Integer, nullable=True)
    facility_id = Column(Integer, nullable=True)
    visit_date = Column(Date, nullable=False)
    symptoms = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    patient = relationship("Patient", back_populates="visits")
    prescriptions = relationship("Prescription", back_populates="visit")
    tests = relationship("Test", back_populates="visit")


class Prescription(Base):
    __tablename__ = "emr_prescriptions"

    prescription_id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("emr_visits.visit_id"), nullable=False)
    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=True)
    frequency = Column(String(50), nullable=True)
    duration = Column(String(50), nullable=True)
    instructions = Column(Text, nullable=True)
    prescribed_by = Column(Integer, nullable=True)
    prescribed_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    visit = relationship("Visit", back_populates="prescriptions")


class Test(Base):
    __tablename__ = "emr_tests"

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey("emr_visits.visit_id"), nullable=False)
    test_name = Column(String(100), nullable=False)
    test_type = Column(String(50), nullable=True)
    ordered_by = Column(Integer, nullable=True)
    ordered_date = Column(Date, nullable=False)
    performed_date = Column(Date, nullable=True)
    results = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    visit = relationship("Visit", back_populates="tests")
