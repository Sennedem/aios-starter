#!/usr/bin/env node
/**
 * brain-janitor.mjs: deterministic structural lint of brain/ and the OS ledgers.
 *
 * Report-only: never edits content, never deletes, always exits 0 and always leaves
 * a report. The weekly /audit quotes its counts instead of re-deriving them, so the
 * same question always gets the same answer.
 *
 * Usage: node scripts/brain-janitor.mjs [--local] [--fix] [--quiet] [--out <file>]
 *   --local  also run machine-only checks (inbox/, the Claude Code memory index); never on CI
 *   --fix    run scripts/brain-normalize-frontmatter.mjs --write first, when that script exists
 *   --quiet  print only the one-line summary
 *   --out    report path (default brain/audits/janitor-latest.md)
 *
 * Checks (brain): broken wikilinks, ambiguous bare links, orphans, content pages missing
 * from the brain/README.md index, frontmatter (parent/updated/type/status/domain enums),
 * stale updated: on the content layer, updated: older than the git last-commit date,
 * TBD/TODO markers, wiki pages missing from wiki/README.md, duplicate wiki ingests.
 * Checks (OS): tasks.yaml past-due, cadence.md rows due, skill and agent frontmatter,
 * skill references to scripts/ files that do not exist.
 *
 * The domain enum is derived from the folder names under brain/projects/, plus wiki and meta.
 */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BRAIN = path.join(ROOT, 'brain');
const ARGS = process.argv.slice(2);
const LOCAL = ARGS.includes('--local');
const FIX = ARGS.includes('--fix');
const QUIET = ARGS.includes('--quiet');
const outIdx = ARGS.indexOf('--out');
const OUT = outIdx > -1 && ARGS[outIdx + 1] ? path.resolve(ROOT, ARGS[outIdx + 1]) : path.join(BRAIN, 'audits', 'janitor-latest.md');

// Single-instance lock. Two sessions ending at once can start two janitors; only one may
// run per machine. A lock older than 10 minutes is a crashed run and gets taken over.
const LOCK = path.join(ROOT, 'tmp', '.brain-janitor.lock');
const LOCK_STALE_MS = 10 * 60 * 1000;
function takeLock() {
  fs.mkdirSync(path.dirname(LOCK), { recursive: true });
  try {
    fs.writeFileSync(LOCK, String(process.pid), { flag: 'wx' });
    return true;
  } catch (e) {
    if (e.code !== 'EEXIST') throw e;
    let age = 0;
    try { age = Date.now() - fs.statSync(LOCK).mtimeMs; } catch { return takeLock(); }
    if (age < LOCK_STALE_MS) return false;
    try { fs.unlinkSync(LOCK); } catch { /* another run took it first */ }
    try { fs.writeFileSync(LOCK, String(process.pid), { flag: 'wx' }); return true; } catch { return false; }
  }
}
try {
  if (!takeLock()) {
    if (!QUIET) console.log('brain-janitor: another run holds the lock, skipping.');
    process.exit(0);
  }
} catch { /* tmp/ not writable: run without a lock */ }
process.on('exit', () => {
  try { if (fs.readFileSync(LOCK, 'utf8') === String(process.pid)) fs.unlinkSync(LOCK); } catch { /* already gone */ }
});

const TODAY = new Date();
const todayIso = TODAY.toISOString().slice(0, 10);
const FM_HEAD = ['---', 'type: log', 'status: active', `updated: ${todayIso}`, 'domain: meta', 'parent: "[[audits/README|Audits]]"', 'tags: [janitor, lint]', '---', ''];

// Invariant: always exit 0 and always leave a report. An unexpected throw becomes a
// one-section report naming the error instead of a missing file and a failed hook or CI job.
process.on('uncaughtException', e => {
  try {
    fs.mkdirSync(path.dirname(OUT), { recursive: true });
    fs.writeFileSync(OUT, [...FM_HEAD, `# Brain janitor, ${todayIso} (FAILED)`, '', 'The janitor crashed before finishing its scan. Fix the script, then rerun.', '', '```', String(e && e.stack || e), '```', ''].join('\n'), 'utf8');
  } catch { /* nothing left to do */ }
  console.log('[janitor] crashed: ' + String(e && e.message || e).split('\n')[0]);
  process.exit(0);
});

