/* FlowState home page: scroll reveals, the rest clock, and the "log a set" demo. No library, no network.
   The page is complete without this file: it only adds motion. Nothing is hidden until it is running. */
(() => {
  const d = document, root = d.documentElement;
  const $$ = (s) => [...d.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fmt = (s) => Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");

  // Scroll reveals, once each. js-ready is added only after the observer exists. An element the reader has
  // already scrolled past (anchor jump, restored scroll) is revealed too, and if the observer never reports
  // anything the timeout reveals everything, so nothing can stay hidden.
  try {
    let reported = 0;
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      reported++;
      if (e.isIntersecting || e.boundingClientRect.top < 0) { e.target.classList.add("in"); io.unobserve(e.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal, .reveal-ring").forEach((el) => io.observe(el));
    root.classList.add("js-ready");
    setTimeout(() => { if (!reported) $$(".reveal, .reveal-ring").forEach((el) => el.classList.add("in")); }, 1500);
  } catch (_) { /* leave everything visible */ }

  if (reduce || !("IntersectionObserver" in window)) return;

  // Run something only while an element is on screen and the tab is visible.
  const whileVisible = (el, on, off, margin = "0px") => {
    let seen = false, running = false;
    const sync = () => {
      const go = seen && !d.hidden;
      if (go && !running) { running = true; on(); } else if (!go && running) { running = false; off(); }
    };
    new IntersectionObserver((es) => { seen = es[es.length - 1].isIntersecting; sync(); }, { rootMargin: margin }).observe(el);
    d.addEventListener("visibilitychange", sync);
  };

  // The rest clock in the capsule and on the Lock Screen card: one second per second from 1:12, the capsule
  // ring draining with it (of a 90 second rest). At 0:00 it waits a moment and starts over.
  const exhibit = d.querySelector(".exhibit");
  const clocks = $$("[data-clock]"), arcs = $$(".cap-arc"), START = 72, TOTAL = 90;
  if (exhibit && clocks.length) {
    let left = START, base = START, t0 = 0, timer = 0;
    const paint = () => {
      clocks.forEach((c) => { c.textContent = fmt(left); });
      arcs.forEach((a) => { a.style.strokeDasharray = (left / TOTAL) * 100 + " 100"; });
    };
    const restart = () => {
      arcs.forEach((a) => { a.style.transition = "none"; });
      left = base = START; paint();
      arcs[0] && arcs[0].getBoundingClientRect();
      arcs.forEach((a) => { a.style.transition = ""; });
      begin();
    };
    const step = () => {
      left = Math.max(0, base - Math.floor((performance.now() - t0) / 1000)); paint();
      timer = setTimeout(left ? step : restart, left ? 1000 - ((performance.now() - t0) % 1000) : 1400);
    };
    const begin = () => { base = left; t0 = performance.now(); timer = setTimeout(step, 1000); };
    whileVisible(exhibit, () => (left ? begin() : restart()), () => clearTimeout(timer));
  }

  // "Log the set": the button presses, set 2's check draws, the rest strip rises and counts down from 1:30.
  // Replays about every 9 seconds while in view. Out of view it stops and shows the finished state.
  $$(".demo").forEach((demo) => {
    const clock = demo.querySelector("[data-rest]"), line = demo.querySelector(".rline"), timers = [];
    const at = (ms, fn) => timers.push(setTimeout(fn, ms));
    const flag = (c, on) => demo.classList.toggle(c, on);
    const paint = (s) => { clock.textContent = fmt(s); line.style.transform = "scaleX(" + s / 90 + ")"; };
    const stop = () => { timers.splice(0).forEach(clearTimeout); };
    const play = () => {
      stop(); flag("pre", true); flag("logged", false); flag("resting", false); paint(90);
      at(700, () => flag("press", true));
      at(860, () => { flag("press", false); flag("logged", true); });
      at(1250, () => flag("resting", true));
      for (let i = 1; i <= 6; i++) at(1250 + i * 1000, () => paint(90 - i));
      at(8000, () => { flag("logged", false); flag("resting", false); });
      at(9000, play);
    };
    whileVisible(demo, play, () => { stop(); ["pre", "press", "logged", "resting"].forEach((c) => flag(c, false)); paint(90); }, "0px 0px -20% 0px");
  });
})();
