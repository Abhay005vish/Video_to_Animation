from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router)

@app.get("/")
def root():
    return {"status":"Backend running successfully"}