const STALE_DAYS = 21;
const TYPE_ENUM = new Set(['context', 'project', 'index', 'reference', 'note', 'log', 'tracker', 'artifact']);
const STATUS_ENUM = new Set(['active', 'paused', 'building', 'archived', 'draft', 'template']);
const PROJECTS_DIR = path.join(BRAIN, 'projects');
const PROJECT_SLUGS = (() => {
  try { return fs.readdirSync(PROJECTS_DIR, { withFileTypes: true }).filter(e => e.isDirectory() && !e.name.startsWith('.') && !e.name.startsWith('_')).map(e => e.name); } catch { return []; }
})();
const DOMAIN_ENUM = new Set([...PROJECT_SLUGS, 'wiki', 'meta']);
const ARCHIVE_RE = /(^|\/)archives?(\/|$)/;
// Folders whose pages are records, not navigation targets: excluded from orphan/stale/TBD checks.
const RECORD_RE = /^(audits\/|wiki\/raw\/|templates\/|archives?\/|brainstorms\/|attachments\/)/;
// The content layer: the pages that must stay fresh and be listed in the index.
const CONTENT_RE = /^(README\.md|conventions\.md|context\/[^/]+\.md|decisions\/log\.md|projects\/[^/]+\/CONTEXT\.md|references\/[^/]+\.md)$/;
// Links to Claude Code memory files live outside the vault: reported once as accepted, not broken.
const OUT_OF_VAULT_RE = /^(feedback-|project-|user-|reference-)/;

// ---- helpers ---------------------------------------------------------------
const rel = f => path.relative(BRAIN, f).split(path.sep).join('/');
const daysBetween = (a, b) => Math.round((b - a) / 86400000);
const parseDate = s => { const m = /^(\d{4}-\d{2}-\d{2})/.exec(String(s || '').trim()); return m ? new Date(m[1] + 'T00:00:00Z') : null; };
const todayUtc = new Date(todayIso + 'T00:00:00Z');

function walk(dir, list = []) {
  let entries = [];
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return list; }
  for (const e of entries) {
    if (e.name === 'attachments' || e.name.startsWith('Untitled') || e.name.startsWith('.')) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, list);
    else if (e.name.endsWith('.md')) list.push(full);
  }
  return list;
}

