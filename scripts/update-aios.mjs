#!/usr/bin/env node
// update-aios.mjs: bring improvements from the public starter into this copy, safely.
// The /update-aios skill runs it; it can also be run by hand. No dependencies, Node 18+, needs git.
//
//   node scripts/update-aios.mjs --plan            fetch upstream and print what would change
//   node scripts/update-aios.mjs --plan --json     the same plan as JSON
//   node scripts/update-aios.mjs --apply           apply every new, update, merge and retire item
//   node scripts/update-aios.mjs --apply --only <path> [<path> ...]   apply only those paths
//
// Rules it enforces (the skill explains them to the user):
// - Reads only from the `upstream` remote (the starter), fetch-only. It never pushes anywhere.
// - Never touches what the user owns: brain content they wrote, connections.md, cadence.md,
//   otherworlds notes, voice files, any references/learnings.md, skill state, .env.
// - Never brings back a pack the user removed (.claude/packs.json "removed").
// - A shipped file the user never edited is replaced. A file they edited gets a three-way
//   merge; a merge with conflicts is never written over their file: the merged text with
//   conflict markers goes to tmp/update-aios/ for the user to look at.
// - Records the upstream commit it synced to in .aios-upstream, the base for the next run.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const UPSTREAM_URL = process.env.AIOS_UPSTREAM_URL || 'https://github.com/Sennedem/aios-starter.git'; // the env override is for testing
const BASE_FILE = path.join(ROOT, '.aios-upstream');
const MERGE_DIR = path.join(ROOT, 'tmp', 'update-aios');
const args = process.argv.slice(2);
const JSON_OUT = args.includes('--json');
const onlyIdx = args.indexOf('--only');
const ONLY = onlyIdx >= 0 ? new Set(args.slice(onlyIdx + 1).map(p => p.replace(/\\/g, '/'))) : null;

function git(gitArgs, opts = {}) {
  const r = spawnSync('git', gitArgs, { cwd: ROOT, encoding: opts.encoding ?? 'utf8', windowsHide: true, maxBuffer: 64 * 1024 * 1024, input: opts.input });
  if (opts.allowFail) return r;
  if (r.status !== 0) throw new Error(`git ${gitArgs.join(' ')} failed: ${(r.stderr || '').toString().trim()}`);
  return opts.encoding === 'buffer' ? r.stdout : r.stdout.trim();
}

// What an update may touch, and what it never touches.
const IN_SCOPE = [
  /^\.claude\/(skills|rules|agents)\//, /^\.claude\/(settings\.json|metered\.README\.md|packs\.json)$/,
  /^scripts\//, /^\.github\/workflows\//, /^docs\//,
  /^brain\/wiki\/(concepts|techniques|tools|sources)\//, /^brain\/wiki\/README\.md$/,
  /^brain\/references\/(?!README\.md$)/, /^brain\/templates\//, /^brain\/conventions\.md$/, /^brain\/README\.md$/,
  /^(CLAUDE|README|AGENTS)\.md$/, /^(LICENSE|THIRD-PARTY-NOTICES\.md|\.gitignore|\.gitattributes|\.env\.example)$/,
  /^otherworlds\/(_template|README)\.md$/, /^inbox\/README\.md$/,
];
const NEVER = [
  /(^|\/)references\/learnings\.md$/, /^\.claude\/skills\/writing\/references\/(voice-samples|ban_list)\.md$/,
  /^\.claude\/skills\/[^/]+\/state\.json$/, /^\.claude\/skills\/inbox-janitor\/references\/(run-log|sender-map)\.md$/,
  /^\.env$/, /^brain\/wiki\/raw\//,
];
const inScope = p => IN_SCOPE.some(r => r.test(p)) && !NEVER.some(r => r.test(p));

