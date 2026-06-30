const DATA_SOURCES = {
  dashboard: [
    './data/executive_dashboard.json',
    '../evidence/generated/executive_dashboard.json',
    '/evidence/generated/executive_dashboard.json',
  ],
  manifest: [
    './data/evidence_manifest.json',
    '../evidence/generated/evidence_manifest.json',
    '/evidence/generated/evidence_manifest.json',
  ],
  companion: [
    './data/ai_governance_companion_export_summary.json',
    '../evidence/generated/ai_governance_companion_export_summary.json',
    '/evidence/generated/ai_governance_companion_export_summary.json',
  ],
};

async function fetchFirstAvailable(paths) {
  const errors = [];
  for (const path of paths) {
    try {
      const response = await fetch(path, { cache: 'no-store' });
      if (!response.ok) {
        errors.push(`${path}: ${response.status}`);
        continue;
      }
      const contentType = response.headers.get('content-type') || '';
      const payload = await response.text();
      if (contentType.includes('text/html') || payload.trim().startsWith('<')) {
        errors.push(`${path}: returned HTML instead of JSON`);
        continue;
      }
      return JSON.parse(payload);
    } catch (error) {
      errors.push(`${path}: ${error.message}`);
    }
  }
  throw new Error(errors.join('; '));
}

function el(selector) {
  return document.querySelector(selector);
}

function formatValue(value) {
  if (typeof value === 'number') {
    return Number.isInteger(value) ? value.toLocaleString() : value.toFixed(2);
  }
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }
  return value ?? 'n/a';
}

function severityClass(severity) {
  return ['critical', 'warning', 'healthy'].includes(severity) ? severity : 'warning';
}

function renderKpis(kpis) {
  el('#kpi-grid').innerHTML = kpis
    .map(
      (kpi) => `
        <article class="kpi-card">
          <div class="label">${kpi.label}</div>
          <div class="value">${formatValue(kpi.value)}</div>
          <span class="severity ${severityClass(kpi.severity)}">${kpi.severity}</span>
        </article>
      `,
    )
    .join('');
}

function metricRow(label, value) {
  return `<div class="metric-row"><span>${label}</span><span>${formatValue(value)}</span></div>`;
}

function renderTopRisk(topRisk) {
  if (!topRisk) {
    el('#top-risk-card').innerHTML = '<p>No top risk subject found.</p>';
    return;
  }

  el('#top-risk-card').innerHTML = `
    <div class="metric-list">
      ${metricRow('Subject ID', topRisk.subject_id)}
      ${metricRow('Subject type', topRisk.subject_type)}
      ${metricRow('Composite score', topRisk.composite_score)}
      ${metricRow('Priority', topRisk.priority_level)}
      ${metricRow('Decision', topRisk.decision)}
      ${metricRow('Signal count', topRisk.signal_count)}
    </div>
    <div class="signal-list">
      ${(topRisk.signal_types || []).map((signal) => `<span class="pill">${signal}</span>`).join('')}
    </div>
  `;
}

function renderEvidenceHealth(evidenceHealth) {
  el('#evidence-health').innerHTML = [
    metricRow('Validation status', evidenceHealth.validation_status),
    metricRow('Artifact count', evidenceHealth.artifact_count),
    metricRow('Audit-chain events', evidenceHealth.audit_chain_events),
    metricRow('Authority', evidenceHealth.authority),
  ].join('');
}

function renderRiskCards(cards) {
  el('#risk-cards').innerHTML = cards
    .map(
      (card, index) => `
        <article class="risk-card">
          <div class="risk-card-header">
            <div>
              <h3>${index + 1}. ${card.subject_id}</h3>
              <div class="risk-meta">${card.subject_type} · score ${card.composite_score} · ${card.signal_count} signal(s)</div>
            </div>
            <span class="severity ${severityClass(card.priority_level)}">${card.decision}</span>
          </div>
          <div class="reason-list">
            ${(card.executive_reasons || []).map((reason) => `<span class="pill">${reason}</span>`).join('')}
          </div>
        </article>
      `,
    )
    .join('');
}

function renderRecommendations(recommendations) {
  el('#recommendations').innerHTML = recommendations
    .slice(0, 10)
    .map(
      (item) => `
        <div class="recommendation-item">
          <strong>${item.recommended_control}</strong>
          <span>${item.subject_id} · ${item.subject_type} · ${item.priority_level} · ${item.decision}</span>
        </div>
      `,
    )
    .join('');
}

function renderCompanionExport(summary) {
  el('#companion-export').innerHTML = [
    metricRow('Contract version', summary.contract_version),
    metricRow('Export type', summary.export_type),
    metricRow('Top risk subject', summary.top_risk_subject_id),
    metricRow('Top risk decision', summary.top_risk_decision),
    metricRow('Total risk subjects', summary.total_risk_subjects),
    metricRow('Repo merge required', summary.repo_merge_required),
    metricRow('Codebase dependency required', summary.codebase_dependency_required),
    metricRow('Evidence validation', summary.evidence_validation_status),
  ].join('');
}

function renderArtifacts(manifest) {
  el('#artifact-list').innerHTML = (manifest.artifacts || [])
    .map(
      (artifact) => `
        <div class="artifact-item">
          <strong>${artifact}</strong>
          <span>${manifest.evidence_mode} · ${manifest.authority}</span>
        </div>
      `,
    )
    .join('');
}

function renderError(error) {
  document.querySelector('main').innerHTML = `
    <section class="error-panel">
      <h2>Dashboard evidence could not be loaded</h2>
      <p>${error.message}</p>
      <p>Run <code>python scripts/generate_evidence.py</code>, then serve the repository root with <code>python -m http.server 8080</code> and open <code>/frontend/</code>.</p>
    </section>
  `;
  const dot = document.querySelector('.status-dot');
  dot.classList.add('error');
  el('#evidence-status').textContent = 'Evidence load failed';
}

async function boot() {
  try {
    const [dashboard, manifest, companion] = await Promise.all([
      fetchFirstAvailable(DATA_SOURCES.dashboard),
      fetchFirstAvailable(DATA_SOURCES.manifest),
      fetchFirstAvailable(DATA_SOURCES.companion),
    ]);

    renderKpis(dashboard.kpis || []);
    renderTopRisk(dashboard.summary?.top_risk_subject);
    renderEvidenceHealth(dashboard.evidence_health || {});
    renderRiskCards(dashboard.top_risk_cards || []);
    renderRecommendations(dashboard.control_recommendations || []);
    renderCompanionExport(companion || {});
    renderArtifacts(manifest || {});

    el('#generated-at').textContent = `Generated at: ${dashboard.generated_at || manifest.generated_at || 'unknown'}`;
    el('#evidence-status').textContent = `${dashboard.authority || 'advisory_only'} evidence loaded`;
    document.querySelector('.status-dot').classList.add('ready');
  } catch (error) {
    renderError(error);
  }
}

boot();
