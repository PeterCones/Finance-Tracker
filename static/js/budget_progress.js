document.addEventListener('DOMContentLoaded', () => {
  const allProgressBars = document.querySelectorAll('.progress-bar-container');

  allProgressBars.forEach(container => {
    const raw = parseFloat(container.dataset.progress);
    const requestedPercentage = isNaN(raw) ? 0 : raw;

    // Clamp to [0, 100] for both animation and display
    const clampedPercentage = Math.min(Math.max(requestedPercentage, 0), 100);
    const animationValue = clampedPercentage / 100;

    // Use amber while animating, switch to green at 100%
    const AMBER = '#ff9800';
    const GREEN = '#4caf50';

    const bar = new ProgressBar.Line(container, {
      strokeWidth: 4,
      easing: 'easeInOut',
      duration: 1400,
      color: AMBER,                  // will switch to GREEN at 100%
      trailColor: '#eee',
      trailWidth: 4,
      svgStyle: { width: '100%', height: '100%', 'border-radius': '15px' },
      text: {
        style: {
          color: '#333',
          position: 'absolute',
          right: '10px',
          top: '5px',
          padding: 0,
          margin: 0,
          transform: null,
          fontFamily: 'sans-serif',
        },
        autoStyleContainer: false
      },
      step: (state, bar) => {
        // Compute current animated percentage (0..100), clamped
        const currentPct = Math.min(Math.round(bar.value() * 100), 100);

        // Display clamped text only up to 100%
        bar.setText(currentPct + ' %');

        // Turn green exactly at 100%, else amber
        if (currentPct >= 100) {
          bar.path.setAttribute('stroke', GREEN);
          bar.text.style.color = GREEN;
        } else {
          bar.path.setAttribute('stroke', AMBER);
          bar.text.style.color = '#333';
        }
      }
    });

    // Animate to the clamped value (never beyond 100%)
    bar.animate(animationValue);
  });
});