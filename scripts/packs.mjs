#!/usr/bin/env node
// packs.mjs: list or remove opt-in packs (see .claude/packs.json). No dependencies, Node 18+.
//
//   node scripts/packs.mjs list                 every pack with its file count
//   node scripts/packs.mjs files <pack>         the files a pack owns
//   node scripts/packs.mjs remove <pack> [...]  delete the pack's files, their index lines and
//                                               every link to them; record it as removed
//   add --dry to remove to see what would change without changing anything
//
// A brain page belongs to a pack through `pack: <name>` in its frontmatter. Skills, scripts and
// workflows belong through the pack's `paths`. Lines ending in <!-- pack:<name> --> in the
// root markdown files belong to the pack too. Links to removed pages are not left broken:
// list lines that only point at a removed page are dropped, other wikilinks become plain text,
// and `related:` entries are removed.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BRAIN = path.join(ROOT, 'brain');
const CONFIG = path.join(ROOT, '.claude', 'packs.json');
const args = process.argv.slice(2);
const DRY = args.includes('--dry');
const [cmd, ...names] = args.filter(a => a !== '--dry');

const readConfig = () => JSON.parse(fs.readFileSync(CONFIG, 'utf8'));
const relRoot = p => path.relative(ROOT, p).split(path.sep).join('/');
const relBrain = p => path.relative(BRAIN, p).split(path.sep).join('/');

function walk(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (e.name === '.git' || e.name === 'node_modules' || e.name === '.obsidian') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}

const packOf = file => {
  try {
    const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(fs.readFileSync(file, 'utf8'));
    const p = m && /^pack:\s*["']?([\w-]+)["']?\s*$/m.exec(m[1]);
    return p ? p[1] : null;
  } catch { return null; }
};

function filesOf(name, config) {
  const pack = config.packs[name];
  if (!pack) throw new Error(`no pack named "${name}". Run: node scripts/packs.mjs list`);
  const files = new Set();
  for (const f of walk(BRAIN)) if (f.endsWith('.md') && packOf(f) === name) files.add(f);
  for (const p of pack.paths || []) {
    const abs = path.join(ROOT, p);
    if (!fs.existsSync(abs)) continue;
    if (fs.statSync(abs).isDirectory()) walk(abs).forEach(f => files.add(f)); else files.add(abs);
  }
  return [...files].sort();
}

function list() {
  const config = readConfig();
  for (const [name, pack] of Object.entries(config.packs)) {
    const n = filesOf(name, config).length;
    const state = config.removed.includes(name) ? 'removed' : (pack.removable === false ? 'always' : 'kept');
    console.log(`${name.padEnd(11)} ${String(n).padStart(4)} files  ${state.padEnd(7)}  ${pack.what}`);
  }
}

// Rewrite one markdown file so it no longer links to any removed brain page.
function unlink(text, removed) {
  const isRemoved = t => removed.has(t.replace(/\.md$/, '').replace(/^\/+/, ''));
  let changed = false;
  const lines = text.split('\n');
  const out = [];
  let inFm = false;
  let fmDone = false;
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    if (i === 0 && line.trim() === '---') { inFm = true; out.push(line); continue; }
    if (inFm && !fmDone && line.trim() === '---') { fmDone = true; inFm = false; out.push(line); continue; }
    if (inFm) {
      // related: ["[[a]]", "[[b]]"] on one line, or a block list item - "[[a]]"
      if (/^related:\s*\[/.test(line)) {
        const kept = [...line.matchAll(/"?\[\[([^\]|]+)(?:\|[^\]]*)?\]\]"?/g)].filter(m => !isRemoved(m[1])).map(m => `"[[${m[1]}]]"`);
        const next = kept.length ? `related: [${kept.join(', ')}]` : null;
        if (next !== line) changed = true;
        if (next) out.push(next);
        continue;
      }
      const item = /^\s+-\s*"?\[\[([^\]|]+)/.exec(line);
      if (item && isRemoved(item[1])) { changed = true; continue; }
      out.push(line);
      continue;
    }
    const links = [...line.matchAll(/\[\[([^\]|\\]+)(?:\\?\|([^\]]*))?\]\]/g)];
    const dead = links.filter(m => isRemoved(m[1]));
    if (!dead.length) { out.push(line); continue; }
    changed = true;
    // A list item or table row that leads with a removed page (an index line), or whose links all
    // point at removed pages, is dropped whole.
    if (/^\s*([-*]|\d+\.|\|)/.test(line) && (isRemoved(links[0][1]) || dead.length === links.length)) continue;
    for (const m of dead) {
      const label = m[2] || m[1].split('/').pop().replace(/-/g, ' ');
      line = line.replace(m[0], label);
    }
    out.push(line);
  }
  return changed ? out.join('\n') : null;
}