function readPage(f) {
  let raw = fs.readFileSync(f, 'utf8');
  if (raw.charCodeAt(0) === 0xfeff) raw = raw.slice(1);
  const nl = raw.replace(/\r\n/g, '\n');
  const fm = {};
  let body = nl;
  let hasFm = false;
  if (nl.startsWith('---\n')) {
    const end = nl.indexOf('\n---', 3);
    if (end > -1) {
      hasFm = true;
      const fmLines = nl.slice(4, end).split('\n');
      for (let i = 0; i < fmLines.length; i++) {
        const m = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(fmLines[i]);
        if (!m) continue;
        let v = m[2].trim();
        if (/^[>|][-+]?$/.test(v)) {            // YAML block scalar: gather the indented lines
          const parts = [];
          while (i + 1 < fmLines.length && /^\s+\S/.test(fmLines[i + 1])) parts.push(fmLines[++i].trim());
          v = parts.join(' ');
        }
        fm[m[1]] = v.replace(/^["']|["']$/g, '');
      }
      const endNl = nl.indexOf('\n', end + 1);
      body = endNl > -1 ? nl.slice(endNl + 1) : '';
    }
  }
  return { fm, body, hasFm, text: nl };
}

// Wikilinks: [[target]], [[target|alias]], [[target\|alias]], [[target#heading]]
const LINK_RE = /\[\[([^\]\n]+?)\]\]/g;
function linksIn(text) {
  const out = [];
  let m;
  // Prose that mentions wikilinks lives in code spans and fences; those are not links.
  text = text.replace(/```[\s\S]*?```/g, '').replace(/`[^`\n]*`/g, '');
  while ((m = LINK_RE.exec(text))) {
    let t = m[1].replace(/\\\|/g, '|');
    t = t.split('|')[0].split('#')[0].trim();
    if (t) out.push(t);
  }
  return out;
}

const BULK_COMMIT_FILES = 40;   // a commit touching more brain files than this is a migration, not an edit
function gitLastCommitDates() {
  // One git call: newest-first log with names; first sighting of a path in a non-bulk commit is its last edit date.
  const map = new Map();
  try {
    const log = execFileSync('git', ['-c', 'core.quotepath=false', 'log', '--format=%x00%cs', '--name-only', '--', 'brain'],
      { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, windowsHide: true, stdio: ['ignore', 'pipe', 'ignore'] });
    const commits = [];
    let cur = null;
    for (const line of log.split('\n')) {
      if (line.startsWith('\0')) { cur = { date: line.slice(1).trim(), files: [] }; commits.push(cur); continue; }
      const p = line.trim();
      if (p && cur) cur.files.push(p);
    }
    for (const c of commits) {
      if (c.files.length > BULK_COMMIT_FILES) continue;
      for (const p of c.files) if (!map.has(p)) map.set(p, c.date);
    }
  } catch {
    return null;   // not a git repo, or git missing
  }
  return map;
}

// ---- optional fix ----------------------------------------------------------
let fixNote = '';
if (FIX) {
  const normalizer = path.join(ROOT, 'scripts', 'brain-normalize-frontmatter.mjs');
  if (!fs.existsSync(normalizer)) fixNote = 'no scripts/brain-normalize-frontmatter.mjs, --fix skipped';
  else {
    try {
      const outp = execFileSync(process.execPath, [normalizer, '--write'], { cwd: ROOT, encoding: 'utf8', windowsHide: true });
      fixNote = (outp.split('\n')[0] || '').trim();
    } catch (e) {
      fixNote = 'normalize script failed: ' + String(e.message || e).split('\n')[0];
    }
  }
}

// ---- scan brain ------------------------------------------------------------
const files = walk(BRAIN);
const pages = new Map();          // rel -> {fm, body, hasFm, text}
const byBase = new Map();         // basename (no .md) -> [rel]
for (const f of files) {
  const r = rel(f);
  pages.set(r, readPage(f));
  const base = path.posix.basename(r, '.md');
  if (!byBase.has(base)) byBase.set(base, []);
  byBase.get(base).push(r);
}

const findings = {
  broken: [], ambiguous: [], outOfVault: new Set(), orphans: [], unlinkedElsewhere: [], notInIndex: [], wikiNotInIndex: [],
  fmMissing: [], fmEnum: [], stale: [], drift: [], markers: [], dupIngest: [],
  tasks: [], cadence: [], skills: [], agents: [], local: [],
};

const inbound = new Map();        // rel -> Set(source rel)
const indexTargets = new Set();
const wikiIndexTargets = new Set();

function resolve(target) {
  // Path form ("projects/acme/CONTEXT") or bare basename ("priorities").
  // Bare basenames resolve like Obsidian: the shortest path wins; a tie is ambiguous.
  if (target.includes('/')) {
    const r = target.endsWith('.md') ? target : target + '.md';
    return pages.has(r) ? [r] : [];
  }
  const hits = byBase.get(target.replace(/\.md$/, '')) || [];
  if (hits.length < 2) return hits;
  const depth = r => r.split('/').length;
  const min = Math.min(...hits.map(depth));
  return hits.filter(r => depth(r) === min);
}

// Records (audits, raw dumps, brainstorms) and archives are not navigation: their links
// neither count as inbound (for orphans) nor get linted (append-only prose mentions).
const isNavSource = r => !RECORD_RE.test(r) && !ARCHIVE_RE.test(r);

for (const [r, p] of pages) {
  if (!isNavSource(r)) continue;
  const seen = new Set();
  for (const t of linksIn(p.text)) {
    const hits = resolve(t);
    if (hits.length === 0) {
      if (OUT_OF_VAULT_RE.test(t)) { findings.outOfVault.add(t); continue; }
      if (!seen.has(t)) { findings.broken.push(`${r} -> [[${t}]]`); seen.add(t); }
      continue;
    }
    if (hits.length > 1 && !seen.has(t)) { findings.ambiguous.push(`${r} -> [[${t}]] matches ${hits.join(', ')}`); seen.add(t); }
    for (const h of hits) {
      if (h === r) continue;
      if (!inbound.has(h)) inbound.set(h, new Set());
      inbound.get(h).add(r);
      if (r === 'README.md') indexTargets.add(h);
      if (r === 'wiki/README.md') wikiIndexTargets.add(h);
    }
  }
}

const gitDates = gitLastCommitDates();

for (const [r, p] of pages) {
  const archived = ARCHIVE_RE.test(r);
  const record = RECORD_RE.test(r);
  const isContent = CONTENT_RE.test(r);
  const isWiki = r.startsWith('wiki/') && !r.startsWith('wiki/raw/') && r !== 'wiki/README.md' && r !== 'wiki/log.md';

  // frontmatter (note templates carry {{placeholders}} instead of real values: no enum check there)
  if (r.startsWith('templates/')) continue;
  if (!p.hasFm) { findings.fmMissing.push(`${r}: no frontmatter`); }
  else {
    if (r !== 'README.md' && !p.fm.parent)findings.fmMissing.push(`${r}: no parent:`);
    if (!p.fm.updated && !archived) findings.fmMissing.push(`${r}: no updated:`);
    if (p.fm.type && !TYPE_ENUM.has(p.fm.type)) findings.fmEnum.push(`${r}: type "${p.fm.type}"`);
    if (p.fm.status && !STATUS_ENUM.has(p.fm.status)) findings.fmEnum.push(`${r}: status "${p.fm.status}"`);
    if (p.fm.domain && !DOMAIN_ENUM.has(p.fm.domain)) findings.fmEnum.push(`${r}: domain "${p.fm.domain}" (not a brain/projects/ folder, wiki or meta)`);
    if (archived && p.fm.status && p.fm.status !== 'archived') findings.fmEnum.push(`${r}: archive path but status "${p.fm.status}"`);
    if (p.fm.parent) {
      const t = linksIn('[[' + p.fm.parent.replace(/^\[\[|\]\]$/g, '') + ']]')[0];
      if (t && resolve(t).length === 0) findings.broken.push(`${r} -> parent [[${t}]]`);
    }
  }

  // Orphan scope is the content layer plus the wiki; anything else unlinked is
  // informational ("unlinked elsewhere"), not a defect.
  if (!archived && !record && r !== 'README.md') {
    const ins = inbound.get(r);
    const unlinked = !ins || ins.size === 0;
    if (unlinked && (isContent || isWiki)) findings.orphans.push(r);
    else if (unlinked) findings.unlinkedElsewhere.push(r);
    if (isContent && !indexTargets.has(r)) findings.notInIndex.push(r);
    if (isWiki && !wikiIndexTargets.has(r)) findings.wikiNotInIndex.push(r);
  }

  // stale + drift
  const upd = parseDate(p.fm.updated);
  if (isContent && upd && p.fm.status !== 'template') {
    const age = daysBetween(upd, todayUtc);
    if (age > STALE_DAYS) findings.stale.push({ r, age });
  }
  if (!archived && !record && upd && gitDates) {
    const g = gitDates.get('brain/' + r);
    const gd = parseDate(g);
    if (gd && daysBetween(upd, gd) > 0) findings.drift.push({ r, updated: p.fm.updated, git: g, days: daysBetween(upd, gd) });
  }

  // markers
  if (isContent) {
    p.body.split('\n').forEach((line, i) => {
      if (/_TBD_|\bTBD\b|\bTODO\b|\(date TBD\)|open question/i.test(line)) findings.markers.push(`${r}:${i + 1}: ${line.trim().slice(0, 100)}`);
    });
  }
}

// duplicate wiki ingests: the same source: URL on two source pages or two raw pages
const bySource = new Map();
for (const [r, p] of pages) {
  if (!(r.startsWith('wiki/sources/') || r.startsWith('wiki/raw/'))) continue;
  const s = (p.fm.source || '').replace(/[?&]si=[^&\s]+/, '').replace(/\/$/, '');
  if (!s) continue;
  const key = (r.startsWith('wiki/raw/') ? 'raw:' : 'src:') + s;
  if (!bySource.has(key)) bySource.set(key, []);
  bySource.get(key).push(r);
}
for (const [k, rs] of bySource) if (rs.length > 1) findings.dupIngest.push(`${k.slice(4)}: ${rs.join(', ')}`);

// ---- scan OS ---------------------------------------------------------------
const tasksPath = path.join(ROOT, 'tasks.yaml');
if (fs.existsSync(tasksPath)) {
  try {
    const y = fs.readFileSync(tasksPath, 'utf8').replace(/\r\n/g, '\n');
    let cur = null;
    const clean = v => v.replace(/\s+#.*$/, '').trim().replace(/^["']|["']$/g, '');
    const flush = () => {
      if (!cur || !cur.title || !cur.deadline || cur.status === 'done') return;
      const d = parseDate(cur.deadline);
      if (d && daysBetween(d, todayUtc) > 0) findings.tasks.push(`${cur.title}: ${cur.status || 'todo'} ${cur.progress ?? '?'}%, deadline ${cur.deadline} (${daysBetween(d, todayUtc)}d ago)${cur.example === 'true' ? ' [example task]' : ''}`);
    };
    for (const line of y.split('\n')) {
      if (/^\s*#/.test(line) || !line.trim()) continue;
      const m = /^-\s+(\w+):\s*(.*)$/.exec(line);
      if (m) { flush(); cur = { [m[1]]: clean(m[2]) }; continue; }
      const kv = /^\s+(\w+):\s*(.*)$/.exec(line);
      if (kv && cur) cur[kv[1]] = clean(kv[2]);
    }
    flush();
  } catch { findings.tasks.push('tasks.yaml unreadable'); }
}

const cadencePath = path.join(ROOT, 'cadence.md');
if (fs.existsSync(cadencePath)) {
  try {
    const c = fs.readFileSync(cadencePath, 'utf8').replace(/\r\n/g, '\n');
    let col = null;   // column indexes, found from the header row
    for (const line of c.split('\n')) {
      if (!line.trim().startsWith('|')) { col = null; continue; }
      const cells = line.split('|').map(s => s.trim());
      if (/^\|\s*:?-/.test(line.trim())) continue;
      const lower = cells.map(s => s.toLowerCase().replace(/[_*`]/g, ' ').replace(/\s+/g, ' ').trim());
      if (lower.includes('item') && lower.some(s => s === 'next due')) {
        col = { item: lower.indexOf('item'), last: lower.indexOf('last run'), due: lower.indexOf('next due') };
        continue;
      }
      if (!col) continue;
      const item = (cells[col.item] || '').replace(/\*/g, '');
      if (!item) continue;
      const dueRaw = (cells[col.due] || '').replace(/\*/g, '');
      const lastRaw = col.last > -1 ? (cells[col.last] || '') : '';
      const d = parseDate(dueRaw);
      if (d) {
        const late = daysBetween(d, todayUtc);
        if (late >= 0) findings.cadence.push(`${item}: due ${d.toISOString().slice(0, 10)}${late > 0 ? ` (${late}d overdue)` : ' (today)'}`);
      } else if (!dueRaw.trim() && !parseDate(lastRaw)) {
        findings.cadence.push(`${item}: never run (no last run, no next due)`);
      }
    }
  } catch { findings.cadence.push('cadence.md unreadable'); }
}

