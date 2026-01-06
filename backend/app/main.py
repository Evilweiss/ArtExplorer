from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.paintings import router as paintings_router

app = FastAPI(title="Art Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)

app.include_router(paintings_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
