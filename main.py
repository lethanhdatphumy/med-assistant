from fastapi import FastAPI, HTTPException, status
from database import SessionLocal, engine
from routers import patients, visits, tests, chat
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(visits.router, prefix="/visits", tags=["Visits"])
app.include_router(tests.router, prefix="/tests", tags=["Tests"])

app.include_router(chat.router, prefix="/chat", tags=["Chat"])