const skillsDir = path.join(ROOT, '.claude', 'skills');
let skillCount = 0;
if (fs.existsSync(skillsDir)) {
  for (const e of fs.readdirSync(skillsDir, { withFileTypes: true })) {
    if (!e.isDirectory()) continue;
    const sk = path.join(skillsDir, e.name, 'SKILL.md');
    if (!fs.existsSync(sk)) { findings.skills.push(`${e.name}: no SKILL.md`); continue; }
    skillCount++;
    const p = readPage(sk);
    if (!p.hasFm || !p.fm.name) findings.skills.push(`${e.name}: missing name: in frontmatter`);
    if (!p.hasFm || !p.fm.description) findings.skills.push(`${e.name}: missing description: in frontmatter`);
    else if (p.fm.description.length < 40) findings.skills.push(`${e.name}: description too short to route on (${p.fm.description.length} chars)`);
    if (p.fm.name && p.fm.name !== e.name) findings.skills.push(`${e.name}: name "${p.fm.name}" differs from folder`);
    const refs = new Set();
    let m; const re = /`(scripts\/[\w./-]+\.\w{1,5})`/g;   // files only, not folders
    while ((m = re.exec(p.text))) refs.add(m[1]);
    for (const ref of refs) {
      const inSkill = path.join(skillsDir, e.name, ...ref.split('/'));
      const inRoot = path.join(ROOT, ...ref.split('/'));
      if (!fs.existsSync(inSkill) && !fs.existsSync(inRoot)) findings.skills.push(`${e.name}: references \`${ref}\`, which exists neither under the skill nor at the repo root`);
    }
  }
}
const agentsDir = path.join(ROOT, '.claude', 'agents');
if (fs.existsSync(agentsDir)) {
  for (const f of fs.readdirSync(agentsDir)) {
    if (!f.endsWith('.md')) continue;
    const p = readPage(path.join(agentsDir, f));
    if (!p.hasFm || !p.fm.name || !p.fm.description) findings.agents.push(`${f}: missing name/description frontmatter`);
  }
}

