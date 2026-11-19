#!/usr/bin/env node
/**
 * inbox-check.mjs: SessionStart hook.
 *
 * There can be two inboxes: `inbox/` in this repo, and a cloud-drive folder for phone drops
 * (set up by /setup step 4). The cloud one is named in the frontmatter of a note in
 * otherworlds/ as `inbox: <absolute path>` (more than one note may name one).
 * This hook lists what is waiting in each, so files get filed instead of sitting unnoticed.
 * Whatever it prints is added to the session's opening context. Silent when every inbox is
 * empty or missing. Always exits 0.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

const inboxes = [{ label: 'inbox/', dir: path.join(ROOT, 'inbox') }];
try {
  const ow = path.join(ROOT, 'otherworlds');
  for (const f of fs.readdirSync(ow)) {
    if (!f.endsWith('.md') || f.startsWith('_')) continue;
    const text = fs.readFileSync(path.join(ow, f), 'utf8');
    const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
    if (!fm) continue;
    for (const m of fm[1].matchAll(/^inbox:\s*["']?(.+?)["']?\s*$/gm)) {
      const dir = m[1].replace(/^~(?=$|[\/])/, process.env.HOME || process.env.USERPROFILE || '~');
      if (!inboxes.some(i => path.resolve(i.dir) === path.resolve(dir))) inboxes.push({ label: dir, dir });
    }
  }
} catch { /* no otherworlds notes: only the repo inbox */ }

const out = [];
for (const { label, dir } of inboxes) {
  let waiting;
  try {
    waiting = fs.readdirSync(dir, { withFileTypes: true })
      .filter(e => e.name !== 'README.md' && !e.name.startsWith('.') && e.name !== 'desktop.ini')
      .map(e => e.name + (e.isDirectory() ? '/' : ''));
  } catch {
    if (label !== 'inbox/') out.push(`[inbox] cloud inbox not reachable: ${dir}. Check the drive app is running and signed in.`);
    continue;
  }
  if (waiting.length) {
    const shown = waiting.slice(0, 10).join(', ') + (waiting.length > 10 ? `, and ${waiting.length - 10} more` : '');
    out.push(`[inbox] ${waiting.length} item(s) waiting in ${label}: ${shown}.`);
  }
}
if (out.length) {
  out.push('[inbox] File each item to its real home (routing in inbox/README.md), then leave every inbox empty. There are ' + inboxes.length + ' inbox(es); check all of them before saying a file is not there.');
  console.log(out.join('\n'));
}
process.exit(0);
