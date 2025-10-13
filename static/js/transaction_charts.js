document.addEventListener('DOMContentLoaded', () => {
  const moneyCanvas = document.getElementById('moneyPie');
  if (moneyCanvas) {
    const labelStr = moneyCanvas.dataset.labels || "[]";
    const valueStr = moneyCanvas.dataset.values || "[]";

    let labels, values;
    try {
      labels = JSON.parse(labelStr);
      values = JSON.parse(valueStr);
    } catch (e) {
      console.error("Failed to parse chart data:", e);
      labels = [];
      values = [];
    }

    if (labels.length && values.length) {
      new Chart(moneyCanvas, {
        type: 'pie',
        data: { labels, datasets: [{ data: values }] },
        options: {
          responsive: true,
          plugins: {
            title: { display: true, text: 'Income vs Expenses' },
            legend: { position: 'bottom' },
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const v = ctx.parsed ?? 0;
                  const total = ctx.dataset.data.reduce((a,b)=>a+b,0) || 1;
                  const pct = (v / total * 100).toFixed(1);
                  return `${ctx.label}: £${v.toLocaleString()} (${pct}%)`;
                }
              }
            }
          }
        }
      });
    }
  }
});