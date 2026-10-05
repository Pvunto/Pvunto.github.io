document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.classList.add('js-ready');

  const reveals = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    reveals.forEach((item) => item.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.14 });
    reveals.forEach((item, index) => {
      item.style.transitionDelay = `${Math.min(index * 65, 320)}ms`;
      revealObserver.observe(item);
    });
  }

  const navLinks = document.querySelectorAll('nav a[href^="#"]');
  const sections = document.querySelectorAll('main section[id]');
  if ('IntersectionObserver' in window && navLinks.length) {
    const linkObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`));
      });
    }, { rootMargin: '-35% 0px -55% 0px' });
    sections.forEach((section) => linkObserver.observe(section));
  }

  const menuToggle = document.querySelector('.menu-toggle');
  const primaryNav = document.querySelector('#primary-nav');
  if (menuToggle && primaryNav) {
    const closeMenu = () => {
      primaryNav.classList.remove('is-open');
      menuToggle.setAttribute('aria-expanded', 'false');
    };
    menuToggle.addEventListener('click', () => {
      const open = primaryNav.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', String(open));
    });
    primaryNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    window.addEventListener('resize', () => { if (window.innerWidth > 760) closeMenu(); });
  }

  const filterButtons = document.querySelectorAll('.filter-button');
  const favoriteGames = document.querySelectorAll('.favorite-game[data-game-type]');
  if (filterButtons.length && favoriteGames.length) {
    filterButtons.forEach((button) => button.addEventListener('click', () => {
      const filter = button.dataset.filter;
      filterButtons.forEach((item) => item.classList.toggle('is-active', item === button));
      favoriteGames.forEach((game) => {
        game.hidden = filter !== 'all' && game.dataset.gameType !== filter;
      });
    }));
  }

  if (window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.tilt-card').forEach((card) => {
      card.addEventListener('pointermove', (event) => {
        const box = card.getBoundingClientRect();
        const x = ((event.clientX - box.left) / box.width - 0.5) * 3;
        const y = ((event.clientY - box.top) / box.height - 0.5) * 3;
        card.style.transform = `translateY(-6px) rotateX(${-y}deg) rotateY(${x}deg)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }
});
