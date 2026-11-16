#!/usr/bin/env node
/**
 * metered-guard.mjs: PreToolUse hook (Bash) that hard-blocks commands which spend
 * metered credits or money (paid TTS, image or video generation, paid APIs) unless the
 * command carries an approval flag. Claude may add that flag ONLY after the user said
 * yes to that exact spend in the same conversation.
 *
 * Why: a written rule can be rationalised past under momentum; a hook cannot. Origin: a
 * full paid generation batch ran on the wrong settings without anyone confirming it first.
 *
 * Config lives in .claude/metered.json (see .claude/metered.README.md):
 *   { "approvalFlag": "--user-approved", "patterns": [...], "safeForms": [...] }
 * patterns: case-insensitive substrings, or "/regex/" strings, that mark a paid command.
 * safeForms: "/regex/" or substrings for read-only forms (an estimate, a listing) that are
 *   scrubbed out before matching, so they never trip the block.
 * An empty pattern list, or no config file, allows everything.
 *
 * Exit 2 blocks the call and the stderr text goes back to Claude as the reason.
 * Unparseable payload or config: exit 0 (never block unrelated work on a broken hook).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const CONFIG = path.join(ROOT, '.claude', 'metered.json');

let cfg;
try { cfg = JSON.parse(fs.readFileSync(CONFIG, 'utf8')); } catch { process.exit(0); }
const patterns = Array.isArray(cfg.patterns) ? cfg.patterns.filter(p => typeof p === 'string' && p.trim()) : [];
if (!patterns.length) process.exit(0);
const safeForms = Array.isArray(cfg.safeForms) ? cfg.safeForms.filter(p => typeof p === 'string' && p.trim()) : [];
const FLAG = typeof cfg.approvalFlag === 'string' && cfg.approvalFlag.trim() ? cfg.approvalFlag.trim() : '--user-approved';

let command = '';
try { command = JSON.parse(fs.readFileSync(0, 'utf8').replace(/^﻿/, ''))?.tool_input?.command || ''; } catch { process.exit(0); }
if (!command) process.exit(0);

const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// "/body/flags" is a regex (always case-insensitive); anything else is a literal substring.
function toRegex(p, global) {
  const m = /^\/(.+)\/([a-z]*)$/s.exec(p);
  try {
    if (m) return new RegExp(m[1], [...new Set((m[2] + 'i' + (global ? 'g' : '')).split(''))].join(''));
  } catch { /* invalid regex: treat it as a literal */ }
  return new RegExp(escapeRe(p), global ? 'gi' : 'i');
}

let scrubbed = command;
for (const s of safeForms) scrubbed = scrubbed.replace(toRegex(s, true), ' metered-readonly ');

const hits = patterns.filter(p => toRegex(p, false).test(scrubbed));
if (!hits.length) process.exit(0);
if (command.toLowerCase().includes(FLAG.toLowerCase())) process.exit(0);

process.stderr.write(
  `BLOCKED: metered-credit command (matched: ${hits.join(', ')}).\n` +
  'This spends real money or credits. Before re-running you MUST, in this order:\n' +
  '1. Read the workstream\'s documented approach (settings, model, known fixes) and the current budget.\n' +
  '2. Tell the user exactly what will be generated (model or voice, item count, estimated cost)\n' +
  '   and get their explicit yes IN THIS CONVERSATION.\n' +
  `3. Re-run the command with ${FLAG} appended as a comment, e.g.:  node tools/generate.mjs  # ${FLAG}\n` +
  'Adding the flag without step 2 is lying to the user. Do not do that.\n'
);
process.exit(2);
