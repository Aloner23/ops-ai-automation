from __future__ import annotations

from typing import Protocol

from app.domain import Decision, Intake, ProposedAction


class AutomationEngine(Protocol):
    """Boundary for a future LLM or enterprise automation provider."""

    def decide(self, intake: Intake) -> Decision: ...


class DemoAutomationEngine:
    """Deterministic engine for a reproducible, credential-free demo.

    A production adapter can implement AutomationEngine and return the same
    schema after calling an LLM. The policy checks below stay server-side.
    """

    def decide(self, intake: Intake) -> Decision:
        text = intake.text.lower()
        if any(word in text for word in ("pago", "factura", "cobro")):
            return Decision(
                category="finance_ops",
                summary="Se detectó una solicitud financiera que requiere revisión humana antes de cualquier movimiento.",
                confidence=0.92,
                risk="high",
                proposed_actions=[
                    ProposedAction(
                        action="Crear borrador de conciliación y adjuntar evidencia",
                        owner="finanzas",
                        due_in_hours=4,
                        reason="Las acciones de pago no se ejecutan automáticamente.",
                    )
                ],
                requires_human_approval=True,
            )
        if any(word in text for word in ("reserva", "evento", "espacio")):
            return Decision(
                category="reservation_ops",
                summary="Solicitud de reserva clasificada; se propone una respuesta y una tarea de disponibilidad.",
                confidence=0.89,
                risk="medium",
                proposed_actions=[
                    ProposedAction(
                        action="Consultar disponibilidad y preparar propuesta",
                        owner="operaciones",
                        due_in_hours=2,
                        reason="La reserva solo se confirma después de validar agenda y condiciones.",
                    )
                ],
                requires_human_approval=True,
            )
        return Decision(
            category="general_ops",
            summary="Solicitud clasificada para seguimiento operativo; no se detectó una acción irreversible.",
            confidence=0.74,
            risk="low",
            proposed_actions=[
                ProposedAction(
                    action="Crear tarea de seguimiento con contexto resumido",
                    owner="operaciones",
                    due_in_hours=8,
                    reason="La persona responsable conserva el control de la respuesta final.",
                )
            ],
            requires_human_approval=True,
        )
