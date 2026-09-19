// EPR Compliance Copilot - Frontend Logic (IMP-009, IMP-013)

function switchTab(tabId, btn) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  btn.classList.add('active');
  if (tabId === 'kbTab') loadKnowledgeBase();
}

function fillQuery(pill) {
  document.getElementById('questionInput').value = pill.innerText;
  askQuestion();
}

async function askQuestion() {
  const q = document.getElementById('questionInput').value.trim();
  if (!q) return;
  const loading = document.getElementById('qaLoading');
  const output = document.getElementById('qaOutput');

  loading.style.display = 'block';
  output.style.display = 'none';

  try {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: q})
    });
    const data = await res.json();

    if (!res.ok) {
      output.innerHTML = `<span style="color:#f4a261;">Error: ${data.error || 'Request failed'}</span>`;
      output.style.display = 'block';
      return;
    }

    let formatted = data.answer.replace(/\n/g, '<br>');
    let html = formatted;

    if (data.citations && data.citations.length > 0) {
      html += '<br><br><b>Ground-truth Citations:</b><br>';
      data.citations.forEach(c => {
        html += `<span class="citation-tag ${c.confidence}">[${c.id}] ${c.title} (${c.confidence})</span>`;
      });
    }
    html += `<br><br><i style="color:#9aa59d;font-size:12px;">${data.disclaimer}</i>`;
    output.innerHTML = html;
    output.style.display = 'block';
  } catch (err) {
    output.innerHTML = '<span style="color:#f4a261;">Network error querying copilot: ' + err + '</span>';
    output.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
}

async function calculateObligations() {
  const piboType = document.getElementById('piboType').value;
  const fiscalYear = document.getElementById('fiscalYearSelect').value;
  const tonnages = {
    cat_1: parseFloat(document.getElementById('cat1Input').value) || 0,
    cat_2: parseFloat(document.getElementById('cat2Input').value) || 0,
    cat_3: parseFloat(document.getElementById('cat3Input').value) || 0,
    cat_4: parseFloat(document.getElementById('cat4Input').value) || 0,
  };

  try {
    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({pibo_type: piboType, fiscal_year: fiscalYear, tonnages})
    });
    const data = await res.json();

    document.getElementById('resTotalIntroduced').innerText = data.total_introduced_packaging_mt + ' MT';
    document.getElementById('resRecyclingTarget').innerText = data.total_recycling_obligation_mt + ' MT';
    document.getElementById('resRecycledContent').innerText = data.total_recycled_content_required_mt + ' MT';
    document.getElementById('resPenaltyExposure').innerText = 'Rs ' + data.potential_ec_penalty_exposure_inr.toLocaleString('en-IN');
    document.getElementById('resCertRange').innerText = data.estimated_cert_procurement_cost_range_inr.formatted;

    document.getElementById('refYr1').innerText = data.ec_refund_schedule.year_1_fulfillment;
    document.getElementById('refYr2').innerText = data.ec_refund_schedule.year_2_fulfillment;
    document.getElementById('refYr3').innerText = data.ec_refund_schedule.year_3_fulfillment;

    const tbody = document.querySelector('#categoryTable tbody');
    tbody.innerHTML = '';
    for (const [key, c] of Object.entries(data.categories)) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><b>${c.name.split(':')[0]}</b><br><span style="font-size:11px;color:#9aa59d">${c.name.split(':')[1]}</span></td>
        <td>${c.introduced_mt}</td>
        <td>${c.recycling_target_pct}%</td>
        <td><b>${c.recycling_obligation_mt}</b></td>
        <td>${c.recycled_content_mandate_pct}% (${c.recycled_content_required_mt} MT)</td>
        <td>Rs ${c.estimated_cert_cost_range_inr[0].toLocaleString('en-IN')} - ${c.estimated_cert_cost_range_inr[1].toLocaleString('en-IN')}</td>
      `;
      tbody.appendChild(row);
    }

    document.getElementById('calcResultsSection').style.display = 'block';
  } catch (e) {
    alert('Error computing liability: ' + e);
  }
}

function printReport() {
  window.print();
}

async function loadKnowledgeBase() {
  const container = document.getElementById('kbListContainer');
  try {
    const res = await fetch('/api/kb');
    const chunks = await res.json();
    let html = '';
    chunks.forEach(c => {
      html += `
        <div style="background:#0f1511; border:1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <b style="font-size:13.5px; color:#e1e7e2;">[${c.id}] ${c.title}</b>
            <span class="citation-tag ${c.confidence}">${c.confidence}</span>
          </div>
          <div style="font-size:12px; color:var(--text-muted); margin-bottom:6px;"><b>Citation:</b> ${c.citation}</div>
          <div style="font-size:12.5px; color:#c5cdc7; line-height:1.4;">${c.text_preview}</div>
        </div>
      `;
    });
    container.innerHTML = html;
  } catch (e) {
    container.innerHTML = 'Error loading knowledge base: ' + e;
  }
}
