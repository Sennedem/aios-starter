#!/usr/bin/env node
// sweep-root.mjs: SessionEnd hook.
//
// Moves stray media and office files that landed loose in the repo ROOT into inbox/, so the
// router root never collects clutter. The next session's inbox check then files them. A hook
// cannot know which project a file belongs to, so it only quarantines; Claude does the filing.
//
// Scope: the root folder only. Never touches subfolders, markdown, config or dotfiles.
// Always exits 0.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const INBOX = path.join(ROOT, 'inbox');
const EXT = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg', '.heic',
  '.mp4', '.mov', '.webm', '.mkv', '.mp3', '.wav', '.m4a',
  '.pdf', '.pptx', '.ppt', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.zip']);

try {
  const strays = fs.readdirSync(ROOT, { withFileTypes: true })
    .filter(e => e.isFile() && !e.name.startsWith('.') && EXT.has(path.extname(e.name).toLowerCase()));
  if (!strays.length) process.exit(0);
  fs.mkdirSync(INBOX, { recursive: true });
  let moved = 0;
  for (const e of strays) {
    let dest = path.join(INBOX, e.name);
    if (fs.existsSync(dest)) dest = path.join(INBOX, `${Date.now()}-${e.name}`);
    try { fs.renameSync(path.join(ROOT, e.name), dest); moved++; console.log(`[sweep] stray ${e.name} -> inbox/`); } catch { /* leave it */ }
  }
  if (moved) console.log(`[sweep] ${moved} file(s) moved to inbox/. The next session files them.`);
} catch { /* never block a session end */ }
process.exit(0);
