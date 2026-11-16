#!/usr/bin/env node
// Machine check for AIOS. No dependencies, Node 18+.
//
//   node scripts/doctor.mjs                   report what is installed and what is missing
//   node scripts/doctor.mjs --json            same, as JSON
//   node scripts/doctor.mjs --register-vault  add brain/ to Obsidian's vault list (close Obsidian first)
//   node scripts/doctor.mjs --open-vault      open the brain vault in Obsidian
//
// It never installs anything. It prints the install command for this system and the
// setup skill runs it after the user says yes.
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync, copyFileSync, mkdirSync } from 'node:fs';
import { homedir, platform } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomBytes } from 'node:crypto';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const brain = join(root, 'brain');
const os = platform();
const args = new Set(process.argv.slice(2));
const STARTER = /github\.com[:/]+sennedem\/aios-starter(\.git)?$/i;

function run(cmd, cmdArgs = []) {
  try {
    const r = spawnSync(cmd, cmdArgs, { encoding: 'utf8', windowsHide: true, timeout: 15000, cwd: root });
    return { ok: r.status === 0, out: `${r.stdout || ''}`.trim(), err: `${r.stderr || ''}`.trim() };
  } catch {
    return { ok: false, out: '', err: '' };
  }
}

function obsidianInstalled() {
  const home = homedir();
  if (os === 'win32') {
    const local = process.env.LOCALAPPDATA || join(home, 'AppData', 'Local');
    return [join(local, 'Programs', 'Obsidian', 'Obsidian.exe'), join(local, 'Obsidian', 'Obsidian.exe')]
      .some(existsSync);
  }
  if (os === 'darwin') {
    return ['/Applications/Obsidian.app', join(home, 'Applications', 'Obsidian.app')].some(existsSync);
  }
  if (run('which', ['obsidian']).ok) return true;
  return [
    join(home, '.var', 'app', 'md.obsidian.Obsidian'),
    '/var/lib/flatpak/app/md.obsidian.Obsidian',
    '/snap/bin/obsidian',
  ].some(existsSync);
}

function obsidianInstallCommand() {
  if (os === 'win32') return 'winget install -e --id Obsidian.Obsidian';
  if (os === 'darwin') return 'brew install --cask obsidian';
  return 'flatpak install -y flathub md.obsidian.Obsidian';
}

function obsidianConfigPath() {
  if (process.env.OBSIDIAN_CONFIG) return process.env.OBSIDIAN_CONFIG; // override, used for testing
  const home = homedir();
  if (os === 'win32') return join(process.env.APPDATA || join(home, 'AppData', 'Roaming'), 'obsidian', 'obsidian.json');
  if (os === 'darwin') return join(home, 'Library', 'Application Support', 'obsidian', 'obsidian.json');
  const flatpak = join(home, '.var', 'app', 'md.obsidian.Obsidian', 'config', 'obsidian', 'obsidian.json');
  if (existsSync(dirname(flatpak))) return flatpak;
  return join(process.env.XDG_CONFIG_HOME || join(home, '.config'), 'obsidian', 'obsidian.json');
}

const samePath = (a, b) => {
  const norm = (p) => resolve(p).replace(/[\\/]+$/, '');
  return os === 'win32' ? norm(a).toLowerCase() === norm(b).toLowerCase() : norm(a) === norm(b);
};

function registerVault() {
  const file = obsidianConfigPath();
  let config = {};
  if (existsSync(file)) {
    try {
      config = JSON.parse(readFileSync(file, 'utf8'));
    } catch {
      console.log(`Could not parse ${file}. Left it untouched. Open Obsidian and use "Open folder as vault" on: ${brain}`);
      return 1;
    }
    copyFileSync(file, `${file}.bak-aios`);
  } else {
    mkdirSync(dirname(file), { recursive: true });
  }
  if (typeof config !== 'object' || config === null || Array.isArray(config)) config = {};
  config.vaults = config.vaults && typeof config.vaults === 'object' ? config.vaults : {};

  const already = Object.values(config.vaults).some((v) => v && v.path && samePath(v.path, brain));
  if (already) {
    console.log(`Already registered: ${brain}`);
    return 0;
  }
  config.vaults[randomBytes(8).toString('hex')] = { path: brain, ts: Date.now(), open: true };
  writeFileSync(file, JSON.stringify(config));
  console.log(`Registered the vault: ${brain}`);
  console.log('Start Obsidian and it opens. The first time, Obsidian asks whether you trust the vault.');
  return 0;
}

