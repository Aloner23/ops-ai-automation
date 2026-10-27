const form = document.querySelector('#intake-form');
const state = document.querySelector('#state');
const summary = document.querySelector('#summary');
const details = document.querySelector('#details');
const approve = document.querySelector('#approve');
let auditId = null;

document.querySelectorAll('[data-example]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelector('#text').value = button.dataset.example === 'finance'
      ? 'Llegó una factura pendiente de pago por mantenimiento. Contacto: proveedor@ejemplo.com'
      : 'Necesitamos reservar la terraza para un evento el próximo viernes. Contacto: cliente@ejemplo.com';
  });
});

function render(run) {
  auditId = run.audit_id;
  state.textContent = run.status === 'approved' ? 'Acción aprobada' : 'Requiere aprobación humana';
  summary.textContent = run.decision.summary;
  details.hidden = false;
  details.innerHTML = `
    <dl>
      <div><dt>Riesgo</dt><dd>${run.decision.risk}</dd></div>
      <div><dt>Confianza</dt><dd>${Math.round(run.decision.confidence * 100)}%</dd></div>
      <div><dt>Auditoría</dt><dd>${run.audit_id}</dd></div>
    </dl>
    <p><strong>Acción:</strong> ${run.decision.proposed_actions[0].action}</p>
    <p class="muted">${run.decision.proposed_actions[0].reason}</p>`;
  approve.hidden = run.status === 'approved';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  state.textContent = 'Analizando con políticas…';
  const response = await fetch('/api/runs', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({requester: requester.value, text: text.value})});
  render(await response.json());
});

approve.addEventListener('click', async () => {
  const response = await fetch(`/api/runs/${auditId}/approve`, {method: 'POST'});
  render(await response.json());
});
