from __future__ import annotations

from app.domain import Intake, RunStatus, WorkflowRun, new_audit_id
from app.engine import AutomationEngine


class WorkflowService:
    def __init__(self, engine: AutomationEngine):
        self.engine = engine
        self.runs: dict[str, WorkflowRun] = {}

    def process(self, intake: Intake) -> WorkflowRun:
        decision = self.engine.decide(intake)
        status = RunStatus.BLOCKED if decision.confidence < 0.7 else RunStatus.NEEDS_APPROVAL
        run = WorkflowRun(intake=intake, decision=decision, status=status, audit_id=new_audit_id())
        self.runs[run.audit_id] = run
        return run

    def approve(self, audit_id: str) -> WorkflowRun:
        run = self.runs[audit_id]
        if run.status is RunStatus.BLOCKED:
            raise ValueError("A low-confidence decision cannot be approved automatically.")
        run.status = RunStatus.APPROVED
        return run
