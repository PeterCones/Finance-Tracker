(() => {
  const PREFIX = 'ft_audio_progress:';   // time key
  const STATE_SUFFIX = ':state';         // play/pause key
  const qs = (s) => document.querySelector(s);

  const sectionFromPath = (p) => '/' + ((p || '/').split('/').filter(Boolean)[0] || '');
  const pageKey = () => {
    const path = window.location.pathname || '/';
    const html = document.documentElement;
    const body = document.body;
    const explicit = body?.getAttribute('data-audio-key');
    const scope = (body?.getAttribute('data-audio-scope') || '').toLowerCase();
    const base = explicit || (scope === 'page' ? path : sectionFromPath(path));
    const uid = html?.getAttribute('data-user-id') || '';
    return `${PREFIX}${uid ? uid + ':' : ''}${base}`;
  };
  const stateKey = () => pageKey() + STATE_SUFFIX;

  function getDefaultSrc() {
    const p = window.location.pathname || '/';
    const base = (window.STATIC_URL || '/static/') + 'music/';

    if (p.startsWith('/transactions')) return base + 'transactions.mp3';
    if (p.startsWith('/budgets'))      return base + 'budgets.mp3';
    if (p.startsWith('/goals'))        return base + 'goals.mp3';
    if (p.startsWith('/accounts/signup') || p.startsWith('/accounts/login'))
                                      return base + 'signup.mp3';
    return base + 'dashboard.mp3';
  }

  const loadNum = (k, d = 0) => {
    try { const v = localStorage.getItem(k); const n = v == null ? NaN : parseFloat(v); return Number.isFinite(n) ? n : d; }
    catch { return d; }
  };
  const saveNum = (k, n) => { try { localStorage.setItem(k, String(n ?? 0)); } catch {} };
  const loadState = () => { try { return localStorage.getItem(stateKey()) === 'playing' ? 'playing' : 'paused'; } catch { return 'paused'; } };
  const saveState = (s) => { try { localStorage.setItem(stateKey(), s === 'playing' ? 'playing' : 'paused'); } catch {} };

  function setup() {
    const audio = qs('#site-audio');
    if (!audio) return;
    audio.controls = true; audio.preload = 'auto';

    const src = document.body?.getAttribute('data-audio-src') || getDefaultSrc();
    if (!audio.src || !audio.src.endsWith(src)) audio.src = src;

    audio.addEventListener('loadedmetadata', () => {
      const t = loadNum(pageKey(), 0);
      if (Number.isFinite(audio.duration) && audio.duration > 0 && t > 0) {
        audio.currentTime = Math.min(t, Math.max(audio.duration - 2, 0));
      }
      if (loadState() === 'playing') {
        audio.play().catch(() => {}); // user gesture may be required
      }
    }, { once: true });

    let lastSaved = -1;
    const saveTime = () => {
      const t = audio.currentTime || 0;
      if (Math.abs(t - lastSaved) >= 1) { saveNum(pageKey(), t); lastSaved = t; }
    };
    audio.addEventListener('timeupdate', saveTime);
    audio.addEventListener('seeking', saveTime);
    audio.addEventListener('seeked', saveTime);
    audio.addEventListener('pause', () => { saveTime(); saveState('paused'); });
    audio.addEventListener('play',  () => { saveState('playing'); });

    const startOnce = () => { if (audio.paused) audio.play().catch(() => {}); window.removeEventListener('click', startOnce); window.removeEventListener('keydown', startOnce); window.removeEventListener('touchstart', startOnce); };
    window.addEventListener('click', startOnce, { passive: true });
    window.addEventListener('keydown', startOnce);
    window.addEventListener('touchstart', startOnce, { passive: true });
    window.addEventListener('beforeunload', saveTime);
    document.addEventListener('visibilitychange', () => { if (document.hidden) saveTime(); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
