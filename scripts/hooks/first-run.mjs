#!/usr/bin/env node
// SessionStart hook. Until setup is finished, tell Claude to start (or resume) the
// setup skill on the user's first message. Prints nothing once `.aios-setup-done` exists.
// Never blocks a session: any error exits 0 silently.
import { existsSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

try {
  const root = process.env.CLAUDE_PROJECT_DIR
    || resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');

  if (existsSync(join(root, '.aios-setup-done'))) process.exit(0);

  let resume = false;
  const brainstorms = join(root, 'brain', 'brainstorms');
  if (existsSync(brainstorms)) {
    resume = readdirSync(brainstorms).some((f) => /-setup\.md$/i.test(f));
  }

  const lines = resume
    ? [
        'AIOS FIRST RUN (resume): setup was started and not finished.',
        'On the user\'s first message, invoke the `setup` skill and resume from the capture file in brain/brainstorms/.',
        'Say in one line where you left off, then ask the next question. Do not restart.',
      ]
    : [
        'AIOS FIRST RUN: this clone has not been set up. The brain is empty.',
        'On the user\'s first message, whatever it says, invoke the `setup` skill and begin phase 1 in the same reply.',
        'Do not ask whether to start, do not give a tour. Open in three sentences and ask the first question.',
        'If the first message is an urgent, unrelated request, answer it briefly, then start setup.',
      ];

  process.stdout.write(lines.join('\n') + '\n');
} catch {
  // never block a session
}
process.exit(0);
