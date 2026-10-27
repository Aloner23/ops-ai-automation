from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.domain import Intake
from app.engine import DemoAutomationEngine
from app.service import WorkflowService

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Ops AI Automation", version="0.1.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
service = WorkflowService(DemoAutomationEngine())


class IntakeRequest(BaseModel):
    requester: str = Field(min_length=2, max_length=80)
    text: str = Field(min_length=12, max_length=1000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": "deterministic-demo", "external_ai_calls": False}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/runs")
def create_run(payload: IntakeRequest) -> dict:
    return service.process(Intake(text=payload.text, requester=payload.requester)).public_dict()


@app.post("/api/runs/{audit_id}/approve")
def approve_run(audit_id: str) -> dict:
    try:
        return service.approve(audit_id).public_dict()
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Workflow run not found") from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
