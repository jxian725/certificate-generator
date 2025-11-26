from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from .db import get_db, Participant
from .pdf_generator import generate_certificate
from .obs_client import upload_file

app = FastAPI()

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
            "url": participant.pdf_url
        }

    # Generate cert serial
    cert_no = f"HDC251120{str(uuid4())[:8].upper()}"

    # Create PDF
    pdf_bytes = generate_certificate(participant.name, cert_no, participant.cert_type)

    # Upload PDF to OBS
    object_name = f"certificates/{cert_no}.pdf"
    pdf_url = upload_file(pdf_bytes, object_name)

    # Save results to DB
    participant.cert_no = cert_no
    participant.cert_url = pdf_url
    db.commit()

    return {
        "id": participant.id,
        "name": participant.name,
        "cert_no": cert_no,
        "url": pdf_url
    }
