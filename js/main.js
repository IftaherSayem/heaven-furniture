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
})();
