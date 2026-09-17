document.addEventListener("DOMContentLoaded", () => {
  document.documentElement.classList.add("js-ready");

  const revealItems = document.querySelectorAll(".reveal");
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.16 }
  );

  revealItems.forEach((item, index) => {
    item.style.setProperty("--reveal-delay", `${Math.min(index * 70, 350)}ms`);
    revealObserver.observe(item);
  });

  const ticker = document.querySelector(".ticker");
  if (ticker) {
    const content = ticker.innerHTML;
    ticker.innerHTML = `<div class="ticker-track">${content}${content}</div>`;
    ticker.classList.add("is-animated");
  }

  const portrait = document.querySelector(".portrait");
  if (
    portrait &&
    window.matchMedia("(prefers-reduced-motion: no-preference)").matches
  ) {
    window.addEventListener(
      "scroll",
      () => {
        const distance = portrait.getBoundingClientRect().top * -0.035;
        portrait.style.setProperty(
          "--parallax-y",
          `${Math.max(-18, Math.min(18, distance))}px`
        );
      },
      { passive: true }
    );
  }

  document.querySelectorAll(".tile, .socials a, .back").forEach(element => {
    element.addEventListener("pointermove", event => {
      if (window.matchMedia("(hover: none)").matches) return;
      const box = element.getBoundingClientRect();
      const x = ((event.clientX - box.left) / box.width - 0.5) * 4;
      const y = ((event.clientY - box.top) / box.height - 0.5) * 4;
      element.style.setProperty("--tilt-x", `${-y}deg`);
      element.style.setProperty("--tilt-y", `${x}deg`);
    });

    element.addEventListener("pointerleave", () => {
      element.style.setProperty("--tilt-x", "0deg");
      element.style.setProperty("--tilt-y", "0deg");
    });
  });
});