function ensureUpstream() {
  const remotes = git(['remote']).split(/\s+/);
  if (!remotes.includes('upstream')) {
    git(['remote', 'add', 'upstream', UPSTREAM_URL]);
    git(['remote', 'set-url', '--push', 'upstream', 'DISABLED-fetch-only']);
  }
  git(['fetch', '--quiet', 'upstream']);
  const head = git(['symbolic-ref', '--short', 'refs/remotes/upstream/HEAD'], { allowFail: true });
  const ref = head.status === 0 ? head.stdout.trim() : (git(['rev-parse', '--verify', '--quiet', 'upstream/main'], { allowFail: true }).status === 0 ? 'upstream/main' : 'upstream/master');
  return ref;
}

const blobAt = (commit, p) => {
  const r = git(['rev-parse', '--verify', '--quiet', `${commit}:${p}`], { allowFail: true });
  return r.status === 0 ? r.stdout.trim() : null;
};
const localBlob = p => {
  const abs = path.join(ROOT, p);
  if (!fs.existsSync(abs)) return null;
  return git(['hash-object', '--', p]);
};
const historyBlobs = (ref, p) => {
  const commits = git(['rev-list', ref, '--', p]).split('\n').filter(Boolean);
  return new Set(commits.map(c => blobAt(c, p)).filter(Boolean));
};
const readBlob = sha => git(['cat-file', 'blob', sha], { encoding: 'buffer' });

function packOfText(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  const p = m && /^pack:\s*["']?([\w-]+)["']?\s*$/m.exec(m[1]);
  return p ? p[1] : null;
}

function plan() {
  const ref = ensureUpstream();
  const tip = git(['rev-parse', ref]);
  let base = fs.existsSync(BASE_FILE) ? fs.readFileSync(BASE_FILE, 'utf8').trim() : '';
  if (base && git(['cat-file', '-e', `${base}^{commit}`], { allowFail: true }).status !== 0) base = '';
  if (!base) {
    const mb = git(['merge-base', 'HEAD', ref], { allowFail: true });
    base = mb.status === 0 ? mb.stdout.trim() : '';
  }

  let packs = { removed: [], packs: {} };
  try { packs = JSON.parse(fs.readFileSync(path.join(ROOT, '.claude', 'packs.json'), 'utf8')); } catch { /* none */ }
  const removedPaths = packs.removed.flatMap(n => (packs.packs[n]?.paths || []));
  const inRemovedPack = (p, text) => removedPaths.some(rp => p === rp || p.startsWith(rp.replace(/\/?$/, '/')))
    || (text && packs.removed.includes(packOfText(text)));

  const upstreamFiles = git(['ls-tree', '-r', '--name-only', tip]).split('\n').filter(Boolean).filter(inScope);
  const items = [];
  for (const p of upstreamFiles) {
    const theirs = blobAt(tip, p);
    const theirsText = p.endsWith('.md') ? readBlob(theirs).toString('utf8') : null;
    if (inRemovedPack(p, theirsText)) { items.push({ path: p, action: 'skip', why: 'pack you removed' }); continue; }
    const mine = localBlob(p);
    const baseBlob = base ? blobAt(base, p) : null;
    if (mine === theirs) continue;
    if (!mine) {
      if (baseBlob) items.push({ path: p, action: 'skip', why: 'you deleted it' });
      else items.push({ path: p, action: 'new', theirs });
      continue;
    }
    if (baseBlob === theirs) continue; // upstream did not change it since your last sync: yours stands
    const shipped = historyBlobs(tip, p);
    if (shipped.has(mine)) { items.push({ path: p, action: 'update', theirs }); continue; }
    items.push({ path: p, action: 'merge', theirs, base: baseBlob });
  }
  // Files upstream retired since your last sync, that you never edited.
  if (base) {
    const baseFiles = git(['ls-tree', '-r', '--name-only', base]).split('\n').filter(Boolean).filter(inScope);
    const tipSet = new Set(upstreamFiles);
    for (const p of baseFiles) {
      if (tipSet.has(p)) continue;
      const mine = localBlob(p);
      if (!mine) continue;
      if (mine === blobAt(base, p)) items.push({ path: p, action: 'retire' });
      else items.push({ path: p, action: 'skip', why: 'retired upstream, but you edited it: kept' });
    }
  }
  return { ref, tip, base, items };
}

function apply(p) {
  fs.mkdirSync(MERGE_DIR, { recursive: true });
  const done = [], conflicts = [];
  for (const it of p.items) {
    if (it.action === 'skip') continue;
    if (ONLY && !ONLY.has(it.path)) continue;
    const abs = path.join(ROOT, it.path);
    if (it.action === 'retire') { fs.rmSync(abs, { force: true }); done.push(it); continue; }
    const theirs = readBlob(it.theirs);
    if (it.action === 'new' || it.action === 'update') {
      fs.mkdirSync(path.dirname(abs), { recursive: true });
      fs.writeFileSync(abs, theirs);
      done.push(it);
      continue;
    }
    // merge: three-way when a base exists, otherwise a conflict for the user to settle
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'aios-merge-'));
    const fBase = path.join(tmp, 'base'), fTheirs = path.join(tmp, 'theirs');
    fs.writeFileSync(fBase, it.base ? readBlob(it.base) : '');
    fs.writeFileSync(fTheirs, theirs);
    const r = spawnSync('git', ['merge-file', '-p', '-L', 'yours', '-L', 'last sync', '-L', 'starter', abs, fBase, fTheirs], { cwd: ROOT, encoding: 'buffer', windowsHide: true });
    fs.rmSync(tmp, { recursive: true, force: true });
    if (r.status === 0 && it.base) { fs.writeFileSync(abs, r.stdout); done.push(it); continue; }
    const out = path.join(MERGE_DIR, it.path);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, r.stdout);
    conflicts.push({ ...it, mergedAt: path.relative(ROOT, out).split(path.sep).join('/') });
  }
  if (!ONLY && !conflicts.length) fs.writeFileSync(BASE_FILE, p.tip + '\n');
  return { done, conflicts };
}