function openVault() {
  const uri = `obsidian://open?path=${encodeURIComponent(brain)}`;
  const r = os === 'win32'
    ? run('cmd', ['/c', 'start', '""', uri])
    : os === 'darwin' ? run('open', [uri]) : run('xdg-open', [uri]);
  console.log(r.ok ? `Opening ${brain} in Obsidian.` : `Could not open it automatically. Open Obsidian and pick the vault at: ${brain}`);
  return r.ok ? 0 : 1;
}

function report() {
  const nodeMajor = Number(process.versions.node.split('.')[0]);
  const git = run('git', ['--version']);
  const gh = run('gh', ['--version']);
  const ghAuth = gh.ok ? run('gh', ['auth', 'status']) : { ok: false };
  const isRepo = git.ok && run('git', ['rev-parse', '--is-inside-work-tree']).ok;
  const origin = isRepo ? run('git', ['remote', 'get-url', 'origin']) : { ok: false, out: '' };

  let remote = 'none';
  let remoteNote = 'No origin remote. Setup offers a private backup at the end.';
  if (origin.ok && origin.out) {
    if (STARTER.test(origin.out)) {
      remote = 'starter';
      remoteNote = 'origin is the public starter repo. Remove it (git remote remove origin) before your notes go anywhere.';
    } else if (ghAuth.ok) {
      const vis = run('gh', ['repo', 'view', origin.out, '--json', 'visibility', '-q', '.visibility']);
      remote = vis.ok && vis.out ? vis.out.toLowerCase() : 'unknown';
      remoteNote = remote === 'private'
        ? 'origin is private. Backups can push there.'
        : remote === 'public'
          ? 'origin is PUBLIC. Your notes must not be pushed there. Remove it or make the repo private.'
          : 'Could not confirm that origin is private. The backup hook will not push until it can.';
    } else {
      remote = 'unknown';
      remoteNote = 'Could not check whether origin is private (GitHub CLI missing or not logged in). The backup hook will not push until it can.';
    }
  }

  const obsidian = obsidianInstalled();
  const result = {
    os,
    node: { ok: nodeMajor >= 18, version: process.versions.node },
    git: { ok: git.ok, version: git.out },
    githubCli: { installed: gh.ok, loggedIn: ghAuth.ok },
    gitRepo: isRepo,
    remote,
    obsidian: { installed: obsidian, installCommand: obsidianInstallCommand(), config: obsidianConfigPath() },
    brain,
    setupDone: existsSync(join(root, '.aios-setup-done')),
  };

  if (args.has('--json')) {
    console.log(JSON.stringify(result, null, 2));
    return 0;
  }

  const mark = (ok) => (ok ? 'ok     ' : 'MISSING');
  console.log('AIOS machine check');
  console.log(`  ${mark(result.node.ok)} Node ${result.node.version}${result.node.ok ? '' : ' (needs 18 or newer, the hooks will not run)'}`);
  console.log(`  ${mark(git.ok)} git${git.ok ? '' : ' (no backups or history until it is installed)'}`);
  console.log(`  ${mark(gh.ok && ghAuth.ok)} GitHub CLI${gh.ok ? (ghAuth.ok ? '' : ' (installed, run: gh auth login)') : ' (optional, needed for the private backup)'}`);
  console.log(`  ${mark(obsidian)} Obsidian${obsidian ? '' : `  install with: ${result.obsidian.installCommand}   or download from https://obsidian.md`}`);
  const remoteOk = isRepo && (remote === 'private' || remote === 'none');
  console.log(`  ${remoteOk ? 'ok     ' : 'note   '} ${isRepo ? remoteNote : 'Not a git repository yet. Run: git init'}`);
  console.log(`  vault   ${brain}`);
  console.log(`  setup   ${result.setupDone ? 'done' : 'not done yet. Start Claude Code here and say: start'}`);
  return 0;
}

let code = 0;
if (args.has('--register-vault')) code = registerVault();
else if (args.has('--open-vault')) code = openVault();
else code = report();
process.exit(code);
