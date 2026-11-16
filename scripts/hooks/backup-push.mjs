#!/usr/bin/env node
/**
 * backup-push.mjs: SessionEnd hook. Commits everything, rebases onto the remote, pushes.
 *
 * Why it rebases: anything else that commits to the same branch (a CI job such as the
 * janitor workflow, a second machine) makes a plain `git push` get rejected. A backup
 * that fails silently is worse than none, because the docs keep saying the remote is the
 * off-machine copy. So: pull --rebase before the push, and never fail silently. When the
 * backup does not land, tmp/BACKUP-PUSH-FAILED.md is written (tmp/ is gitignored) and the
 * next session's catch-up surfaces it.
 *
 * Why it checks privacy: the brain holds private notes. This hook pushes ONLY when the
 * `origin` remote is confirmed private (via `gh repo view --json visibility`). A positive
 * result is cached in tmp/.backup-remote-private. A public remote, an unknown one, or no
 * `gh` CLI means: commit locally, skip the push, print one line saying why.
 *
 * Other safeties: a stale .git/index.lock left by a killed hook is removed only when no
 * git process is running; a rebase or merge already in progress is never committed into;
 * a rebase this hook started and that hit a conflict is aborted, so local commits stay
 * intact; network steps are bounded by a timeout. Closing the editor can kill SessionEnd
 * hooks mid-run, so an in-progress marker exposes an interrupted run to the next one.
 *
 * Not a git repo: exit 0. No remote: commit locally, exit 0 quietly. Always exits 0.
 * Every child process spawns with windowsHide so no console window flashes on Windows.
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(process.env.CLAUDE_PROJECT_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..'));
const NET_TIMEOUT_MS = 45_000;
const PRIVACY_RECHECK_MS = 7 * 24 * 3600 * 1000;
const TMP = path.join(ROOT, 'tmp');
const FLAG = path.join(TMP, 'BACKUP-PUSH-FAILED.md');
const LOG = path.join(TMP, 'backup-push.log');
const MARK = path.join(TMP, 'backup-push.inprogress');
const PRIVATE_CACHE = path.join(TMP, '.backup-remote-private');
const now = new Date();
const pad = n => String(n).padStart(2, '0');
const STAMP = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
let NOTE = '';
let logText = '';

function run(cmd, args, timeout) {
  const r = spawnSync(cmd, args, { cwd: ROOT, encoding: 'utf8', windowsHide: true, timeout, stdio: ['ignore', 'pipe', 'pipe'] });
  const out = ((r.stdout || '') + (r.stderr || '')).trim();
  return { ok: r.status === 0, status: r.status, out, timedOut: r.error?.code === 'ETIMEDOUT' || r.signal === 'SIGTERM', missing: r.error?.code === 'ENOENT' };
}
const git = (args, timeout) => run('git', args, timeout);
const logged = r => { if (r.out) logText += r.out + '\n'; return r; };

function done(code = 0) {
  try { fs.unlinkSync(MARK); } catch { /* not there */ }
  process.exit(code);
}

function fail(msg) {
  try {
    const parts = [`# Backup push FAILED ${STAMP}`, '', msg];
    if (NOTE) parts.push('', `Also: ${NOTE}`);
    parts.push('', 'Local commits are safe on this machine but NOT on the remote until this is resolved.');
    if (logText.trim()) parts.push('', '```', logText.trim(), '```');
    fs.writeFileSync(FLAG, parts.join('\n') + '\n', 'utf8');
  } catch { /* nothing more to do */ }
  done(0);
}

function gitRunning() {
  const r = process.platform === 'win32'
    ? run('tasklist', ['/FI', 'IMAGENAME eq git.exe', '/NH'], 10_000)
    : run('pgrep', ['-x', 'git'], 10_000);
  if (process.platform === 'win32') return /git\.exe/i.test(r.out);
  return r.ok;
}

// "git@github.com:owner/repo.git" or "https://github.com/owner/repo(.git)" -> "owner/repo"
function githubSlug(url) {
  const m = /github\.com[:/]+([^/\s]+)\/([^/\s]+?)(?:\.git)?\/?$/i.exec(url || '');
  return m ? `${m[1]}/${m[2]}` : null;
}

function readCache(url) {
  try {
    const st = fs.statSync(PRIVATE_CACHE);
    const cached = fs.readFileSync(PRIVATE_CACHE, 'utf8').trim();
    if (cached !== url) return null;
    return { fresh: Date.now() - st.mtimeMs < PRIVACY_RECHECK_MS };
  } catch { return null; }
}

