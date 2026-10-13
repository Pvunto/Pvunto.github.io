(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');

  if (menuButton && nav) {
    const closeMenu = () => {
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Apri il menu');
      nav.classList.remove('is-open');
    };

    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Apri il menu' : 'Chiudi il menu');
      nav.classList.toggle('is-open', !isOpen);
    });

    nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeMenu();
    });
  }

  const filters = [...document.querySelectorAll('.filter-button')];
  const cards = [...document.querySelectorAll('.game-card')];
  const status = document.getElementById('game-filter-status');
  const filterLabels = { all: 'tutti', preferito: 'i preferiti', attuale: 'il titolo in rotazione' };

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;
      let shown = 0;

      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });

      cards.forEach((card) => {
        const visible = filter === 'all' || card.dataset.tags.split(' ').includes(filter);
        card.classList.toggle('is-hidden', !visible);
        if (visible) shown += 1;
      });

      if (status) {
        const noun = shown === 1 ? 'videogioco' : 'videogiochi';
        status.textContent = `Mostrati ${filterLabels[filter]}: ${shown} ${noun}.`;
      }
    });
  });

  const year = document.getElementById('current-year');
  if (year) year.textContent = String(new Date().getFullYear());

  const feedbackForm = document.getElementById('feedback-form');
  if (feedbackForm) {
    const topic = document.getElementById('feedback-topic');
    const title = document.getElementById('feedback-title');
    const statusMessage = document.getElementById('feedback-status');
    const terminal = feedbackForm.closest('.feedback-terminal');
    const updateIssueTitle = () => {
      if (topic && title) title.value = `Feedback dal sito Punto: ${topic.value}`;
    };

    if (topic) topic.addEventListener('change', updateIssueTitle);
    feedbackForm.addEventListener('submit', () => {
      updateIssueTitle();
      if (terminal) terminal.classList.add('is-ready');
      if (statusMessage) statusMessage.textContent = 'La bozza si apre in una nuova scheda: rileggila e inviala su GitHub solo se vuoi.';
    });
  }

  const sections = [...document.querySelectorAll('main section[id]')];
  const navLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];
  if ('IntersectionObserver' in window && sections.length && navLinks.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => {
          if (link.getAttribute('href') === `#${entry.target.id}`) {
            link.setAttribute('aria-current', 'location');
          } else {
            link.removeAttribute('aria-current');
          }
        });
      });
    }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
    sections.forEach((section) => observer.observe(section));
  }
})();
