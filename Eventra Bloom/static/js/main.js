// ── Nav toggle ──
const navToggle = document.querySelector('.nav-toggle');
const navLinks  = document.querySelector('.nav-links');
const navActions = document.querySelector('.nav-actions');

if (navToggle) {
  navToggle.addEventListener('click', () => {
    navLinks?.classList.toggle('open');
    navActions?.classList.toggle('open');
    navToggle.textContent = navToggle.textContent === '☰' ? '✕' : '☰';
  });
}

// ── Auto-dismiss alerts ──
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity 0.5s, transform 0.5s';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-10px)';
    setTimeout(() => alert.remove(), 500);
  }, 4000);
});

// ── Animate cards on scroll ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      entry.target.style.animationDelay = `${i * 0.08}s`;
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.event-card, .dash-stat-card, .announcement-card').forEach(el => {
  el.style.opacity = '0';
  observer.observe(el);
});

// ── Stat counter animation ──
function animateCount(el) {
  const target = parseInt(el.dataset.target || el.textContent, 10);
  if (isNaN(target)) return;
  let current = 0;
  const step = target / 40;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.round(current);
    if (current >= target) clearInterval(timer);
  }, 30);
}

document.querySelectorAll('.stat-number, .dash-stat-number').forEach(el => {
  el.dataset.target = el.textContent.replace(/\D/g,'');
  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) { animateCount(el); obs.disconnect(); }
  });
  obs.observe(el);
});

// ── Tab switching ──
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
    btn.classList.add('active');
    const pane = document.getElementById(target);
    if (pane) pane.style.display = 'block';
  });
});

// Show first tab by default
const firstTab = document.querySelector('.tab-btn');
if (firstTab) firstTab.click();

// ── Search filter (client side for filters bar) ──
const searchInput = document.querySelector('#search-input');
if (searchInput) {
  searchInput.addEventListener('input', debounce(() => {
    const query = searchInput.value.toLowerCase();
    document.querySelectorAll('.event-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(query) ? '' : 'none';
    });
  }, 200));
}

function debounce(fn, delay) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}

// ── Confirm delete ──
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', e => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// ── Category pill colors ──
const categoryColors = {
  default: { bg: '#F5F0FF', border: '#C9B8FF', text: '#6A4FA0' }
};

// ── Smooth page load ──
document.body.style.opacity = '0';
window.addEventListener('load', () => {
  document.body.style.transition = 'opacity 0.4s ease';
  document.body.style.opacity = '1';
});

// ── Registration countdown ──
const deadlineEl = document.querySelector('[data-deadline]');
if (deadlineEl) {
  const deadline = new Date(deadlineEl.dataset.deadline);
  function updateCountdown() {
    const now = new Date();
    const diff = deadline - now;
    if (diff <= 0) { deadlineEl.textContent = 'Registration closed'; return; }
    const days = Math.floor(diff / 86400000);
    const hours = Math.floor((diff % 86400000) / 3600000);
    const mins = Math.floor((diff % 3600000) / 60000);
    deadlineEl.textContent = days > 0
      ? `${days}d ${hours}h remaining`
      : `${hours}h ${mins}m remaining`;
  }
  updateCountdown();
  setInterval(updateCountdown, 60000);
}
