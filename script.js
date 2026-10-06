document.addEventListener("DOMContentLoaded", () => {
  document.documentElement.classList.add("js-ready");

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll("video[autoplay]").forEach((video) => {
      video.removeAttribute("autoplay");
      video.pause();
    });
  }

  // Reveal sections progressively without blocking content when JS is unavailable.
  const reveals = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    reveals.forEach((item) => item.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.14 },
    );
    reveals.forEach((item, index) => {
      item.style.transitionDelay = `${Math.min(index * 65, 320)}ms`;
      revealObserver.observe(item);
    });
  }

  // Keep the current page highlighted even if a page is opened from a sub-path.
  const primaryNav = document.querySelector("#primary-nav");
  const menuToggle = document.querySelector(".menu-toggle");
  if (primaryNav && menuToggle) {
    const currentPage =
      window.location.pathname.split("/").pop() || "index.html";
    primaryNav.querySelectorAll('a[href$=".html"]').forEach((link) => {
      const target = link.getAttribute("href").split("/").pop();
      link.classList.toggle(
        "active",
        target === currentPage ||
          (currentPage === "" && target === "index.html"),
      );
    });

    const setMenuState = (open) => {
      const isMobile = window.innerWidth <= 820;
      primaryNav.classList.toggle("is-open", open);
      menuToggle.setAttribute("aria-expanded", String(open));
      primaryNav.setAttribute("aria-hidden", String(isMobile && !open));
      primaryNav.inert = isMobile && !open;
    };
    setMenuState(false);
    menuToggle.addEventListener("click", () =>
      setMenuState(!primaryNav.classList.contains("is-open")),
    );
    primaryNav
      .querySelectorAll("a")
      .forEach((link) =>
        link.addEventListener("click", () => setMenuState(false)),
      );
    document.addEventListener("click", (event) => {
      if (!primaryNav.classList.contains("is-open")) return;
      if (
        !primaryNav.contains(event.target) &&
        !menuToggle.contains(event.target)
      )
        setMenuState(false);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setMenuState(false);
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth > 820) setMenuState(false);
    });
  }

  const navLinks = document.querySelectorAll('nav a[href^="#"]');
  const sections = document.querySelectorAll("main section[id]");
  if ("IntersectionObserver" in window && navLinks.length) {
    const linkObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          navLinks.forEach((link) =>
            link.classList.toggle(
              "active",
              link.getAttribute("href") === `#${entry.target.id}`,
            ),
          );
        });
      },
      { rootMargin: "-35% 0px -55% 0px" },
    );
    sections.forEach((section) => linkObserver.observe(section));
  }

  const filterButtons = document.querySelectorAll(".filter-button");
  const favoriteGames = document.querySelectorAll(
    ".favorite-game[data-game-type]",
  );
  if (filterButtons.length && favoriteGames.length) {
    filterButtons.forEach((button) =>
      button.addEventListener("click", () => {
        const filter = button.dataset.filter;
        filterButtons.forEach((item) =>
          item.classList.toggle("is-active", item === button),
        );
        favoriteGames.forEach((game) => {
          game.hidden = filter !== "all" && game.dataset.gameType !== filter;
        });
      }),
    );
  }

  if (
    window.matchMedia(
      "(hover: hover) and (prefers-reduced-motion: no-preference)",
    ).matches
  ) {
    document.querySelectorAll(".tilt-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const box = card.getBoundingClientRect();
        const x = ((event.clientX - box.left) / box.width - 0.5) * 3;
        const y = ((event.clientY - box.top) / box.height - 0.5) * 3;
        card.style.transform = `translateY(-4px) rotateX(${-y}deg) rotateY(${x}deg)`;
      });
      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  }
});
