#!/usr/bin/env node
/**
 * inbox-check.mjs: SessionStart hook.
 *
 * Surfaces any files waiting in inbox/ so they get filed to their real home instead of
 * sitting unnoticed. Whatever this prints is added to the session's opening context.
 * Silent when the inbox is empty or missing. Always exits 0.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const INBOX = path.join(ROOT, 'inbox');

let waiting = [];
try {
  waiting = fs.readdirSync(INBOX, { withFileTypes: true })
    .filter(e => e.name !== 'README.md' && !e.name.startsWith('.'))
    .map(e => e.name + (e.isDirectory() ? '/' : ''));
} catch { process.exit(0); }

if (waiting.length) {
  const shown = waiting.slice(0, 10).join(', ') + (waiting.length > 10 ? `, and ${waiting.length - 10} more` : '');
  console.log(`[inbox] ${waiting.length} item(s) waiting in inbox/: ${shown}. File each one to its real home (routing table in inbox/README.md), then leave the inbox empty.`);
}
process.exit(0);
