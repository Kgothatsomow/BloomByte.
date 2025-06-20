// Javascript for BloomByte
// 🌟 BloomByte script.js

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for anchor links
  const links = document.querySelectorAll('a[href^="#"]');
  for (let link of links) {
    link.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Optional: Add a fade-in animation on page load
  document.body.style.opacity = 0;
  setTimeout(() => {
    document.body.style.transition = 'opacity 0.8s ease';
    document.body.style.opacity = 1;
  }, 100);
});

// 🌗 Dark Mode Toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.createElement('button');
  toggle.textContent = '🌙 Toggle Theme';
  toggle.className = 'run-btn';
  document.body.insertBefore(toggle, document.body.firstChild);

  toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    alert('Theme changed!');
  });
});
// 📚 Filter Lessons
function filterLessons(topic) {
  document.querySelectorAll('.lesson-card').forEach(card => {
    card.style.display = topic === 'all' || card.dataset.topic === topic ? 'block' : 'none';
  });
}

// ✨ Reveal lesson cards one at a time
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.lesson-card');
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.style.animation = 'fadeIn 0.5s ease forwards';
      card.style.animationDelay = `${index * 200}ms`;
    }, index * 200);
  });
});

// 💬 Reusable alert popup
function showAlert(message) {
  const alertBox = document.getElementById('alert');
  if (alertBox) {
    alertBox.textContent = message;
    alertBox.style.display = 'block';
    setTimeout(() => {
      alertBox.style.display = 'none';
    }, 4000);
  }
}

toggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  showAlert('Theme changed!');
});