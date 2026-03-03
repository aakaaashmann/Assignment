from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import contact
from app.api.identify import router as identify_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(identify_router)

@app.get("/")
def root():
    return {"message": "Database Connected Successfully and Api is working"}