/* GRID 메인 v2 — 화면에 들어오면 [data-v2-in]에 is-in */
(function () {
  var els = [].slice.call(document.querySelectorAll('[data-v2-in]'));
  if (!els.length) return;
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('is-in'); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px' });
  els.forEach(function (e) { io.observe(e); });
})();

/* 22개 부위 — Upper/Mid/Lower 탭: 해당 점 켜기 + 목록 바꾸기 (처음엔 사진만 깨끗하게, 화면에 들어오면 Upper부터) */
(function () {
  var box = document.querySelector('[data-v2map]');
  if (!box) return;
  var tabs = [].slice.call(box.querySelectorAll('.v2zm__tab'));
  var dots = [].slice.call(box.querySelectorAll('.v2zm__dot'));
  var lists = [].slice.call(box.querySelectorAll('.v2zm__ol'));
  function show(z) {
    tabs.forEach(function (t) { var on = t.dataset.zone === z; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
    dots.forEach(function (d) { d.classList.toggle('is-on', d.dataset.zone === z); });
    lists.forEach(function (l) { l.classList.toggle('is-on', l.dataset.zone === z); });
  }
  tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.dataset.zone); }); });
  var img = box.querySelector('.v2zm__img');
  if (!('IntersectionObserver' in window)) { show(tabs[0].dataset.zone); return; }
  var io = new IntersectionObserver(function (es) {
    if (es[0].isIntersecting) { show((box.querySelector('.v2zm__tab.is-on') || tabs[0]).dataset.zone); io.disconnect(); }
  }, { threshold: .45 });
  // 들어오기 전엔 점을 꺼 둔다
  dots.forEach(function (d) { d.classList.remove('is-on'); });
  io.observe(img);
})();

/* 5초 스탬핑 영상 — 소리 켜기/끄기, 화면 밖에서는 멈춤 */
(function () {
  var v = document.querySelector('.v2stamp__video');
  if (!v) return;
  var b = document.querySelector('.v2stamp__snd');
  if (b) b.addEventListener('click', function () {
    v.muted = !v.muted;
    if (!v.muted) { v.play(); }
    b.setAttribute('aria-pressed', v.muted ? 'false' : 'true');
    b.setAttribute('aria-label', v.muted ? '소리 켜기' : '소리 끄기');
  });
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; }
  if (!('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { if (v.autoplay) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } } else { v.pause(); } });
  }, { threshold: .25 }).observe(v);
})();
