document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.classList.add('js-ready');
  const items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach((item) => item.classList.add('is-visible'));
    return;
  }
  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      currentObserver.unobserve(entry.target);
    });
  }, { threshold: 0.14 });
  items.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index * 70, 350)}ms`;
    observer.observe(item);
  });

  const navLinks = document.querySelectorAll('nav a[href^="#"]');
  const sections = document.querySelectorAll('main section[id]');
  const linkObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`));
    });
  }, { rootMargin: '-35% 0px -55% 0px' });
  sections.forEach((section) => linkObserver.observe(section));
});
