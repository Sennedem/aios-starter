#!/usr/bin/env node
// collision-guard.mjs: stop two Claude Code windows from silently editing the same file.
// The idea is written up in brain/wiki/techniques/mod-collision-guard.md.
//
//   node collision-guard.mjs record   PostToolUse Edit|Write: note {file -> session, time} in the ledger
//   node collision-guard.mjs check    PreToolUse  Edit|Write: if ANOTHER session touched the file in the
//                                     last WINDOW_MIN minutes, return permissionDecision "ask" with the reason
//
// The ledger is tmp/edit-ledger.json (gitignored tmp/). Subagents share their parent's session_id,
// so a session never blocks its own agents. Fails open: any error lets the tool call through.
import fs from 'node:fs';
import path from 'node:path';

const WINDOW_MIN = 30;
const KEEP_MIN = 180;
const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const ledgerPath = path.join(root, 'tmp', 'edit-ledger.json');
const mode = process.argv[2];

const readStdin = () => {
  try {
    return JSON.parse(fs.readFileSync(0, 'utf8') || '{}');
  } catch {
    return {};
  }
};
const readLedger = () => {
  try {
    return JSON.parse(fs.readFileSync(ledgerPath, 'utf8'));
  } catch {
    return {};
  }
};
const normalise = (p) => path.resolve(p).replace(/\\/g, '/').toLowerCase();

const writeLedger = (ledger) => {
  const now = Date.now();
  const kept = Object.fromEntries(
    Object.entries(ledger).filter(([, v]) => now - v.ts < KEEP_MIN * 60_000),
  );
  fs.mkdirSync(path.dirname(ledgerPath), { recursive: true });
  const tmp = `${ledgerPath}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(kept, null, 1));
  fs.renameSync(tmp, ledgerPath);
};

try {
  const input = readStdin();
  const file = input?.tool_input?.file_path;
  const session = input?.session_id;
  if (!file || !session) process.exit(0);
  const key = normalise(file);
  const ledger = readLedger();

  if (mode === 'record') {
    writeLedger({ ...ledger, [key]: { session, ts: Date.now() } });
    process.exit(0);
  }

  if (mode === 'check') {
    const hit = ledger[key];
    const ageMin = hit ? (Date.now() - hit.ts) / 60_000 : Infinity;
    if (hit && hit.session !== session && ageMin < WINDOW_MIN) {
      const reason =
        `Collision guard: another Claude window (session ${hit.session.slice(0, 8)}) edited ` +
        `${path.basename(file)} ${Math.round(ageMin)} min ago. Approve to edit anyway, or deny ` +
        `and re-read the file first (or switch to a worktree).`;
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: 'PreToolUse',
            permissionDecision: 'ask',
            permissionDecisionReason: reason,
          },
        }),
      );
    }
    process.exit(0);
  }
} catch {
  process.exit(0); // fail open: a broken guard must never block work
}
