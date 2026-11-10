/* RewardedTasks Brasil - Interatividade & Suporte AdSense */
document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Menu Toggle
  var toggle = document.querySelector('.mobile-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isVisible = nav.style.display === 'flex';
      nav.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {
        nav.style.flexDirection = 'column';
        nav.style.position = 'absolute';
        nav.style.top = '72px';
        nav.style.left = '0';
        nav.style.width = '100%';
        nav.style.background = '#ffffff';
        nav.style.padding = '20px';
        nav.style.boxShadow = '0 10px 15px -3px rgba(0,0,0,0.1)';
        nav.style.zIndex = '99';
      }
    });
  }

  // 2. Newsletter Form Submission Handler
  var newsForm = document.querySelector('.widget-newsletter form');
  if (newsForm) {
    newsForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = newsForm.querySelector('input');
      var btn = newsForm.querySelector('button');
      if (input && input.value) {
        btn.textContent = 'Subscribed successfully!';
        btn.style.background = '#059669';
        input.value = '';
        setTimeout(function () {
          btn.textContent = 'Subscribe Free';
          btn.style.background = '#10b981';
        }, 3000);
      }
    });
  }

  // 3. Share Buttons
  var shareBtns = document.querySelectorAll('[data-share]');
  shareBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var type = btn.getAttribute('data-share');
      var url = encodeURIComponent(window.location.href);
      var title = encodeURIComponent(document.title);
      if (type === 'whatsapp') {
        window.open('https://api.whatsapp.com/send?text=' + title + '%20' + url, '_blank');
      } else if (type === 'twitter') {
        window.open('https://twitter.com/intent/tweet?text=' + title + '&url=' + url, '_blank');
      } else if (type === 'copy') {
        navigator.clipboard.writeText(window.location.href).then(function () {
          alert('Link copied to clipboard!');
        });
      }
    });
  });

  // 4. Dynamic Year
  var yearEls = document.querySelectorAll('.current-year');
  var currentYear = new Date().getFullYear();
  yearEls.forEach(function (el) {
    el.textContent = currentYear;
  });
});