// Returns { private: true } or { private: false, why }.
function checkPrivate(url) {
  const cache = readCache(url);
  if (cache && cache.fresh) return { private: true };
  const slug = githubSlug(url);
  if (!slug) {
    if (cache) return { private: true };   // a non-GitHub remote the user confirmed by hand
    return { private: false, why: `origin (${url}) is not on GitHub, so its privacy cannot be checked automatically. If you have confirmed it is private, write that exact URL into tmp/.backup-remote-private.` };
  }
  const r = run('gh', ['repo', 'view', slug, '--json', 'visibility', '-q', '.visibility'], NET_TIMEOUT_MS);
  if (r.missing) {
    if (cache) return { private: true };   // confirmed before; gh has since gone missing
    return { private: false, why: 'the GitHub CLI (gh) is not installed, so the remote could not be confirmed private. Install gh and run `gh auth login`, or run /setup, which creates a private repo.' };
  }
  const vis = r.ok ? r.out.split('\n').pop().trim().toUpperCase() : '';
  if (vis === 'PRIVATE') {
    try { fs.writeFileSync(PRIVATE_CACHE, url + '\n', 'utf8'); } catch { /* cache is optional */ }
    return { private: true };
  }
  try { fs.unlinkSync(PRIVATE_CACHE); } catch { /* not there */ }
  if (vis === 'PUBLIC' || vis === 'INTERNAL') {
    return { private: false, why: `origin (${slug}) is ${vis.toLowerCase()}. A brain holds private notes, so it is never pushed there. Make the repo private on GitHub, or run /setup, which creates a private repo.` };
  }
  if (cache) return { private: true };      // offline or gh not logged in; confirmed before
  return { private: false, why: `could not confirm that origin (${slug}) is private (gh said: ${(r.out || 'no answer').split('\n')[0].slice(0, 120)}). Run \`gh auth login\`, or run /setup, which creates a private repo.` };
}

