async function loadDashboard() {
  const response = await fetch('dashboard-data.json');
  const data = await response.json();

  document.getElementById('repo').textContent = `Repository: ${data.repo}`;
  document.getElementById('scan-date').textContent = `Latest scan date: ${data.summary.latest_scan_date}`;

  const summaryCards = document.getElementById('summary-cards');
  const summary = data.summary;

  const cards = [
    ['Total Findings', summary.total_findings],
    ['Secrets Findings', summary.secrets_findings_count],
    ['Vulnerable Dependencies', summary.vulnerable_dependencies_count],
    ['SBOM Generated', summary.sbom_generated ? 'Yes' : 'No'],
    ['By Tool', JSON.stringify(summary.findings_by_tool)],
    ['By Severity', JSON.stringify(summary.findings_by_severity)],
  ];

  cards.forEach(([title, value]) => {
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML = `<h3>${title}</h3><p>${value}</p>`;
    summaryCards.appendChild(card);
  });

  const tbody = document.getElementById('findings-body');
  for (const item of data.findings) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.tool}</td>
      <td>${item.category}</td>
      <td>${item.severity}</td>
      <td>${item.title}</td>
      <td>${item.file}</td>
      <td>${item.line}</td>
      <td>${item.rule_id}</td>
    `;
    tbody.appendChild(row);
  }
}

loadDashboard().catch((error) => {
  console.error('Failed to load dashboard data', error);
});
