from fastapi import FastAPI
from config import settings
from backend.routes import router

app = FastAPI(title=f"{settings.APP_NAME} API")
app.include_router(router)


@app.get("/")
def home():
    return {"message": f"{settings.APP_NAME} API is running"}