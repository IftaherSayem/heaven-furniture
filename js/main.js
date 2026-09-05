/* ============================================================
   HEAVEN FURNITURE MART — main.js
   - Sticky header state
   - Mobile menu
   - Scroll reveal
   - Auto-load real photos from /images if present
   ============================================================ */

(function () {
  "use strict";

  /* ---------- Current year in footer ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Sticky header ---------- */
  var header = document.getElementById("siteHeader");
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 40) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      menu.hidden = open;
    });
    // Close after clicking a link
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        menu.hidden = true;
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealTargets = document.querySelectorAll(
    ".section-head, .intro-copy, .intro-figure, .collection-card, .bespoke-copy, .bespoke-figure, .why-item, .md-quote, .timeline li, .cta-content"
  );
  revealTargets.forEach(function (el) { el.classList.add("reveal"); });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealTargets.forEach(function (el) { io.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Auto-load real photos ----------
     Every element with data-img="name.jpg" tries to load
     images/<name>. If the file exists, it becomes the
     background and the placeholder texture is removed.
     Drop your downloaded Heaven photos into /images with the
     matching filename and they appear — no code changes needed.
  ------------------------------------------------------------ */
  var slots = document.querySelectorAll("[data-img]");
  slots.forEach(function (slot) {
    var file = slot.getAttribute("data-img");
    if (!file) return;
    var url = "images/" + file;
    var probe = new Image();
    probe.onload = function () {
      slot.style.backgroundImage = 'url("' + url + '")';
      slot.classList.add("has-img");
    };
    probe.onerror = function () {
      /* leave elegant placeholder in place */
    };
    probe.src = url;
  });

  /* ---------- Animated trust counters ---------- */
  var counters = document.querySelectorAll('.trust-num[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var counterIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-count'), 10);
        var duration = 1800;
        var start = performance.now();
        function tick(now) {
          var elapsed = now - start;
          var progress = Math.min(elapsed / duration, 1);
          var eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.round(eased * target);
          if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        counterIO.unobserve(el);
      });
    }, { threshold: 0.3 });
    counters.forEach(function (c) { counterIO.observe(c); });
  }

  /* ---------- Quote form → WhatsApp redirect ---------- */
  var quoteForm = document.getElementById('quoteForm');
  if (quoteForm) {
    quoteForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = document.getElementById('qfName').value.trim();
      var phone = document.getElementById('qfPhone').value.trim();
      var interest = document.getElementById('qfInterest').value || 'Not specified';
      var message = document.getElementById('qfMessage').value.trim();
      var text = 'Hi Heaven Furniture Mart!%0A%0A'
               + 'Name: ' + encodeURIComponent(name) + '%0A'
               + 'Phone: ' + encodeURIComponent(phone) + '%0A'
               + 'Interest: ' + encodeURIComponent(interest) + '%0A'
               + 'Message: ' + encodeURIComponent(message || 'N/A');
      window.open('https://wa.me/8801960481983?text=' + text, '_blank');
    });
  }
})();
