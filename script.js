document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('js-ready');

  // Entrata degli elementi quando compaiono durante lo scroll.
  const revealItems = document.querySelectorAll('.section, .sub, .list, .footer, .card, .life > div, .item');
  revealItems.forEach((element, index) => {
    element.classList.add('js-reveal');
    element.style.setProperty('--reveal-delay', `${Math.min(index * 45, 280)}ms`);
  });

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealItems.forEach((element) => revealObserver.observe(element));

  // Ticker infinito, più fluido rispetto alla semplice animazione CSS.
  const ticker = document.querySelector('.ticker');
  if (ticker) {
    const original = ticker.innerHTML;
    ticker.innerHTML = `<div class="ticker-content">${original}${original}</div>`;
    const tickerContent = ticker.querySelector('.ticker-content');
    let position = 0;
    let lastTime = performance.now();
    const animateTicker = (time) => {
      const delta = Math.min(time - lastTime, 40);
      lastTime = time;
      position -= delta * 0.035;
      const halfWidth = tickerContent.scrollWidth / 2;
      if (Math.abs(position) >= halfWidth) position += halfWidth;
      tickerContent.style.transform = `translate3d(${position}px, 0, 0)`;
      requestAnimationFrame(animateTicker);
    };
    requestAnimationFrame(animateTicker);
  }

  // Parallax leggero sull'immagine principale.
  const photo = document.querySelector('.photo');
  if (photo && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    window.addEventListener('scroll', () => {
      const rect = photo.getBoundingClientRect();
      const offset = (window.innerHeight / 2 - (rect.top + rect.height / 2)) * 0.035;
      photo.style.setProperty('--parallax-y', `${offset}px`);
    }, { passive: true });
  }

  // Tilt leggero sulle card, disattivato su touch e per chi riduce il movimento.
  const canTilt = window.matchMedia('(hover: hover) and (pointer: fine)').matches && window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
  if (canTilt) {
    document.querySelectorAll('.card').forEach((card) => {
      card.addEventListener('pointermove', (event) => {
        const rect = card.getBoundingClientRect();
        const rotateX = ((event.clientY - rect.top) / rect.height - 0.5) * -4;
        const rotateY = ((event.clientX - rect.left) / rect.width - 0.5) * 5;
        card.style.setProperty('--tilt-x', `${rotateX}deg`);
        card.style.setProperty('--tilt-y', `${rotateY}deg`);
        card.classList.add('is-tilting');
      });
      card.addEventListener('pointerleave', () => {
        card.classList.remove('is-tilting');
        card.style.setProperty('--tilt-x', '0deg');
        card.style.setProperty('--tilt-y', '0deg');
      });
    });
  }

  // Piccolo effetto ripple sui pulsanti/back link.
  document.querySelectorAll('.back').forEach((button) => {
    button.addEventListener('click', (event) => {
      const ripple = document.createElement('span');
      ripple.className = 'js-ripple';
      const rect = button.getBoundingClientRect();
      ripple.style.left = `${event.clientX - rect.left}px`;
      ripple.style.top = `${event.clientY - rect.top}px`;
      button.appendChild(ripple);
      setTimeout(() => ripple.remove(), 550);
    });
  });
});
