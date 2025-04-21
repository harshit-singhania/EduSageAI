from fastapi import FastAPI
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    prefix=settings.API_V1_STR,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/healthcheck") 
async def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
    
# to run the server, use the command: 
# uvicorn app.main:app --host 