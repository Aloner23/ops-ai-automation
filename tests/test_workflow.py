from app.domain import Intake, RunStatus
from app.engine import DemoAutomationEngine
from app.service import WorkflowService


def test_financial_request_requires_human_approval_and_redacts_email() -> None:
    service = WorkflowService(DemoAutomationEngine())
    run = service.process(Intake(requester="Ventas", text="Factura de pago: vendor@example.com"))

    assert run.status is RunStatus.NEEDS_APPROVAL
    assert run.decision.risk == "high"
    assert "vendor@example.com" not in run.public_dict()["input"]["text"]


def test_approval_is_a_distinct_human_step() -> None:
    service = WorkflowService(DemoAutomationEngine())
    run = service.process(Intake(requester="Ventas", text="Reserva de terraza para evento"))

    assert run.status is RunStatus.NEEDS_APPROVAL
    approved = service.approve(run.audit_id)
    assert approved.status is RunStatus.APPROVED