// ---- local-only checks -----------------------------------------------------
if (LOCAL) {
  const listDir = (dir, filter) => { try { return fs.readdirSync(dir).filter(filter); } catch { return null; } };
  const inboxFiles = listDir(path.join(ROOT, 'inbox'), x => x !== 'README.md' && !x.startsWith('.'));
  if (inboxFiles && inboxFiles.length) findings.local.push(`inbox/ holds ${inboxFiles.length} file(s): ${inboxFiles.slice(0, 8).join(', ')}${inboxFiles.length > 8 ? ', ...' : ''}`);
  // Claude Code keeps this project's memory under ~/.claude/projects/<root path with every
  // non-alphanumeric character replaced by "-">/memory. The drive letter case varies on Windows.
  try {
    const home = process.env.USERPROFILE || process.env.HOME || '';
    const slug = ROOT.replace(/[^A-Za-z0-9]/g, '-');
    const candidates = [slug, slug.charAt(0).toLowerCase() + slug.slice(1), slug.charAt(0).toUpperCase() + slug.slice(1)];
    const memDir = candidates.map(s => path.join(home, '.claude', 'projects', s, 'memory')).find(d => fs.existsSync(path.join(d, 'MEMORY.md')));
    if (memDir) {
      const idx = fs.readFileSync(path.join(memDir, 'MEMORY.md'), 'utf8');
      const listed = new Set([...idx.matchAll(/\]\(([\w.-]+\.md)\)/g)].map(m => m[1]));
      const onDisk = fs.readdirSync(memDir).filter(x => x.endsWith('.md') && x !== 'MEMORY.md');
      for (const f of onDisk) if (!listed.has(f)) findings.local.push(`memory file not in MEMORY.md index: ${f}`);
      for (const f of listed) if (!onDisk.includes(f)) findings.local.push(`MEMORY.md lists a missing file: ${f}`);
    }
  } catch { /* no memory store on this machine */ }
}

