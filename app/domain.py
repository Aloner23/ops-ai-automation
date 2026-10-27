from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from uuid import uuid4


class RunStatus(str, Enum):
    NEEDS_APPROVAL = "needs_approval"
    APPROVED = "approved"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class Intake:
    text: str
    requester: str


@dataclass(frozen=True)
class ProposedAction:
    action: str
    owner: str
    due_in_hours: int
    reason: str


@dataclass(frozen=True)
class Decision:
    category: str
    summary: str
    confidence: float
    risk: str
    proposed_actions: list[ProposedAction]
    requires_human_approval: bool


@dataclass
class WorkflowRun:
    intake: Intake
    decision: Decision
    status: RunStatus
    audit_id: str

    def public_dict(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "status": self.status,
            "input": {"requester": self.intake.requester, "text": redact(self.intake.text)},
            "decision": {
                **asdict(self.decision),
                "proposed_actions": [asdict(action) for action in self.decision.proposed_actions],
            },
        }


def new_audit_id() -> str:
    return f"AUD-{uuid4().hex[:8].upper()}"


def redact(value: str) -> str:
    """Avoid writing email addresses to the automation audit trail."""
    words = []
    for word in value.split():
        words.append("[redacted-email]" if "@" in word else word)
    return " ".join(words)
