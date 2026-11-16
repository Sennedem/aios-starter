// AIOS dashboard: the single source of build truth (zero dependencies, Node 18+).
// Reads tasks.yaml, cadence.md, brain/context/priorities.md, brain/projects/*/CONTEXT.md,
// the latest brain/audits/audit-*.md and the janitor report, and writes dashboard/data.js
// as `window.AIOS_DATA`. Never edit data.js by hand; it is generated and gitignored.
// Run it from the /dashboard skill or by hand: node dashboard/build-data.mjs

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");
const BRAIN = join(ROOT, "brain");

/* ---------- helpers ---------- */
const read = (...parts) => {
  try {
    return readFileSync(join(...parts), "utf8").replace(/^﻿/, "");
  } catch {
    return "";
  }
};
const stripMd = (s) =>
  String(s)
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/\[\[([^\]|]*)\\?\|([^\]]*)\]\]/g, "$2") // [[path|Alias]] -> Alias
    .replace(/\[\[|\]\]/g, "")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1") // [text](url) -> text
    .trim();

// Split a markdown table row on unescaped pipes only ("\|" inside wikilink aliases stays in the cell).
const splitRow = (line) => {
  const ESC = "\u0000";
  return line
    .replaceAll("\\|", ESC)
    .split("|")
    .map((c) => c.trim().replaceAll(ESC, "\\|"));
};

const startOfDay = (d) => {
  const x = new Date(d);
  x.setHours(0, 0, 0, 0);
  return x;
};
const localDate = (s) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(s || "").trim());
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
};
const daysBetween = (from, to) => Math.round((startOfDay(to) - startOfDay(from)) / 86400000);

