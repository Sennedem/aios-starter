/* AIOS dashboard: render layer. Reads window.AIOS_DATA (from data.js, written by build-data.mjs). */
(function () {
  "use strict";
  const D = window.AIOS_DATA || null;
  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Areas are project slugs from brain/projects/, plus "aios" for work on the system itself.
  const PALETTE = ["#38bdf8", "#f472b6", "#2dd4bf", "#fbbf24", "#3b82f6", "#fb923c", "#34d399", "#e879f9"];
  const AREA = { aios: { color: "#a78bfa", label: "AIOS" } };
  ((D && D.projects) || []).forEach((p, i) => {
    AREA[p.slug] = { color: PALETTE[i % PALETTE.length], label: p.name || p.slug };
  });
  const area = (a) => AREA[a] || { color: "#94a3b8", label: a || "Other" };

  const $ = (id) => document.getElementById(id);
  const esc = (s) =>
    String(s == null ? "" : s).replace(
      /[&<>"']/g,
      (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]),
    );
  // `html` is trusted markup built in this file; every data value passes through esc() first.
  const el = (tag, cls, html) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  };
  const empty = (wrap, html) => wrap.appendChild(el("p", "empty", html));
  const fmtDate = (iso, opts) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || "");
    if (!m) return iso || "";
    return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])).toLocaleDateString(undefined, opts);
  };

  /* ---------- clock ---------- */
  function tickClock() {
    const now = new Date();
    const t = $("clock");
    const d = $("date");
    if (t) t.textContent = now.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    if (d)
      d.textContent = now
        .toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long", year: "numeric" })
        .toUpperCase();
  }
  tickClock();
  setInterval(tickClock, 1000);

  /* ---------- count-up ---------- */
  function countUp(node, target) {
    if (REDUCED) {
      node.textContent = String(target);
      return;
    }
    const dur = 1100;
    const start = performance.now();
    function step(t) {
      const p = Math.min(1, (t - start) / dur);
      node.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- system health: latest audit + janitor ---------- */
  function renderHealth() {
    const a = D.audit;
    const cees = $("cees");
    const reports = $("reports");
    if (a && a.overall != null) {
      countUp($("health-overall"), a.overall);
      $("health-unit").textContent = "/ " + a.overallMax;
      const arc = $("reactor-arc");
      const C = 2 * Math.PI * 38;
      setTimeout(() => (arc.style.strokeDashoffset = C * (1 - Math.min(1, a.overall / (a.overallMax || 100)))), 120);
      [
        ["Context", a.context],
        ["Connections", a.connections],
        ["Capabilities", a.capabilities],
        ["Cadence", a.cadence],
      ].forEach(([label, c]) => {
        if (!c) return;
        const row = el("div", "cee");
        row.appendChild(el("span", "cee-label", esc(label)));
        const bar = el("div", "cee-bar");
        const fill = el("div", "cee-fill");
        bar.appendChild(fill);
        row.appendChild(bar);
        row.appendChild(el("span", "cee-val", esc(c.score + "/" + c.max)));
        cees.appendChild(row);
        setTimeout(() => (fill.style.width = (c.score / (c.max || 1)) * 100 + "%"), 150);
      });
    } else {
      empty(cees, "No audit yet. Run <code>/audit</code> in Claude Code for the first score.");
    }

    const link = (file, label) => '<a href="../' + esc(file) + '">' + esc(label) + "</a>";
    if (a) reports.appendChild(el("div", "report-row", "Latest audit: " + link(a.file, a.file.split("/").pop())));
    const j = D.janitor;
    if (j) {
      const what = j.failed
        ? '<span class="bad">crashed</span>'
        : j.defects == null
          ? "report"
          : j.defects === 0
            ? '<span class="good">0 structural defects</span>'
            : '<span class="warn">' + esc(j.defects) + " structural defects</span>";
      reports.appendChild(
        el("div", "report-row", "Janitor " + esc(fmtDate(j.date, { day: "numeric", month: "short" })) + ": " + what + " (" + link(j.file, "report") + ")"),
      );
    } else {
      reports.appendChild(el("div", "report-row", "No janitor report yet. Run <code>node scripts/brain-janitor.mjs</code>."));
    }
  }

  /* ---------- deadlines ---------- */
  function deadlineColor(days) {
    if (days < 7) return "#ef4444";
    if (days < 14) return "#fbbf24";
    return "#38bdf8";
  }
  function renderDeadlines() {
    const wrap = $("deadlines");
    const list = (D.deadlines || []).slice(0, 8);
    if (!list.length) {
      empty(wrap, "No upcoming deadlines. Give a task in <code>tasks.yaml</code> a <code>deadline:</code> and it shows here.");
      return;
    }
    list.forEach((d) => {
      const color = deadlineColor(d.daysLeft);
      const item = el("div", "dl-item");
      item.style.borderLeftColor = color;
      const count = el("div", "dl-count");
      const days = el("span", "dl-days");
      days.style.color = color;
      const overdue = d.daysLeft < 0;
      // The placeholder task carries a far-future date so it never reads as late; show a sample count.
      if (d.example) days.textContent = "21";
      else countUp(days, Math.abs(d.daysLeft));
      count.appendChild(days);
      count.appendChild(el("span", "dl-dlabel", overdue ? "days late" : "days"));
      const main = el("div", "dl-main");
      main.appendChild(el("div", "dl-title", esc(d.title) + (d.example ? ' <span class="chip-example">example</span>' : "")));
      main.appendChild(
        el("div", "dl-meta", esc(area(d.area).label) + " &middot; " + (d.example ? "your deadline date" : esc(fmtDate(d.date, { weekday: "short", day: "numeric", month: "short" })))),
      );
      item.appendChild(count);
      item.appendChild(main);
      wrap.appendChild(item);
    });
  }

  /* ---------- tasks (grouped by area) ---------- */
  function renderTasks() {
    const wrap = $("tasks");
    const tasks = D.tasks || [];
    if (!tasks.length) {
      empty(wrap, "No tasks yet. Add them to <code>tasks.yaml</code>, or ask Claude to capture a goal with <code>/goal</code>.");
      return;
    }
    const groups = {};
    tasks.forEach((t) => (groups[t.area] = groups[t.area] || []).push(t));
    const order = ((D.projects || []).map((p) => p.slug).concat(["aios"]))
      .filter((a) => groups[a])
      .concat(Object.keys(groups).filter((a) => !AREA[a]));
    order.forEach((a) => {
      const meta = area(a);
      const label = el("div", "task-group-label", esc(meta.label));
      label.style.setProperty("--area", meta.color);
      wrap.appendChild(label);
      groups[a]
        .slice()
        .sort((x, y) => (x.priority || 9) - (y.priority || 9))
        .forEach((t) => {
          const row = el("div", "task" + (t.status === "done" ? " done" : ""));
          row.style.setProperty("--area", meta.color);
          if (t.note) row.title = t.note;
          const title = el("div", "task-title", esc(t.title));
          title.appendChild(el("span", "task-status s-" + esc(t.status), esc((t.status || "todo").replace("-", " "))));
          if (t.example) title.appendChild(el("span", "chip-example", "example"));
          row.appendChild(title);
          row.appendChild(el("div", "task-pct", esc((t.progress || 0) + "%")));
          const bar = el("div", "task-bar");
          const fill = el("div", "task-fill");
          bar.appendChild(fill);
          row.appendChild(bar);
          wrap.appendChild(row);
          setTimeout(() => (fill.style.width = (t.progress || 0) + "%"), 160);
        });
    });
  }

  /* ---------- cadence rows due ---------- */
  function renderCadence() {
    const wrap = $("cadence");
    const rows = D.cadence || [];
    if (!D.cadenceRows) {
      empty(wrap, "No recurring work in <code>cadence.md</code> yet.");
      return;
    }
    if (!rows.length) {
      empty(wrap, "Nothing due. All " + esc(D.cadenceRows) + " cadence rows are on schedule.");
      return;
    }
    rows.forEach((r) => {
      const row = el("div", "cd-item" + (r.never ? " never" : r.daysLate > 0 ? " late" : ""));
      row.appendChild(el("div", "cd-title", esc(r.item)));
      const when = r.never ? "never run" : r.daysLate > 0 ? r.daysLate + "d overdue" : "due today";
      row.appendChild(el("div", "cd-meta", (r.command ? "<code>" + esc(r.command) + "</code> &middot; " : "") + esc(when)));
      wrap.appendChild(row);
    });
  }

  /* ---------- projects + priorities ---------- */
  const STATUS_COLOR = { active: "#34d399", building: "#38bdf8", paused: "#fbbf24", archived: "#64748b", draft: "#94a3b8", template: "#94a3b8" };
  function renderStatus() {
    const pwrap = $("projects");
    const projects = D.projects || [];
    if (!projects.length) {
      empty(pwrap, "No projects yet. Each folder in <code>brain/projects/</code> shows up here; <code>/setup</code> creates the first ones.");
    }
    projects.forEach((p) => {
      const color = STATUS_COLOR[p.status] || area(p.slug).color;
      const card = el("div", "project");
      const dot = el("span", "v-dot");
      dot.style.background = area(p.slug).color;
      card.appendChild(dot);
      const main = el("div", "v-main");
      main.appendChild(el("div", "v-name", esc(p.name)));
      if (p.oneLiner) main.appendChild(el("div", "v-goal", esc(p.oneLiner)));
      card.appendChild(main);
      if (p.status) {
        const st = el("span", "v-status", esc(p.status));
        st.style.color = color;
        card.appendChild(st);
      }
      pwrap.appendChild(card);
    });

    const list = $("priorities");
    const prios = D.priorities || [];
    if (!prios.length) {
      list.replaceWith(el("p", "empty", "No priorities yet. Write a numbered list in <code>brain/context/priorities.md</code>."));
      return;
    }
    prios.forEach((p) => {
      const li = el("li", "prio-item");
      const rank = el("span", "prio-rank", esc(p.rank));
      rank.style.background = area(p.area).color;
      li.appendChild(rank);
      li.appendChild(el("span", null, esc(p.text)));
      list.appendChild(li);
    });
  }

  /* ---------- setup banner + footer ---------- */
  function renderBanner() {
    const examples = (D.tasks || []).some((t) => t.example);
    const fresh = !(D.projects || []).length;
    if (!examples && !fresh) return;
    const b = $("setup-banner");
    b.innerHTML = "Fresh install: " + (examples ? "the tasks marked <em>example</em> are placeholders. " : "") + "Run <code>/setup</code> in Claude Code to fill this dashboard with your own projects, tasks and priorities.";
    b.hidden = false;
  }
  function renderFooter() {
    const info = $("gen-info");
    if (info && D.generatedAt) {
      info.textContent =
        "DATA GENERATED " +
        new Date(D.generatedAt).toLocaleString(undefined, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }).toUpperCase();
    }
  }

  /* ---------- boot ---------- */
  if (!D) {
    const b = $("setup-banner");
    b.innerHTML = "No <code>data.js</code> yet. Run <code>node dashboard/build-data.mjs</code> from the repo root (or <code>/dashboard</code> in Claude Code), then reload this page.";
    b.hidden = false;
    document.querySelector(".grid").hidden = true;
    return;
  }
  renderBanner();
  renderHealth();
  renderDeadlines();
  renderTasks();
  renderCadence();
  renderStatus();
  renderFooter();
})();
