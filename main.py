import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.database import init_db
from backend.seed_data import seed_database
from backend.routes import router as api_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        seed_database()
    except Exception as e:
        print(f"Notice during lifespan startup: {e}")
    yield

app = FastAPI(
    title="Intelligent Land Record Digitization and Validation System",
    description="Govt of India - Ministry of Rural Development | AI-Powered Land Records & Dispute Manager",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router)

# Mount frontend static files
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
@app.get("/index.html")
def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Land Dispute Manager API is running. Access /api/health or /docs for API documentation."}

@app.get("/landing")
@app.get("/overview")
def serve_landing():
    landing_path = os.path.join(frontend_dir, "landing.html")
    if os.path.exists(landing_path):
        return FileResponse(landing_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)

@app.on_event("startup")
def startup_event():
    try:
        init_db()
        seed_database()
    except Exception as e:
        print(f"Notice during startup_event: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Land Dispute Manager on http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
