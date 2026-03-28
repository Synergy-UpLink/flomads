// Nav scroll behavior
const nav = document.getElementById('main-nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 40);
});

// Mobile toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
  toggle.addEventListener('click', () => {
    links.classList.toggle('open');
    toggle.textContent = links.classList.contains('open') ? '✕' : '☰';
  });
}

// Duplicate strip for infinite scroll
const strip = document.querySelector('.strip-inner');
if (strip) {
  const clone = strip.cloneNode(true);
  strip.parentElement.appendChild(clone);
}
