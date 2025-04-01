from fastapi import FastAPI
from routers import api


# Initialize FastAPI app with documentation
app = FastAPI(
    title="Document Extraction API",
    description="API for extracting text from various document formats and processing data",
    version="1.0.0",
)


# Register the extractors router
app.include_router(api.router)
