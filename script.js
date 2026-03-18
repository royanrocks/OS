const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const navAnchors = document.querySelectorAll(".nav-links a");
const sectionMap = new Map();

for (const anchor of navAnchors) {
  const id = anchor.getAttribute("href");
  if (!id || !id.startsWith("#")) continue;
  const section = document.querySelector(id);
  if (section) {
    sectionMap.set(section, anchor);
  }
}

let lastY = window.scrollY;
let ticking = false;

const onScroll = () => {
  const y = window.scrollY;
  const delta = y - lastY;
  if (Math.abs(delta) > 20) {
    if (delta > 0 && y > 100) {
      header?.classList.add("is-hidden");
    } else {
      header?.classList.remove("is-hidden");
    }
    lastY = y;
  }
  ticking = false;
};

window.addEventListener("scroll", () => {
  if (!ticking) {
    window.requestAnimationFrame(onScroll);
    ticking = true;
  }
});

navToggle?.addEventListener("click", () => {
  const open = navLinks?.classList.toggle("is-open");
  navToggle.setAttribute("aria-expanded", open ? "true" : "false");
});

for (const anchor of navAnchors) {
  anchor.addEventListener("click", () => {
    navLinks?.classList.remove("is-open");
    navToggle?.setAttribute("aria-expanded", "false");
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      const linkedAnchor = sectionMap.get(entry.target);
      if (!linkedAnchor) continue;
      if (entry.isIntersecting) {
        navAnchors.forEach((a) => a.classList.remove("is-active"));
        linkedAnchor.classList.add("is-active");
      }
    }
  },
  { threshold: 0.45 }
);

for (const section of sectionMap.keys()) {
  observer.observe(section);
}
