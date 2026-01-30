from fastapi import FastAPI
from app.api.endpoints import registration, login, jobs
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="Document QnA API",
    version="1.0.0",
    description="Authentication and Document Q&A service"
)

@app.get("/", tags=["Root"])
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Document QnA API"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


app.include_router(registration.router)
app.include_router(login.router)
app.include_router(jobs.router)
