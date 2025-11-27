from fastapi import FastAPI, HTTPException, Depends, Request
from pdf2image import convert_from_bytes
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from io import BytesIO
from .db import get_db
from .pdf_generator import generate_certificate
from .obs_client import upload_file
from .models import ParticipantQuery, Participant

app = FastAPI()

@app.options("/participant/query")
async def options_handler(request: Request):
    return {}

@app.post("/participant/query")
async def query_participant(filters: ParticipantQuery, db: Session = Depends(get_db)):
    # Ensure at least one identifier exists
    if not any([filters.name, filters.email, filters.accountId]):
        raise HTTPException(status_code=400, detail="Provide name, email, or accountId")

    db_query = db.query(Participant).filter(Participant.country == filters.country)

    if filters.email:
        db_query = db_query.filter(Participant.email == filters.email)
    elif filters.name:
        db_query = db_query.filter(Participant.name == filters.name)
    elif filters.accountId:
        db_query = db_query.filter(Participant.huawei_id == filters.accountId)

    result = db_query.first()

    if not result:
        return {"status": "not_found", "message": "No matching record found"}

    return {
        "status": "success",
        "data": {
            "id": result.id,
            "name": result.name,
            "country": result.country,
            "entity": result.entity
        }
    }

@app.post("/generate/{participant_id}")
async def generate_cert(participant_id: int, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.id == participant_id).first()

    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    # If cert already exists, return saved one
    if participant.pdf_url:
        return {
            "message": "Certificate already generated",
            "name": participant.name,
            "cert_no": participant.cert_no,
            "url": participant.pdf_url,
            "blob": participant.cert_blob
        }

    # Generate cert serial
    cert_no = f"HDC251120{str(uuid4())[:8].upper()}"

    # Create PDF
    pdf_bytes = generate_certificate(participant.name, cert_no, participant.cert_type)

    # PDF to IMG
    images = convert_from_bytes(pdf_bytes)
    img_byte_arr = BytesIO()
    images[0].save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()

    # Upload PDF to OBS
    object_name = f"certificates/{cert_no}.pdf"
    pdf_url = upload_file(pdf_bytes, object_name)

    # Save results to DB
    participant.cert_no = cert_no
    participant.pdf_url = pdf_url
    participant.cert_blob = img_bytes
    participant.issued_at = datetime.now()
    db.commit()

    return {
        "message": "Certificate generated successfully",
        "name": participant.name,
        "cert_no": cert_no,
        "url": pdf_url,
        "blob": img_bytes
    }