// ---- report ----------------------------------------------------------------
findings.stale.sort((a, b) => b.age - a.age);
findings.drift.sort((a, b) => b.days - a.days);
const counts = {
  broken: findings.broken.length, ambiguous: findings.ambiguous.length, orphans: findings.orphans.length,
  notInIndex: findings.notInIndex.length, wikiNotInIndex: findings.wikiNotInIndex.length,
  fmMissing: findings.fmMissing.length, fmEnum: findings.fmEnum.length, stale: findings.stale.length,
  drift: findings.drift.length, markers: findings.markers.length, dupIngest: findings.dupIngest.length,
  tasks: findings.tasks.length, cadence: findings.cadence.length, skills: findings.skills.length, agents: findings.agents.length,
  local: findings.local.length,
};
const defects = counts.broken + counts.ambiguous + counts.orphans + counts.notInIndex + counts.wikiNotInIndex + counts.fmMissing + counts.fmEnum + counts.drift + counts.dupIngest + counts.skills + counts.agents;
const list = (arr, cap = 40) => arr.length ? arr.slice(0, cap).map(x => `- ${x}`).join('\n') + (arr.length > cap ? `\n- ... ${arr.length - cap} more` : '') : '- none';

const lines = [...FM_HEAD];
lines.push(`# Brain janitor, ${todayIso}`, '');
lines.push(`Deterministic lint by \`scripts/brain-janitor.mjs\` (${LOCAL ? 'local run' : 'repo-only run'}${FIX ? ', with --fix' : ''}). Overwritten on every run; \`/audit\` quotes these counts instead of re-deriving them. Scope: ${pages.size} brain pages, ${PROJECT_SLUGS.length} projects, ${skillCount} skills.${gitDates ? '' : ' Git history unavailable, drift check skipped.'}${fixNote ? ` Normalize: ${fixNote}.` : ''}`, '');
lines.push('## Summary', '', '| Check | Count |', '|---|---|');
for (const [k, v] of Object.entries(counts)) lines.push(`| ${k} | ${v} |`);
lines.push(`| **structural defects** (broken + ambiguous + orphans + index gaps + frontmatter + drift + dup ingests + skill/agent frontmatter) | **${defects}** |`, '');
lines.push('## Broken wikilinks', '', list(findings.broken), '');
if (findings.outOfVault.size) lines.push(`_Out-of-vault memory links (accepted, ${findings.outOfVault.size}): ${[...findings.outOfVault].slice(0, 12).join(', ')}${findings.outOfVault.size > 12 ? ', ...' : ''}_`, '');
lines.push('## Ambiguous bare links (two files share the basename)', '', list(findings.ambiguous), '');
lines.push('## Orphans (content layer and wiki pages with no inbound link from a navigation page)', '', list(findings.orphans, 60), '');
lines.push(`_Unlinked pages elsewhere in the brain (informational, ${findings.unlinkedElsewhere.length}): ${findings.unlinkedElsewhere.slice(0, 10).join(', ') || 'none'}${findings.unlinkedElsewhere.length > 10 ? ', ...' : ''}_`, '');
lines.push('## Content pages missing from the brain/README.md index', '', list(findings.notInIndex), '');
lines.push('## Wiki pages missing from the wiki/README.md index', '', list(findings.wikiNotInIndex), '');
lines.push('## Frontmatter missing (parent / updated / none)', '', list(findings.fmMissing), '');
lines.push('## Frontmatter enum violations', '', list(findings.fmEnum), '');
lines.push(`## Stale content pages (updated: more than ${STALE_DAYS} days ago, oldest first)`, '', list(findings.stale.map(s => `${s.r} (${s.age}d)`)), '');
lines.push('## Frontmatter drift (updated: older than the git last commit)', '', list(findings.drift.map(d => `${d.r}: updated ${d.updated}, last commit ${d.git} (${d.days}d)`), 30), '');
lines.push('## Open / TBD markers (content layer)', '', list(findings.markers), '');
lines.push('## Duplicate wiki ingests (same source URL)', '', list(findings.dupIngest), '');
lines.push('## OS: tasks.yaml past deadline, not done', '', list(findings.tasks), '');
lines.push('## OS: cadence rows due today, overdue or never run', '', list(findings.cadence), '');
lines.push('## OS: skill frontmatter and script references', '', list(findings.skills), '');
lines.push('## OS: agent frontmatter', '', list(findings.agents), '');
if (LOCAL) lines.push('## Local only (inbox, memory index)', '', list(findings.local), '');
lines.push('_Judgment checks (missing pages for recurring entities, contradictions between pages) are not scripted; `/audit` still does those._', '');

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, lines.join('\n'), 'utf8');