function frontmatter(text) {
  const fm = {};
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!m) return { fm, body: text };
  for (const line of m[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line);
    if (kv) fm[kv[1]] = kv[2].trim().replace(/^["']|["']$/g, "");
  }
  return { fm, body: text.slice(m[0].length) };
}

/* ---------- minimal YAML reader (flat list of scalar maps) ---------- */
function parseTasks(text) {
  const items = [];
  let cur = null;
  for (const raw of text.split(/\r?\n/)) {
    const trimmed = raw.replace(/\t/g, "  ").trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    let body = trimmed;
    if (trimmed.startsWith("- ")) {
      if (cur) items.push(cur);
      cur = {};
      body = trimmed.slice(2).trim();
    }
    if (!cur) continue;
    const idx = body.indexOf(":");
    if (idx === -1) continue;
    const key = body.slice(0, idx).trim();
    let val = body.slice(idx + 1).trim();
    val = val.replace(/\s+#.*$/, "").trim(); // strip inline comments
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'")))
      val = val.slice(1, -1);
    cur[key] = val;
  }
  if (cur) items.push(cur);
  return items.filter((t) => t.title);
}

const now = new Date();

/* ---------- projects (brain/projects/<slug>/CONTEXT.md) ---------- */
const projects = [];
try {
  for (const e of readdirSync(join(BRAIN, "projects"), { withFileTypes: true })) {
    if (!e.isDirectory() || e.name.startsWith(".") || e.name.startsWith("_")) continue;
    const text = read(BRAIN, "projects", e.name, "CONTEXT.md");
    const { fm, body } = frontmatter(text);
    const heading = /^#\s+(.+)$/m.exec(body);
    const firstLine = body
      .split(/\r?\n/)
      .map((l) => l.trim())
      .find((l) => l && !l.startsWith("#") && !l.startsWith(">") && !l.startsWith("|") && !l.startsWith("-") && !l.startsWith("<!--"));
    projects.push({
      slug: e.name,
      name: heading ? stripMd(heading[1]) : e.name,
      status: fm.status || "",
      updated: fm.updated || "",
      oneLiner: firstLine ? stripMd(firstLine).slice(0, 140) : "",
    });
  }
} catch {
  /* no projects yet */
}
projects.sort((a, b) => a.name.localeCompare(b.name));

/* ---------- tasks + deadlines ---------- */
const tasks = parseTasks(read(ROOT, "tasks.yaml")).map((t) => ({
  title: String(t.title),
  area: String(t.area || "aios").toLowerCase(),
  status: String(t.status || "todo").toLowerCase(),
  progress: Math.max(0, Math.min(100, Number(t.progress) || 0)),
  deadline: localDate(t.deadline) ? String(t.deadline).slice(0, 10) : null,
  priority: Number(t.priority) || 5,
  note: t.note ? String(t.note) : "",
  example: String(t.example).toLowerCase() === "true",
}));

const deadlines = tasks
  .filter((t) => t.deadline && t.status !== "done")
  .map((t) => ({
    title: t.title,
    date: t.deadline,
    area: t.area,
    example: t.example,
    daysLeft: daysBetween(now, localDate(t.deadline)),
  }))
  .sort((a, b) => a.daysLeft - b.daysLeft);

/* ---------- priorities (brain/context/priorities.md numbered list) ---------- */
function inferArea(text) {
  const t = text.toLowerCase();
  for (const p of projects) {
    const words = [p.slug.replace(/-/g, " "), p.name.toLowerCase()];
    if (words.some((w) => w && t.includes(w))) return p.slug;
  }
  return "aios";
}
const priorities = [];
const prioText = frontmatter(read(BRAIN, "context", "priorities.md")).body;
for (const line of prioText.split(/\r?\n/)) {
  const m = line.match(/^\s*(\d+)\.\s+(.*)$/);
  if (!m) continue;
  const text = stripMd(m[2]);
  if (!text) continue;
  priorities.push({ rank: Number(m[1]), area: inferArea(text), text });
}

/* ---------- cadence (cadence.md table, rows due today, overdue or never run) ---------- */
const cadence = [];
let cadenceRows = 0;
{
  let col = null;
  for (const line of read(ROOT, "cadence.md").split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) {
      col = null;
      continue;
    }
    if (/^\|\s*:?-/.test(line.trim())) continue;
    const cells = splitRow(line);
    const lower = cells.map((s) => s.toLowerCase().replace(/[_*`]/g, " ").replace(/\s+/g, " ").trim());
    if (lower.includes("item") && lower.includes("next due")) {
      col = {
        item: lower.indexOf("item"),
        command: lower.indexOf("command"),
        last: lower.indexOf("last run"),
        due: lower.indexOf("next due"),
      };
      continue;
    }
    if (!col) continue;
    const item = stripMd(cells[col.item] || "");
    if (!item) continue;
    cadenceRows++;
    const due = localDate(stripMd(cells[col.due] || ""));
    const last = col.last > -1 ? localDate(stripMd(cells[col.last] || "")) : null;
    const command = col.command > -1 ? stripMd(cells[col.command] || "").split(/\s/)[0] : "";
    if (due) {
      const late = daysBetween(due, now);
      if (late >= 0) cadence.push({ item, command, due: stripMd(cells[col.due]).slice(0, 10), daysLate: late, never: false });
    } else if (!last) {
      cadence.push({ item, command, due: null, daysLate: 0, never: true });
    }
  }
}
cadence.sort((a, b) => Number(b.never) - Number(a.never) || b.daysLate - a.daysLate);

/* ---------- latest audit (brain/audits/audit-*.md) + janitor report ---------- */
let audit = null;
try {
  const files = readdirSync(join(BRAIN, "audits"))
    .filter((f) => /^audit-.*\.md$/.test(f))
    .sort();
  if (files.length) {
    const name = files[files.length - 1];
    const text = read(BRAIN, "audits", name);
    const pick = (label) => {
      const m = text.match(new RegExp(`\\*\\*${label}\\*\\*\\s*\\|\\s*(\\d+)\\s*/\\s*(\\d+)`, "i"));
      return m ? { score: Number(m[1]), max: Number(m[2]) } : null;
    };
    const four = {
      context: pick("Context"),
      connections: pick("Connections"),
      capabilities: pick("Capabilities"),
      cadence: pick("Cadence"),
    };
    // Overall comes from the audit's TOTAL row ("**TOTAL** | **69 / 100**"); else the sum of the four Cs.
    const total = text.match(/TOTAL\*\*\s*\|\s*\*\*\s*(\d+)\s*\/\s*(\d+)/i);
    const parts = Object.values(four).filter(Boolean);
    audit = {
      file: `brain/audits/${name}`,
      overall: total ? Number(total[1]) : parts.length ? parts.reduce((s, c) => s + c.score, 0) : null,
      overallMax: total ? Number(total[2]) : 100,
      ...four,
    };
  }
} catch {
  /* no audits yet */
}

let janitor = null;
{
  const text = read(BRAIN, "audits", "janitor-latest.md");
  if (text) {
    const { fm } = frontmatter(text);
    const defects = text.match(/structural defects[^|]*\|\s*\*\*(\d+)\*\*/i);
    janitor = {
      file: "brain/audits/janitor-latest.md",
      date: fm.updated || "",
      defects: defects ? Number(defects[1]) : null,
      failed: /\(FAILED\)/.test(text),
    };
  }
}

/* ---------- emit ---------- */
const data = {
  generatedAt: now.toISOString(),
  projects,
  tasks,
  deadlines,
  priorities,
  cadence,
  cadenceRows,
  audit,
  janitor,
};

const out = `// AUTO-GENERATED by dashboard/build-data.mjs. Do not edit by hand.\nwindow.AIOS_DATA = ${JSON.stringify(data, null, 2)};\n`;
writeFileSync(join(HERE, "data.js"), out, "utf8");

console.log(
  `[aios] data.js written: ${tasks.length} tasks, ${deadlines.length} deadlines, ` +
    `${projects.length} projects, ${priorities.length} priorities, ${cadence.length} cadence rows due, ` +
    `audit ${audit ? "found" : "none"}, janitor report ${janitor ? "found" : "none"}.`,
);
