# Ops AI Automation

Demostración full-stack de cómo aplicar IA a solicitudes operativas sin delegar decisiones sensibles a un modelo: clasifica contexto, propone pasos, aplica reglas deterministas, pide aprobación humana y deja una traza de auditoría.

> **Modo demo reproducible:** el motor actual es determinista y no hace llamadas externas ni requiere una clave. La interfaz `AutomationEngine` permite sustituirlo por un proveedor de IA en un backend seguro, sin exponer secretos al navegador.

## Qué demuestra

- API en FastAPI y una interfaz web ligera para ejecutar el flujo de punta a punta.
- Separación entre interpretación, reglas de negocio y ejecución.
- Human-in-the-loop: ninguna acción propuesta se aprueba automáticamente.
- Redacción de correos del registro público de auditoría.
- Pruebas para riesgo financiero, privacidad y paso de aprobación.

## Ejecutar

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Abre `http://127.0.0.1:8000`. Ejecuta pruebas con `pytest`.

## Integración futura

Un proveedor de IA real debe vivir detrás del backend e implementar `AutomationEngine`; la clave se configura solo como variable del entorno del servidor. Las políticas, validaciones y aprobación humana permanecen fuera del proveedor.
