(function () {
  const form = document.getElementById('askForm');
  const input = document.getElementById('askInput');

  function normalize(text) {
    return (text || '')
      .toLowerCase()
      .replace(/[“”]/g, '"')
      .replace(/[’]/g, "'")
      .replace(/[^\p{L}\p{N}#+.\-\s]/gu, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function uniqueTokens(text) {
    return Array.from(new Set(normalize(text).split(' ').filter((token) => token.length > 1)));
  }

  function getSectionTarget(element) {
    if (!element) return null;
    if (element.id) return '#' + element.id;
    const section = element.closest('section[id], article[id]');
    if (section) return '#' + section.id;
    const heading = element.querySelector('h1[id], h2[id], h3[id]');
    if (heading) return '#' + heading.id;
    return null;
  }

  function addCandidate(candidates, seen, target, title, body, weight) {
    if (!target || !title) return;
    const key = target + '|' + title;
    if (seen.has(key)) return;
    seen.add(key);
    candidates.push({
      target,
      title: title.trim(),
      body: (body || '').trim(),
      weight: weight || 1
    });
  }

  function buildSearchCandidates() {
    const candidates = [];
    const seen = new Set();

    document.querySelectorAll('.reference-card, .mini-card, .category-card').forEach((card) => {
      const link = card.querySelector('h3 a[href], a[href]');
      const heading = card.querySelector('h3, h2');
      const target = link ? link.getAttribute('href') : getSectionTarget(card);
      addCandidate(candidates, seen, target, heading ? heading.textContent : card.textContent, card.textContent, 5);
    });

    document.querySelectorAll('.question-grid a[href], .contents a[href], .sidebar a[href], .top-links a[href]').forEach((link) => {
      addCandidate(candidates, seen, link.getAttribute('href'), link.textContent, link.textContent, 3);
    });

    document.querySelectorAll('article h1[id], article h2[id], article h3[id]').forEach((heading) => {
      const section = heading.closest('section[id]');
      const body = section ? section.textContent : heading.textContent;
      addCandidate(candidates, seen, '#' + heading.id, heading.textContent, body, heading.tagName === 'H1' ? 5 : 4);
    });

    document.querySelectorAll('article section[id]').forEach((section) => {
      const heading = section.querySelector('h2, h3') || section;
      addCandidate(candidates, seen, '#' + section.id, heading.textContent, section.textContent, 4);
    });

    return candidates;
  }

  function scoreCandidate(candidate, query) {
    const normalizedQuery = normalize(query);
    if (!normalizedQuery) return 0;

    const title = normalize(candidate.title);
    const body = normalize(candidate.body);
    const tokens = uniqueTokens(query);
    let score = 0;

    if (title === normalizedQuery) score += 120;
    if (title.includes(normalizedQuery)) score += 70;
    if (body.includes(normalizedQuery)) score += 35;

    tokens.forEach((token) => {
      if (title.includes(token)) score += 18;
      if (body.includes(token)) score += 6;
      if (candidate.target && normalize(candidate.target).includes(token)) score += 8;
    });

    if (tokens.length && tokens.every((token) => title.includes(token))) score += 35;
    if (tokens.length && tokens.every((token) => body.includes(token))) score += 12;

    return score * candidate.weight;
  }

  function bestCandidate(query) {
    const candidates = buildSearchCandidates();
    if (!normalize(query)) {
      return candidates.find((candidate) => candidate.target && candidate.target.startsWith('#')) || candidates[0];
    }

    return candidates
      .map((candidate) => ({ ...candidate, score: scoreCandidate(candidate, query) }))
      .filter((candidate) => candidate.score > 0)
      .sort((a, b) => b.score - a.score)[0];
  }

  function showSearchNotice(message) {
    let notice = document.getElementById('searchNotice');
    if (!notice && form) {
      notice = document.createElement('span');
      notice.id = 'searchNotice';
      notice.setAttribute('role', 'status');
      notice.style.marginLeft = '8px';
      notice.style.fontSize = '12px';
      notice.style.color = '#54595d';
      form.appendChild(notice);
    }
    if (!notice) return;
    notice.textContent = message;
    window.clearTimeout(showSearchNotice.timer);
    showSearchNotice.timer = window.setTimeout(() => {
      notice.textContent = '';
    }, 2200);
  }

  function goTo(target) {
    if (!target) return false;

    if (!target.startsWith('#')) {
      window.location.href = target;
      return true;
    }

    const element = document.querySelector(target);
    if (!element) return false;
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', target);
    return true;
  }

  if (form && input) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const match = bestCandidate(input.value);
      if (match && goTo(match.target)) {
        showSearchNotice(match.target.startsWith('#') ? 'Moved to: ' + match.title : 'Opening: ' + match.title);
      } else {
        showSearchNotice('No matching section found.');
      }
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
