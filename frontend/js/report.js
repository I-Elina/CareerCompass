document.addEventListener('DOMContentLoaded', async () => {
  const loadingOverlay = document.getElementById('loading-overlay');
  const webDashboard = document.getElementById('web-dashboard') || document.getElementById('report-content');

  // Read from storage safely
  const rawPayload =
    sessionStorage.getItem('assessment_payload') ||
    localStorage.getItem('assessment_payload');

  if (!rawPayload) {
    alert('No assessment data found. Redirecting to start...');
    window.location.href = 'assesment.html';
    return;
  }

  let payload = {};
  try {
    payload = JSON.parse(rawPayload);
  } catch (err) {
    console.error('Payload parse failed:', err);
    payload = { name: 'Candidate' };
  }

  // Load cached report on page refresh
  const existingReport =
    sessionStorage.getItem('careerReport') ||
    localStorage.getItem('careerReport');

  if (existingReport) {
    try {
      const parsed = JSON.parse(existingReport);
      renderAll(parsed, payload.name || 'Candidate');
      if (loadingOverlay) loadingOverlay.style.display = 'none';
      if (webDashboard) webDashboard.style.display = 'block';
      return;
    } catch (e) {}
  }

  // Start loader
  const loaderController = startInteractiveLoader();

  try {
    const res = await fetch('http://127.0.0.1:5000/api/analyze-career', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    const data = await res.json();
    sessionStorage.setItem('careerReport', JSON.stringify(data));
    localStorage.setItem('careerReport', JSON.stringify(data));

    loaderController.complete();

    setTimeout(() => {
      renderAll(data, payload.name || 'Candidate');
      if (loadingOverlay) loadingOverlay.style.display = 'none';
      if (webDashboard) webDashboard.style.display = 'block';
    }, 400);

  } catch (err) {
    console.error(err);
    loaderController.fail();
  }
});

function startInteractiveLoader() {
  const progressBar = document.getElementById('progress-bar');
  const statusElem = document.getElementById('loading-status');
  const stepElem = document.getElementById('step-indicator');
  const factElem = document.getElementById('dynamic-fact');

  const steps = [
    { p: 25, s: 'Step 1 of 4', t: 'Analyzing profile strengths & technical background...' },
    { p: 50, s: 'Step 2 of 4', t: 'Mapping high-growth career tracks & skill gaps...' },
    { p: 75, s: 'Step 3 of 4', t: 'Curating specialized degrees, colleges & delivery modes...' },
    { p: 95, s: 'Step 4 of 4', t: 'Synthesizing executive verdict & roadmap...' }
  ];

  let idx = 0;
  const iv = setInterval(() => {
    if (idx < steps.length) {
      if (progressBar) progressBar.style.width = `${steps[idx].p}%`;
      if (statusElem) statusElem.textContent = steps[idx].t;
      if (stepElem) stepElem.textContent = steps[idx].s;
      idx++;
    }
  }, 2500);

  return {
    complete: () => {
      clearInterval(iv);
      if (progressBar) progressBar.style.width = '100%';
    },
    fail: () => {
      clearInterval(iv);
      if (statusElem) {
        statusElem.textContent = 'Server connection error. Please verify backend.';
        statusElem.style.color = '#fb7185';
      }
    }
  };
}

function renderAll(report, candidateName) {
  /* 1. Render Screen Dashboard */
  const webName = document.getElementById('web-candidate-name') || document.getElementById('user-heading');
  const webSummary = document.getElementById('web-profile-summary') || document.getElementById('profile-summary');
  if (webName) webName.textContent = `Career Blueprint for ${candidateName}`;
  if (webSummary) webSummary.textContent = report.career_profile || '';

  const webPaths = document.getElementById('web-career-paths') || document.getElementById('career-paths-grid');
  if (webPaths) {
    webPaths.innerHTML = '';
    (report.career_paths || []).forEach((p) => {
      const card = document.createElement('div');
      card.className = 'glass-card career-card';
      const r = Array.isArray(p.roles) ? p.roles.join(', ') : p.roles || '';
      const g = Array.isArray(p.skill_gaps) ? p.skill_gaps.join(', ') : p.skill_gaps || '';
      card.innerHTML = `
        <h3>${p.title}</h3>
        <p>${p.fit_reason || ''}</p>
        <span class="tag-label">Target Roles</span>
        <div style="margin:4px 0 8px; color:#e2e8f0; font-size:0.85rem;">${r}</div>
        <span class="tag-label" style="color:#fb7185; background:rgba(244,63,94,0.1);">Key Skill Gaps</span>
        <div style="margin-top:4px; color:#fda4af; font-size:0.85rem;">${g}</div>
      `;
      webPaths.appendChild(card);
    });
  }

  const webSkills = document.getElementById('web-skills-list') || document.getElementById('skills-list');
  if (webSkills) {
    webSkills.innerHTML = `<ul style="list-style:none; padding:0; color:#cbd5e1; font-size:0.9rem;">
      ${(report.skills_to_learn || []).map((s) => `<li style="margin-bottom:6px;">▸ ${s}</li>`).join('')}
    </ul>`;
  }

  const webEdu = document.getElementById('web-education-pathway') || document.getElementById('education-pathway');
  if (webEdu) {
    const deg = Array.isArray(report.recommended_degrees) ? report.recommended_degrees.join(', ') : report.recommended_degrees;
    const col = Array.isArray(report.recommended_colleges) ? report.recommended_colleges.join(', ') : report.recommended_colleges;
    webEdu.innerHTML = `
      <p style="color:#f8fafc; font-weight:600; font-size:0.9rem; margin-bottom:2px;">Degrees:</p>
      <p style="color:#94a3b8; font-size:0.88rem; margin-bottom:10px;">${deg || 'N/A'}</p>
      <p style="color:#f8fafc; font-weight:600; font-size:0.9rem; margin-bottom:2px;">Colleges / Delivery:</p>
      <p style="color:#94a3b8; font-size:0.88rem;">${col || 'N/A'}</p>
    `;
  }

  const webShort = document.getElementById('web-short-plan') || document.getElementById('short-term-plan');
  const webLong = document.getElementById('web-long-plan') || document.getElementById('long-term-plan');
  const webVerdict = document.getElementById('web-verdict') || document.getElementById('overall-verdict');
  if (webShort) webShort.textContent = report.short_term_plan || '';
  if (webLong) webLong.textContent = report.long_term_plan || '';
  if (webVerdict) webVerdict.textContent = report.overall_summary || '';

  /* 2. Render Print-Only Document */
  const docName = document.getElementById('doc-name');
  const docSummary = document.getElementById('doc-summary');
  if (docName) docName.textContent = candidateName;
  if (docSummary) docSummary.textContent = report.career_profile || '';

  const docPaths = document.getElementById('doc-paths-list');
  if (docPaths) {
    docPaths.innerHTML = '';
    (report.career_paths || []).forEach((p, idx) => {
      const entry = document.createElement('div');
      entry.className = 'doc-path-entry';
      const r = Array.isArray(p.roles) ? p.roles.join(', ') : p.roles || 'N/A';
      const g = Array.isArray(p.skill_gaps) ? p.skill_gaps.join(', ') : p.skill_gaps || 'N/A';
      entry.innerHTML = `
        <div class="doc-path-heading">${idx + 1}. ${p.title}</div>
        <div class="doc-path-fit">${p.fit_reason || ''}</div>
        <div class="doc-meta-label">TARGET ROLES</div>
        <div class="doc-meta-val">${r}</div>
        <div class="doc-meta-label">KEY SKILL GAPS</div>
        <div class="doc-meta-val">${g}</div>
      `;
      docPaths.appendChild(entry);
    });
  }

  const docSkills = document.getElementById('doc-skills-list');
  if (docSkills) {
    docSkills.innerHTML = (report.skills_to_learn || [])
      .map((s) => `<li>${s}</li>`)
      .join('');
  }

  const docDeg = document.getElementById('doc-degrees-text');
  const docCol = document.getElementById('doc-colleges-text');
  if (docDeg) docDeg.textContent = Array.isArray(report.recommended_degrees) ? report.recommended_degrees.join(', ') : report.recommended_degrees || 'N/A';
  if (docCol) docCol.textContent = Array.isArray(report.recommended_colleges) ? report.recommended_colleges.join(', ') : report.recommended_colleges || 'N/A';

  const docShort = document.getElementById('doc-short-text');
  const docLong = document.getElementById('doc-long-text');
  const docVerdict = document.getElementById('doc-verdict-text');
  if (docShort) docShort.textContent = report.short_term_plan || '';
  if (docLong) docLong.textContent = report.long_term_plan || '';
  if (docVerdict) docVerdict.textContent = report.overall_summary || '';
}