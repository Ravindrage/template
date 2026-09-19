// ---- Services dropdown ----
document.querySelectorAll('.dropdown-toggle').forEach(function(btn){
  btn.addEventListener('click', function(e){
    e.stopPropagation();
    var dd = btn.closest('.dropdown');
    var wasOpen = dd.classList.contains('open');
    document.querySelectorAll('.dropdown.open').forEach(function(d){ d.classList.remove('open'); });
    if(!wasOpen) dd.classList.add('open');
  });
});
document.addEventListener('click', function(){
  document.querySelectorAll('.dropdown.open').forEach(function(d){ d.classList.remove('open'); });
});

// ---- FAQ accordion ----
document.querySelectorAll('.faq-q').forEach(function(btn){
  btn.addEventListener('click', function(){
    var item = btn.closest('.faq-item');
    var answer = item.querySelector('.faq-a');
    var isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(function(openItem){
      if(openItem !== item){
        openItem.classList.remove('open');
        openItem.querySelector('.faq-a').style.maxHeight = null;
        openItem.querySelector('.faq-q').setAttribute('aria-expanded','false');
      }
    });
    if(isOpen){
      item.classList.remove('open');
      answer.style.maxHeight = null;
      btn.setAttribute('aria-expanded','false');
    } else {
      item.classList.add('open');
      answer.style.maxHeight = answer.scrollHeight + 'px';
      btn.setAttribute('aria-expanded','true');
    }
  });
});

// ---- Scroll-triggered lead modal (shows once per session, per tab) ----
(function(){
  var modal = document.getElementById('leadModal');
  if(!modal) return;
  var closeBtn = document.getElementById('modalClose');
  var shown = false;

  function maybeShow(){
    if(shown) return;
    var scrolled = window.scrollY + window.innerHeight;
    var full = document.documentElement.scrollHeight;
    if(scrolled > full * 0.45){
      if(sessionStorage.getItem('backstageModalSeen')) { shown = true; return; }
      modal.classList.add('visible');
      shown = true;
      sessionStorage.setItem('backstageModalSeen','1');
    }
  }

  window.addEventListener('scroll', function(){
    window.requestAnimationFrame(maybeShow);
  }, {passive:true});

  function closeModal(){ modal.classList.remove('visible'); }
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e){ if(e.target === modal) closeModal(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeModal(); });
})();