function remove(packNames) {
  const config = readConfig();
  for (const n of packNames) {
    if (!config.packs[n]) throw new Error(`no pack named "${n}"`);
    if (config.packs[n].removable === false) throw new Error(`the ${n} pack is not removable`);
  }
  const doomed = new Set();
  for (const n of packNames) filesOf(n, config).forEach(f => doomed.add(f));
  const removedTargets = new Set([...doomed].filter(f => f.startsWith(BRAIN + path.sep) && f.endsWith('.md')).map(f => relBrain(f).replace(/\.md$/, '')));

  // Files that may link to removed pages or carry pack-marked lines.
  const candidates = [
    ...walk(BRAIN).filter(f => f.endsWith('.md')),
    ...['CLAUDE.md', 'README.md', 'connections.md', 'cadence.md', '.env.example'].map(f => path.join(ROOT, f)),
    ...walk(path.join(ROOT, '.claude')).filter(f => f.endsWith('.md')),
    ...walk(path.join(ROOT, 'docs')).filter(f => f.endsWith('.md')),
  ].filter(f => !doomed.has(f) && fs.existsSync(f));

  const edits = [];
  for (const f of candidates) {
    let text = fs.readFileSync(f, 'utf8');
    let changed = false;
    // Single lines ending in <!-- pack:NAME -->, and blocks between ">>> pack:NAME" and "<<< pack:NAME".
    const marked = [];
    let inBlock = null;
    for (const l of text.split('\n')) {
      if (inBlock) { if (l.includes(`<<< pack:${inBlock}`)) inBlock = null; continue; }
      const opener = packNames.find(n => l.includes(`>>> pack:${n}`));
      if (opener) { inBlock = opener; continue; }
      if (packNames.some(n => l.includes(`<!-- pack:${n} -->`))) continue;
      marked.push(l);
    }
    if (marked.length !== text.split('\n').length) { text = marked.join('\n'); changed = true; }
    if (f.startsWith(BRAIN + path.sep)) {
      const next = unlink(text, removedTargets);
      if (next !== null) { text = next; changed = true; }
    }
    if (changed) edits.push([f, text]);
  }

  console.log(`${DRY ? '[dry] would remove' : 'Removing'} ${packNames.join(', ')}: ${doomed.size} files deleted, ${edits.length} files edited.`);
  for (const f of doomed) console.log(`  delete ${relRoot(f)}`);
  for (const [f] of edits) console.log(`  edit   ${relRoot(f)}`);
  if (DRY) return;

  for (const f of doomed) fs.rmSync(f, { force: true });
  // Remove directories the pack's paths left empty.
  for (const n of packNames) for (const p of config.packs[n].paths || []) {
    const abs = path.join(ROOT, p);
    if (fs.existsSync(abs) && fs.statSync(abs).isDirectory()) fs.rmSync(abs, { recursive: true, force: true });
  }
  for (const [f, text] of edits) fs.writeFileSync(f, text, 'utf8');
  config.removed = [...new Set([...config.removed, ...packNames])];
  fs.writeFileSync(CONFIG, JSON.stringify(config, null, 2) + '\n', 'utf8');
  console.log('Done. Run: node scripts/brain-janitor.mjs --local   (expect 0 broken links)');
}

try {
  if (cmd === 'list') list();
  else if (cmd === 'files' && names[0]) filesOf(names[0], readConfig()).forEach(f => console.log(relRoot(f)));
  else if (cmd === 'remove' && names.length) remove(names);
  else { console.log('usage: node scripts/packs.mjs list | files <pack> | remove <pack> [...] [--dry]'); process.exit(1); }
} catch (e) {
  console.error(String(e.message || e));
  process.exit(1);
}
