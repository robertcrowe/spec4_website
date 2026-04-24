// Agents dropdown
document.querySelectorAll('.nav-dropdown').forEach(function(dropdown) {
  var toggle = dropdown.querySelector('.nav-dropdown-toggle');
  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });
  document.addEventListener('click', function() {
    dropdown.classList.remove('open');
  });
  dropdown.addEventListener('click', function(e) { e.stopPropagation(); });
});

// Mobile menu
var navToggle = document.querySelector('.nav-toggle');
var mobileMenu = document.querySelector('.mobile-menu');
if (navToggle && mobileMenu) {
  navToggle.addEventListener('click', function() {
    mobileMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
  });
  mobileMenu.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() {
      mobileMenu.classList.remove('active');
      navToggle.classList.remove('active');
    });
  });
}

// Scroll: nav background
var nav = document.querySelector('.nav');
window.addEventListener('scroll', function() {
  nav.style.background = window.pageYOffset > 80
    ? 'rgba(10, 10, 15, 0.97)'
    : 'rgba(10, 10, 15, 0.85)';
}, { passive: true });

// Smooth scroll for same-page anchors
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
  anchor.addEventListener('click', function(e) {
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - 84, behavior: 'smooth' });
    }
  });
});

// Fade-in on scroll
if ('IntersectionObserver' in window) {
  var io = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-in').forEach(function(el) { io.observe(el); });
}
