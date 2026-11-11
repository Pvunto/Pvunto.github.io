(() => {
  'use strict';

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
    window.addEventListener('resize', () => {
      if (window.matchMedia('(min-width: 761px)').matches) closeMenu();
    }, { passive: true });
  }

  const filters = [...document.querySelectorAll('.filter-button[data-filter]')];
  const cards = [...document.querySelectorAll('.game-card[data-tags]')];
  const status = document.getElementById('game-filter-status');
  const filterLabels = { all: 'elenco completo', archivio: 'altri preferiti non attuali', attuale: 'titoli attuali' };

  if (filters.length && cards.length) {
    const countFor = (filter) => cards.filter((card) => filter === 'all' || card.dataset.tags.split(/\s+/).includes(filter)).length;
    filters.forEach((button) => {
      const count = button.querySelector('[data-count]');
      if (count) count.textContent = String(countFor(button.dataset.filter));
      button.addEventListener('click', () => {
        const filter = button.dataset.filter;
        let shown = 0;
        filters.forEach((item) => {
          const active = item === button;
          item.classList.toggle('is-active', active);
          item.setAttribute('aria-pressed', String(active));
        });
        cards.forEach((card) => {
          const visible = filter === 'all' || card.dataset.tags.split(/\s+/).includes(filter);
          card.classList.toggle('is-hidden', !visible);
          if (visible) shown += 1;
        });
        if (status) {
          const noun = shown === 1 ? 'videogioco' : 'videogiochi';
          const participle = shown === 1 ? 'visualizzato' : 'visualizzati';
          status.textContent = `${shown} ${noun} ${participle} (${filterLabels[filter] || 'selezione'}).`;
        }
      });
    });
  }

  document.querySelectorAll('.video-load').forEach((button) => {
    button.addEventListener('click', () => {
      const frame = button.closest('.video-frame');
      if (!frame || frame.querySelector('iframe')) return;
      const videoId = frame.dataset.videoId;
      if (!/^[A-Za-z0-9_-]{11}$/.test(videoId || '')) return;
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0`;
      iframe.title = frame.dataset.videoTitle || 'Video YouTube';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      iframe.loading = 'eager';
      iframe.allowFullscreen = true;
      frame.replaceChildren(iframe);
    });
  });

  const form = document.getElementById('feedback-form');
  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const topic = document.getElementById('feedback-topic');
      const message = document.getElementById('feedback-message');
      const statusMessage = document.getElementById('feedback-status');
      const issue = new URL('https://github.com/Pvunto/Pvunto.github.io/issues/new');
      issue.searchParams.set('title', `Feedback dal sito Punto: ${topic.value}`);
      issue.searchParams.set('body', `${message.value}\n\n---\nMessaggio preparato dal modulo del sito personale Punto. Non è stato inviato automaticamente.`);
      window.open(issue.toString(), '_blank', 'noopener,noreferrer');
      if (statusMessage) statusMessage.textContent = 'Bozza GitHub aperta in una nuova scheda. Rivedi il contenuto e invialo solo se desideri renderlo pubblico.';
    });
  }
})();