function main() {
  if (process.env.CLAUDE_CODE_REMOTE) done(0);   // cloud sandboxes have no credentials for this
  if (!fs.existsSync(ROOT)) done(0);

  // Only act when ROOT itself is the top of a git work tree (never a parent repo).
  const top = git(['rev-parse', '--show-toplevel'], 15_000);
  const real = p => { try { return fs.realpathSync.native(path.resolve(p)); } catch { return path.resolve(p); } };
  const same = (a, b) => process.platform === 'win32' ? a.toLowerCase() === b.toLowerCase() : a === b;
  if (!top.ok || !same(real(top.out.split('\n').pop().trim()), real(ROOT))) done(0);
  const gitDirR = git(['rev-parse', '--absolute-git-dir'], 15_000);
  if (!gitDirR.ok) done(0);
  const GIT_DIR = gitDirR.out.split('\n').pop().trim();

  fs.mkdirSync(TMP, { recursive: true });

  // 0. Was the previous run killed before it finished? The marker outlives a kill.
  let prevKilled = false;
  if (fs.existsSync(MARK)) {
    prevKilled = true;
    let started = '';
    try { started = fs.readFileSync(MARK, 'utf8').trim(); } catch { /* unreadable */ }
    NOTE = `The previous session-end backup (started ${started || 'at an unknown time'}) was interrupted before it finished; closing the editor can kill SessionEnd hooks.`;
  }
  fs.writeFileSync(MARK, STAMP, 'utf8');

  // 1. A lock with no owning git process is stale (a killed hook leaves one). Remove it.
  const lock = path.join(GIT_DIR, 'index.lock');
  if (fs.existsSync(lock)) {
    if (gitRunning()) fail('Another git process holds .git/index.lock, so nothing was committed or pushed. Retry after it finishes.');
    const age = Math.round((Date.now() - fs.statSync(lock).mtimeMs) / 1000);
    if (age >= 60) {
      try { fs.unlinkSync(lock); } catch { fail('Could not remove a stale .git/index.lock. Delete it by hand, then run `git push`.'); }
      NOTE = `${NOTE ? NOTE + ' ' : ''}Removed a stale .git/index.lock (${age}s old, no git process).`;
    } else {
      fail(`A fresh .git/index.lock (${age}s old) exists with no git process; refused to remove it this fast. If it is still there in a minute, delete it by hand and run \`git push\`.`);
    }
  }

  // 2. Never commit into a half-finished rebase or merge. A rebase this hook started itself
  //    (previous run killed, marker still present) is aborted; anything else is left for a human.
  const rebasing = () => fs.existsSync(path.join(GIT_DIR, 'rebase-merge')) || fs.existsSync(path.join(GIT_DIR, 'rebase-apply'));
  if (fs.existsSync(path.join(GIT_DIR, 'rebase-merge')) && prevKilled) {
    if (logged(git(['rebase', '--abort'], 60_000)).ok) NOTE = `${NOTE ? NOTE + ' ' : ''}Aborted the rebase the killed run left behind.`;
    else fail('The previous backup was killed mid-rebase and `git rebase --abort` failed. Run `git status` and resolve by hand.');
  }
  if (rebasing() || fs.existsSync(path.join(GIT_DIR, 'MERGE_HEAD'))) {
    fail('A rebase or merge was already in progress, so nothing was committed or pushed. Run `git status`, finish or abort it, then run `git push`.');
  }

  // 3. Commit whatever the session left behind.
  if (!logged(git(['add', '-A'], 120_000)).ok) fail('`git add -A` failed.');
  const staged = git(['diff', '--cached', '--quiet'], 60_000);
  if (staged.status === 1) {
    if (!logged(git(['commit', '-q', '-m', `backup (session end): ${STAMP}`], 120_000)).ok) {
      fail('`git commit` failed. If git says it does not know who you are, set `git config user.name` and `git config user.email` once.');
    }
  }

  // 4. No remote: the local commit is the whole job.
  const remote = git(['remote', 'get-url', 'origin'], 15_000);
  if (!remote.ok || !remote.out) done(0);
  const url = remote.out.split('\n').pop().trim();

  // 5. Push only to a remote confirmed private.
  const priv = checkPrivate(url);
  if (!priv.private) {
    console.log(`[backup] Committed locally, push skipped: ${priv.why}`);
    done(0);
  }

  const branchR = git(['symbolic-ref', '--short', 'HEAD'], 15_000);
  if (!branchR.ok) fail('HEAD is detached, so there is no branch to push. Check out your main branch and run `git push`.');
  const branch = branchR.out.split('\n').pop().trim();

  // 6. Bring in what was committed elsewhere, replaying local commits on top.
  const heads = git(['ls-remote', '--exit-code', '--heads', 'origin', branch], NET_TIMEOUT_MS);
  if (heads.timedOut) fail(`\`git ls-remote origin\` timed out after ${NET_TIMEOUT_MS / 1000}s (network). Run \`git pull --rebase --autostash origin ${branch} && git push\` by hand.`);
  const remoteHasBranch = heads.ok;
  if (!remoteHasBranch && heads.status !== 2) {
    logged(heads);
    fail('`git ls-remote origin` failed (network or auth). Run `git push` by hand to see the error.');
  }
  if (remoteHasBranch) {
    const pull = logged(git(['pull', '--rebase', '--autostash', '-q', 'origin', branch], NET_TIMEOUT_MS));
    if (!pull.ok) {
      if (rebasing()) git(['rebase', '--abort'], 60_000);
      if (pull.timedOut) fail(`\`git pull --rebase origin ${branch}\` timed out after ${NET_TIMEOUT_MS / 1000}s (network). Run \`git pull --rebase --autostash origin ${branch} && git push\` by hand.`);
      fail(`\`git pull --rebase origin ${branch}\` failed (a conflict, network or auth) and any rebase was aborted. Resolve by hand: \`git pull --rebase --autostash origin ${branch}\`, fix conflicted files, \`git rebase --continue\`, \`git push\`.`);
    }
  }

  // 7. Push, and clear the flag only on a verified success.
  const push = logged(git(['push', '-q', ...(remoteHasBranch ? [] : ['-u']), 'origin', branch], NET_TIMEOUT_MS));
  if (push.ok) {
    try { fs.unlinkSync(FLAG); } catch { /* not there */ }
    try { fs.unlinkSync(LOG); } catch { /* not there */ }
    done(0);
  }
  fail(`\`git push origin ${branch}\` did not land after a clean rebase (network, auth, or a ${NET_TIMEOUT_MS / 1000}s timeout). Run \`git push\` by hand.`);
}

try { main(); } catch (e) {
  try { fail('The backup hook crashed: ' + String(e && e.message || e).split('\n')[0]); } catch { /* fall through */ }
}
done(0);
