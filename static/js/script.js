document.addEventListener('DOMContentLoaded', () => {
  AOS.init({ duration: 700, once: true, offset: 70 });

  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('show'));
  }

  const counters = document.querySelectorAll('.counter');
  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    let current = 0;
    const updateCounter = () => {
      current += Math.max(1, Math.floor(target / 20));
      if (current >= target) {
        counter.textContent = target;
        return;
      }
      counter.textContent = current;
      requestAnimationFrame(updateCounter);
    };
    updateCounter();
  });

  const scrollTopBtn = document.getElementById('scrollTop');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.style.display = window.scrollY > 300 ? 'grid' : 'none';
    });
    scrollTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  const searchInput = document.querySelector('input[name="search"]');
  if (searchInput) {
    searchInput.addEventListener('input', (event) => {
      const value = event.target.value.toLowerCase();
      document.querySelectorAll('.product-card').forEach((card) => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(value) ? '' : 'none';
      });
    });
  }

  const forms = document.querySelectorAll('.contact-form');
  forms.forEach((form) => {
    form.addEventListener('submit', (event) => {
      const requiredFields = form.querySelectorAll('input[required], textarea[required]');
      let isValid = true;
      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = '#ff6767';
        } else {
          field.style.borderColor = '';
        }
      });
      if (!isValid) {
        event.preventDefault();
      }
    });
  });
});
