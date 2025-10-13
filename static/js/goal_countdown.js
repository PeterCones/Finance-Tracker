document.addEventListener('DOMContentLoaded', () => {
  if (typeof ProgressBar === 'undefined') return;

  const MS_PER_DAY = 24 * 60 * 60 * 1000;
  const parseYMD = (ymd) => new Date(`${ymd}T00:00:00`);

  const containers = document.querySelectorAll('.progress-bar-container');

  containers.forEach(container => {
    const startStr = container.dataset.createdAt || container.dataset.startDate;
    const endStr   = container.dataset.targetDate  || container.dataset.endDate;
    if (!endStr) return;

    const target    = Number.parseFloat(container.dataset.target);
    const remaining = Number.parseFloat(container.dataset.remaining);

    const now   = new Date();
    const start = startStr ? parseYMD(startStr) : new Date(now.getTime());
    const end   = parseYMD(endStr);

    if (isNaN(start.getTime()) || isNaN(end.getTime())) return;

    // Normalize to midnight for day-calcs
    const today   = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const endDay  = new Date(end.getFullYear(), end.getMonth(), end.getDate());

    // Time-based progress (continuous)
    const totalMs   = Math.max(end.getTime() - start.getTime(), 1);
    const elapsedMs = Math.min(Math.max(now.getTime() - start.getTime(), 0), totalMs);
    const timePct   = (elapsedMs / totalMs) * 100;

    // Completion / overdue
    const hasAmounts = Number.isFinite(target) && Number.isFinite(remaining);
    const isComplete = hasAmounts && remaining <= 0;
    const isOverdue  = !isComplete && today > endDay; // after target date and not complete

    // Final percentage
    const pct   = isComplete ? 100 : (isOverdue ? 100 : Math.min(Math.max(timePct, 0), 100));
    const value = pct / 100;

    // Days left (0 on target day, 0 if overdue)
    const daysLeft = Math.max(Math.ceil((endDay.getTime() - today.getTime()) / MS_PER_DAY), 0);

    const GREEN  = '#4caf50'; // success
    const YELLOW = '#ffc107'; // warning
    const RED    = '#f44336'; // danger

    // Pick initial color (before animation step runs)
    let initialColor;
    if (isComplete) initialColor = GREEN;
    else if (isOverdue) initialColor = RED;
    else initialColor = pct < 50 ? GREEN : YELLOW;

    const bar = new ProgressBar.Line(container, {
      strokeWidth: 4,
      easing: 'easeInOut',
      duration: 800,
      color: initialColor,
      trailColor: '#eee',
      trailWidth: 4,
      svgStyle: { width: '100%', height: '100%', 'border-radius': '15px' },
      text: {
        style: {
          color: initialColor,
          position: 'absolute',
          fontWeight:'600',
          right: '10px',
          top: '5px',
          margin: 0,
          fontFamily: 'sans-serif'
        },
        autoStyleContainer: false
      },
      step: (_state, b) => {
        const currentPct = Math.min(Math.round(b.value() * 100), 100);
        const pctText = (isComplete || isOverdue) ? 100 : currentPct;
        const daysText = isOverdue ? 'Overdue' : (daysLeft === 0 ? 'Due' : `${daysLeft} day${daysLeft === 1 ? '' : 's'} left`);
        b.setText(`${pctText}% — ${daysText}`);

        // Dynamic color logic:
        if (isComplete) {
          b.path.setAttribute('stroke', GREEN);
          b.text.style.color = GREEN;
        } else if (isOverdue) {
          b.path.setAttribute('stroke', RED);
          b.text.style.color = RED;
        } else if (currentPct < 50) {
          b.path.setAttribute('stroke', GREEN);
          b.text.style.color = GREEN;
        } else {
          b.path.setAttribute('stroke', YELLOW);
          b.text.style.color = YELLOW;
        }
      }
    });

    bar.animate(value);
  });
});