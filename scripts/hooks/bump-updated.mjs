#!/usr/bin/env node
/**
 * bump-updated.mjs: PostToolUse hook (Edit|Write) that keeps `updated:` honest.
 *
 * Why: frontmatter drift (a page edited, its `updated:` date left behind) kept coming
 * back no matter how often the rule was restated, so it moved into tooling.
 * When Claude edits or writes a markdown page under brain/, this sets its `updated:`
 * line to today's local date. It never adds frontmatter, never touches archive folders,
 * raw wiki dumps or the janitor report, and never fails the tool call (always exit 0,
 * no output). Reads the hook payload from stdin: { tool_input: { file_path } }.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const BRAIN = path.join(ROOT, 'brain');
const SKIP_RE = /(^|\/)(archives?|wiki\/raw|audits\/janitor-latest\.md)(\/|$)/;

let payload = '';
try { payload = fs.readFileSync(0, 'utf8'); } catch { process.exit(0); }
let fp = '';
try { fp = JSON.parse(payload.replace(/^﻿/, ''))?.tool_input?.file_path || ''; } catch { process.exit(0); }
if (!fp) process.exit(0);

const abs = path.resolve(ROOT, fp);
const relBrain = path.relative(BRAIN, abs).split(path.sep).join('/');
if (!relBrain || relBrain.startsWith('..') || path.isAbsolute(relBrain) || !abs.endsWith('.md')) process.exit(0);
if (SKIP_RE.test(relBrain)) process.exit(0);
if (!fs.existsSync(abs)) process.exit(0);

const d = new Date();
const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

try {
  // Splice only the date token, in place, on the original bytes: BOM, CRLF/LF mix, quotes
  // and trailing comments on the line all survive untouched.
  const raw = fs.readFileSync(abs, 'utf8');
  const start = raw.charCodeAt(0) === 0xfeff ? 1 : 0;
  if (!raw.startsWith('---', start)) process.exit(0);
  const fmEnd = raw.indexOf('\n---', start + 3);
  if (fmEnd < 0) process.exit(0);
  const fm = raw.slice(start, fmEnd);
  const m = /^(updated:[ \t]*)(["']?)(\d{4}-\d{2}-\d{2})/m.exec(fm);
  if (!m || m[3] === today) process.exit(0);
  const at = start + m.index + m[1].length + m[2].length;
  const out = raw.slice(0, at) + today + raw.slice(at + m[3].length);
  fs.writeFileSync(abs, out, 'utf8');
} catch { /* never block the tool call */ }
process.exit(0);