const summary = `[janitor] ${defects} structural defects, ${counts.stale} stale, ${counts.markers} markers, ${counts.tasks} past-due tasks, ${counts.cadence} cadence rows due${LOCAL ? `, ${counts.local} local` : ''} -> ${path.relative(ROOT, OUT).split(path.sep).join('/')}`;
console.log(summary);
if (!QUIET) {
  const show = (title, arr, cap = 8) => { if (arr.length) { console.log(`\n${title} (${arr.length}):`); arr.slice(0, cap).forEach(x => console.log('  - ' + (typeof x === 'string' ? x : x.r))); if (arr.length > cap) console.log(`  ... ${arr.length - cap} more`); } };
  show('Broken links', findings.broken); show('Ambiguous links', findings.ambiguous); show('Orphans', findings.orphans);
  show('Missing from index', findings.notInIndex); show('Wiki missing from index', findings.wikiNotInIndex);
  show('Frontmatter missing', findings.fmMissing); show('Enum violations', findings.fmEnum);
  show('Drift', findings.drift.map(d => `${d.r} (${d.days}d)`)); show('Dup ingests', findings.dupIngest);
  show('Past-due tasks', findings.tasks); show('Cadence due', findings.cadence); show('Skills', findings.skills); show('Agents', findings.agents);
  if (LOCAL) show('Local', findings.local);
}
process.exit(0);
