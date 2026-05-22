const paths = {
  priority: "analysis/outputs/priority_queue.csv",
  lanes: "analysis/outputs/intake_triage_summary.csv",
  handoffs: "analysis/outputs/handoff_packages.csv",
  risks: "analysis/outputs/integration_risk_register.csv",
};

function parseCsv(text) {
  const rows = [];
  let current = "";
  let row = [];
  let insideQuotes = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === '"' && next === '"') {
      current += '"';
      index += 1;
    } else if (char === '"') {
      insideQuotes = !insideQuotes;
    } else if (char === "," && !insideQuotes) {
      row.push(current);
      current = "";
    } else if ((char === "\n" || char === "\r") && !insideQuotes) {
      if (char === "\r" && next === "\n") {
        index += 1;
      }
      row.push(current);
      if (row.some((value) => value.trim() !== "")) {
        rows.push(row);
      }
      row = [];
      current = "";
    } else {
      current += char;
    }
  }

  if (current || row.length) {
    row.push(current);
    rows.push(row);
  }

  const [headers, ...records] = rows;
  return records.map((record) =>
    headers.reduce((item, header, index) => {
      item[header] = record[index] || "";
      return item;
    }, {})
  );
}

async function loadCsv(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Unable to load ${path}`);
  }
  return parseCsv(await response.text());
}

function statusClass(lane) {
  return lane.toLowerCase().replace(/\s+/g, "-");
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function renderMetrics(priority, handoffs) {
  const blocked = priority.filter((row) => row.triage_lane === "Blocked").length;
  const ready = priority.filter((row) => Number(row.acceptance_readiness) >= 80 && row.triage_lane !== "Blocked").length;
  setText("metric-requests", priority.length);
  setText("metric-ready", ready);
  setText("metric-blocked", blocked);
  setText("metric-handoffs", handoffs.length);
}

function renderLanes(lanes) {
  const grid = document.getElementById("lane-grid");
  grid.innerHTML = lanes
    .map(
      (lane) => `
        <article class="lane-card ${statusClass(lane.triage_lane)}">
          <div>
            <span>${lane.triage_lane}</span>
            <strong>${lane.request_count}</strong>
          </div>
          <p>${lane.primary_operating_question}</p>
          <small>Average score ${lane.avg_priority_score}</small>
        </article>
      `
    )
    .join("");
}

function renderRisks(risks) {
  document.getElementById("risk-table").innerHTML = risks
    .map(
      (risk) => `
        <tr>
          <td><b>${risk.request_id}</b><span>${risk.request_name}</span></td>
          <td><mark>${risk.dependency_risk}</mark></td>
          <td>${risk.vendor_dependency}</td>
          <td>${risk.mitigation}</td>
        </tr>
      `
    )
    .join("");
}

function renderPriority(priority) {
  document.getElementById("priority-table").innerHTML = priority
    .map(
      (item) => `
        <tr>
          <td>${item.rank}</td>
          <td><b>${item.request_id}</b><span>${item.request_name}</span></td>
          <td><span class="pill ${statusClass(item.triage_lane)}">${item.triage_lane}</span></td>
          <td><mark>${item.priority_score}</mark></td>
          <td>${item.recommended_next_step}</td>
        </tr>
      `
    )
    .join("");
}

function renderHandoffs(handoffs) {
  document.getElementById("handoff-grid").innerHTML = handoffs
    .map(
      (handoff) => `
        <article class="handoff-card">
          <div class="handoff-title">
            <span>${handoff.request_id}</span>
            <h3>${handoff.request_name}</h3>
          </div>
          <p>${handoff.problem_statement}</p>
          <dl>
            <div>
              <dt>Acceptance criteria</dt>
              <dd>${handoff.acceptance_criteria}</dd>
            </div>
            <div>
              <dt>Edge cases</dt>
              <dd>${handoff.edge_cases}</dd>
            </div>
            <div>
              <dt>QA focus</dt>
              <dd>${handoff.qa_focus}</dd>
            </div>
            <div>
              <dt>Launch gate</dt>
              <dd>${handoff.launch_gate}</dd>
            </div>
          </dl>
        </article>
      `
    )
    .join("");
}

function applySurfaceMode() {
  const surface = new URLSearchParams(window.location.search).get("surface");
  if (!surface) {
    return;
  }

  const selected = document.getElementById(surface);
  if (!selected) {
    return;
  }

  document.body.classList.add("screenshot-mode");
  document.querySelectorAll(".surface").forEach((section) => {
    section.hidden = section !== selected;
  });
  window.scrollTo(0, 0);
}

async function init() {
  const [priority, lanes, handoffs, risks] = await Promise.all([
    loadCsv(paths.priority),
    loadCsv(paths.lanes),
    loadCsv(paths.handoffs),
    loadCsv(paths.risks),
  ]);

  renderMetrics(priority, handoffs);
  renderLanes(lanes);
  renderRisks(risks);
  renderPriority(priority);
  renderHandoffs(handoffs);
  applySurfaceMode();
}

init().catch((error) => {
  document.body.insertAdjacentHTML(
    "afterbegin",
    `<p class="load-error">The studio data could not load: ${error.message}</p>`
  );
});