try {
  const p = plan();
  if (args.includes('--apply')) {
    const r = apply(p);
    console.log(`Applied ${r.done.length} change(s) from ${p.ref} (${p.tip.slice(0, 7)}).`);
    for (const it of r.done) console.log(`  ${it.action.padEnd(7)} ${it.path}`);
    if (r.conflicts.length) {
      console.log(`\n${r.conflicts.length} file(s) need you: your version and the starter's both changed the same lines. Your file is untouched; the merged text with conflict markers is here:`);
      for (const c of r.conflicts) console.log(`  ${c.path}  ->  ${c.mergedAt}`);
      console.log('\n.aios-upstream not advanced until these are settled. Rerun --apply after.');
    } else if (!ONLY) console.log(`\nSynced to ${p.tip.slice(0, 7)} (.aios-upstream).`);
  } else if (JSON_OUT) {
    console.log(JSON.stringify(p, null, 2));
  } else {
    const groups = { new: [], update: [], merge: [], retire: [], skip: [] };
    for (const it of p.items) groups[it.action].push(it);
    console.log(`Starter: ${p.ref} at ${p.tip.slice(0, 7)}. Last sync: ${p.base ? p.base.slice(0, 7) : 'unknown (first run)'}.`);
    const label = { new: 'New from the starter', update: 'Updated in the starter, unchanged by you: replaced', merge: 'Changed on both sides: three-way merge', retire: 'Retired by the starter, unchanged by you: deleted', skip: 'Left alone' };
    for (const [k, list] of Object.entries(groups)) {
      if (!list.length) continue;
      console.log(`\n${label[k]} (${list.length})`);
      for (const it of list) console.log(`  ${it.path}${it.why ? `  (${it.why})` : ''}`);
    }
    if (!p.items.some(i => i.action !== 'skip')) console.log('\nNothing to update. You are on the latest starter.');
  }
} catch (e) {
  console.error(`[update-aios] ${e.message}`);
  process.exit(1);
}
