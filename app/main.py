import uvicorn
from core.config import settings
from fastapi import FastAPI
from api.router import router as api_router

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
