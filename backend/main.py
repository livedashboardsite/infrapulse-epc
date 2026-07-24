import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

from ground_truth import get_ground_truth_tasks, get_benchmark_metrics
from cpm_engine import create_cpm_graph, calculate_cpm, recalculate_with_delays
from agents.spec_compliance import check_submittal, check_submittal_document
from agents.schedule_risk import predict_risks
from agents.supply_chain import get_live_weather, get_supply_chain_tracking
from agents.commissioning import evaluate_test_result, get_commissioning_steps
from agents.rfi_knowledge import search_rfi, get_past_rfis
from google.antigravity import Document


app = FastAPI(title="InfraPulse EPC API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve built React frontend as static files
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


class SubmittalData(BaseModel):
    submittal_name: str
    battery_runtime_minutes: int
    redundancy: str
    ups_efficiency_percent: float
    chiller_n_plus_1: bool


class TestEvaluationData(BaseModel):
    test_notes: str


class RecalculateData(BaseModel):
    delays: Dict[int, int]


@app.get("/")
async def root():
    index = FRONTEND_DIST / "index.html"
    if FRONTEND_DIST.exists() and index.exists():
        return FileResponse(index)
    return {"message": "InfraPulse EPC API — frontend not built. Run: cd frontend && npm run build"}


@app.get("/api/tasks")
async def get_tasks():
    tasks = get_ground_truth_tasks()
    G, task_dict = create_cpm_graph(tasks)
    return calculate_cpm(G, task_dict)


@app.get("/api/metrics")
async def get_metrics():
    return get_benchmark_metrics()


@app.post("/api/spec-compliance/check")
async def check_spec_compliance(submittal: SubmittalData):
    return check_submittal(submittal.model_dump())


@app.post("/api/spec-compliance/upload")
async def check_spec_compliance_upload(file: UploadFile = File(...)):
    contents = await file.read()
    if file.filename and file.filename.endswith(".pdf"):
        mime_type = "application/pdf"
    else:
        mime_type = "text/plain"

    doc = Document(content=contents, mime_type=mime_type)
    result = check_submittal_document(doc)
    return result


@app.get("/api/schedule-risks")
async def get_schedule_risks():
    tasks = get_ground_truth_tasks()
    return predict_risks(tasks)


@app.get("/api/weather")
async def get_weather():
    return await get_live_weather()


@app.get("/api/supply-chain")
async def get_supply_chain():
    return get_supply_chain_tracking()


@app.get("/api/commissioning/steps")
async def get_steps():
    return get_commissioning_steps()


@app.post("/api/commissioning/evaluate")
async def evaluate_test(data: TestEvaluationData):
    return evaluate_test_result(data.test_notes)


@app.post("/api/recalculate")
async def recalculate_schedule(data: RecalculateData):
    return recalculate_with_delays(data.delays)


@app.get("/api/rfi/search")
async def search_rfi_endpoint(query: str):
    return search_rfi(query)


@app.get("/api/rfi/all")
async def get_all_rfis():
    return get_past_rfis()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# Catch-all route: serve React SPA index.html for all non-API routes
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    index = FRONTEND_DIST / "index.html"
    if FRONTEND_DIST.exists() and index.exists():
        return FileResponse(index)
    return {"message": "Frontend not built. Run: cd frontend && npm run build"}
