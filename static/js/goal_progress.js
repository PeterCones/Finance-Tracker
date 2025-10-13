document.addEventListener('DOMContentLoaded', () => {
  if (typeof Chart === 'undefined') return;

  const els = document.querySelectorAll('canvas.goal-line');

  const toDate = (iso) => {
    if (!iso) return null;
    const d = new Date(`${iso}T00:00:00`);
    return isNaN(d.getTime()) ? null : d;
  };

  const buildDayLabels = (start, end) => {
    const days = [];
    const d = new Date(start.getTime());
    d.setHours(0,0,0,0);
    const last = new Date(end.getTime());
    last.setHours(0,0,0,0);

    while (d <= last) {
      days.push(new Date(d.getTime())); // push a copy
      d.setDate(d.getDate() + 1);
    }
    return days;
  };

  els.forEach(cnv => {
    const startISO = cnv.dataset.startDate || cnv.dataset.createdAt;
    const endISO = cnv.dataset.endDate || cnv.dataset.targetDate;

    const start = toDate(startISO) || new Date(); // fallback to today
    const end = toDate(endISO);
    if (!end) return; // cannot draw without an end date

    const startRemaining = Number.parseFloat(cnv.dataset.startRemaining || '0');
    const currentRemaining = Number.parseFloat(cnv.dataset.currentRemaining || '0');

    // Daily labels from start to target_date (inclusive)
    const labels = buildDayLabels(start, end);

    // Planned: remaining goes from startRemaining -> 0 by target date
    const planned = [
      { x: start, y: Number.isFinite(startRemaining) ? startRemaining : 0 },
      { x: end,   y: 0 }
    ];

    const today = new Date();
    today.setHours(0,0,0,0);

    const actualPoint = {
      x: today > end ? end : today,
      y: Math.max(Number.isFinite(currentRemaining) ? currentRemaining : 0, 0)
    };

    // Avoid duplicate init during hot reloads
    if (cnv._goalChart) cnv._goalChart.destroy();

    cnv._goalChart = new Chart(cnv, {
      type: 'line',
      data: {
        labels,                // force day-by-day ticks; last tick is target_date
        datasets: [
          {
            label: 'Planned remaining',
            data: planned,
            parsing: false,
            borderColor: '#9e9e9e',
            backgroundColor: 'rgba(158,158,158,0.15)',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0
          },
          {
            label: 'Today',
            data: [actualPoint],
            parsing: false,
            showLine: false,
            borderColor: '#2196f3',
            backgroundColor: '#2196f3',
            pointRadius: 5,
            pointHoverRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,   // use a fixed-height wrapper in CSS
        animation: { duration: 300 },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `Remaining: £${(ctx.parsed.y ?? 0).toFixed(2)}`
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              round: 'day',
              tooltipFormat: 'PP',
              displayFormats: { day: 'MMM d' }
            },
            ticks: {
              source: 'labels',   // use our per-day labels
              autoSkip: true,     // avoid overcrowding (still daily increments)
              maxTicksLimit: 10,  // adjust for density
              maxRotation: 0
            },
            min: labels[0],
            max: labels[labels.length - 1]
          },
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Remaining (£)' }
          }
        }
      }
    });
  });
});