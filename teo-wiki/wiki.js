(function () {
  const form = document.getElementById('askForm');
  const input = document.getElementById('askInput');

  const routes = [
    { keywords: ['summary', 'overview', 'who', 'intro', 'profile'], target: '#overview' },
    { keywords: ['research map', 'map', 'graph', 'direction', 'directions'], target: 'research-map/' },
    { keywords: ['wiki', 'llm wiki', 'research brain', 'brain', 'karpathy', 'knowledge base'], target: '#research-brain' },
    { keywords: ['research', 'field', 'identity', 'vision', 'multimodal', 'audio', 'visual', '3d', 'scene'], target: '#research' },
    { keywords: ['project', 'projects', 'known', 'known for', 'anybald', 'gomoku', 'lang', 'cheese', 'vad'], target: '#projects' },
    { keywords: ['publication', 'paper', 'papers', 'wacv', 'technical report'], target: '#publications' },
    { keywords: ['experience', 'toronto', 'unist', 'upsight', 'education', 'work', 'study'], target: '#experience' },
    { keywords: ['value', 'values', 'principle', 'approach', 'style', 'operate'], target: '#values' },
    { keywords: ['question', 'questions', 'future', 'explore', 'open'], target: '#open-questions' },
    { keywords: ['public', 'private', 'boundary', 'safe', 'privacy'], target: '#public-boundary' }
  ];

  function normalize(text) {
    return (text || '').toLowerCase().trim();
  }

  function findTarget(query) {
    const normalized = normalize(query);
    if (!normalized) return window.location.pathname.includes('/research-map/') ? '#map-overview' : '#ask-about-teo';

    if (window.location.pathname.includes('/research-map/')) {
      const mapRoutes = [
        { keywords: ['visual', 'editing', 'diffusion', 'anybald', 'hair'], target: '#visual-editing' },
        { keywords: ['scene', '3d', 'language', 'gaussian', 'clip'], target: '#scene-understanding' },
        { keywords: ['video', 'vad', 'anomaly', 'inspection', 'alignment'], target: '#video-understanding' },
        { keywords: ['audio', 'multimodal', 'temporal'], target: '#audio-visual-learning' },
        { keywords: ['practical', 'robot', 'hri', 'cheese', 'application'], target: '#practical-ai' },
        { keywords: ['wiki', 'llm', 'karpathy', 'brain', 'knowledge'], target: '#llm-wiki-loop' }
      ];
      for (const route of mapRoutes) {
        if (route.keywords.some((keyword) => normalized.includes(keyword))) return route.target;
      }
    }

    for (const route of routes) {
      if (route.keywords.some((keyword) => normalized.includes(keyword))) {
        return route.target === 'research-map/' && window.location.pathname.includes('/research-map/')
          ? '#map-overview'
          : route.target;
      }
    }
    return '#ask-about-teo';
  }

  function goTo(target) {
    if (!target.startsWith('#')) {
      window.location.href = target;
      return;
    }
    const element = document.querySelector(target);
    if (!element) return;
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', target);
  }

  if (form && input) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      goTo(findTarget(input.value));
    });
  }

  const sections = Array.from(document.querySelectorAll('article section[id], article h1[id]'));
  const sideLinks = Array.from(document.querySelectorAll('.sidebar a'));

  if ('IntersectionObserver' in window && sections.length && sideLinks.length) {
    const observer = new IntersectionObserver(
      function (entries) {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (!visible) return;

        const id = visible.target.getAttribute('id');
        sideLinks.forEach((link) => {
          const active = link.getAttribute('href') === '#' + id;
          link.classList.toggle('active', active);
        });
      },
      { rootMargin: '-20% 0px -65% 0px', threshold: [0.1, 0.3, 0.6] }
    );

    sections.forEach((section) => observer.observe(section));
  }
})();
