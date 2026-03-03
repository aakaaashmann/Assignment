from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.contact import IdentifyRequest, IdentifyResponse
from app.services.identity_service import identify_contact
from app.core.database import get_db

router = APIRouter()

@router.post("/identify", response_model=IdentifyResponse)
def identify(request: IdentifyRequest, db: Session = Depends(get_db)):
    return identify_contact(db, request.email, request.phoneNumber)