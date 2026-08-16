// Preserves the scroll position of the DocSy left sidebar across page navigations.
//
// Each page is a full static render, so the sidebar DOM is rebuilt and its scroll
// offset resets to the top. This script stores the sidebar's scrollTop in
// sessionStorage (shared across pages, per-tab, per-session) and restores it on
// each load, so your "where I am in the nav list" survives clicking a link.
// On the first load of a session (no saved value yet) it anchors the
// currently-active row into view.
//
// The inner <nav id="td-section-nav"> is the scroll container in DocSy
// (overflow-y: auto + max-height). We fall back to #td-sidebar-menu so the
// script keeps working if the id ever changes.
//
// Injected via the DocSy extension hook: layouts/partials/hooks/body-end.html
// To revert: delete this file and layouts/partials/hooks/body-end.html.
(function () {
  var KEY = 'docsy-sidebar-scroll';

  function el() {
    return document.getElementById('td-section-nav') ||
           document.getElementById('td-sidebar-menu');
  }

  var pending = false;
  function save() {
    var e = el();
    if (e) {
      try { sessionStorage.setItem(KEY, String(e.scrollTop)); } catch (_) {}
    }
    pending = false;
  }
  function onScroll() {
    if (!pending) { pending = true; requestAnimationFrame(save); }
  }

  function clamp(e, v) {
    return Math.max(0, Math.min(v, e.scrollHeight - e.clientHeight));
  }

  function restore() {
    var e = el();
    if (!e) return;

    var stored = null;
    try { stored = sessionStorage.getItem(KEY); } catch (_) {}

    if (stored !== null) {
      var v = parseInt(stored, 10);
      if (!isNaN(v)) { e.scrollTop = clamp(e, v); return; }
    }

    // First load of the session: anchor the currently-active row into view.
    var marker = document.querySelector('.td-sidebar-nav-active-item');
    if (!marker) return;
    var row = marker.closest('li') || marker;
    var eRect = e.getBoundingClientRect();
    var rRect = row.getBoundingClientRect();
    var top = (rRect.top - eRect.top) + e.scrollTop - 20;
    e.scrollTop = clamp(e, top);
  }

  function init() {
    var e = el();
    if (!e) return;
    e.addEventListener('scroll', onScroll, { passive: true });
    restore();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
