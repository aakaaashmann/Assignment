🚀 Live API URL
https://assignment-xeaw.onrender.com
📌 Swagger Documentation
https://assignment-xeaw.onrender.com/docs

API Endpoint
POST /identify
Request Body
{
  "email": "string (optional)",
  "phoneNumber": "string (optional)"
}
 At least one of email or phoneNumber must be provided.

Response Format
{
  "contact": {
    "primaryContatctId": number,
    "emails": ["string"],
    "phoneNumbers": ["string"],
    "secondaryContactIds": [number]
  }
}

How Identity Reconciliation Works:
    Contacts are linked if they share email OR phoneNumber
    The oldest contact becomes the primary
    All others become secondary
    If new information is provided, a new secondary record is created
    All operations are wrapped inside a database transaction to ensure atomicity

Tech Stack
FastAPI
PostgreSQL (Render)
SQLAlchemy
Uvicorn
Hosted on Render