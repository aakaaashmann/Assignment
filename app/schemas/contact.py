from pydantic import BaseModel, model_validator
from typing import Optional, List

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

    @model_validator(mode="after")
    def validate_at_least_one(cls, values):
        if not values.email and not values.phoneNumber:
            raise ValueError("At least one of email or phoneNumber must be provided")
        return values


class ContactResponse(BaseModel):
    primaryContatctId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

class IdentifyResponse(BaseModel):
    contact: ContactResponse