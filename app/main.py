from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import contact

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Database Connected Successfully and Api is working"}