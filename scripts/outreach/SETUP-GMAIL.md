# Connect your Gmail to the outreach engine

This is a one-time setup, about 20 minutes. When you finish, the `/outreach` skill can send the e-mails you approve from your own Gmail address, through a small automated job (a GitHub Action) in your own private backup repository. No paid service, and no session needs to be open while mail goes out.

You will do four things: create a free Google Cloud project, give it permission to use Gmail, create a login key for it, and store that key in GitHub as a secret. Every step below says what you should see when it worked. If what you see is different, stop and ask Claude: paste the message you see, never a key or a password.

## Before you start

You need:

- **The Gmail account you want to send from.** Log in to it in your browser now. If you use several Google accounts, use a private browser window with only this one logged in, so nothing gets set up under the wrong account.
- **Your backup repository on GitHub, set to private.** Setup created it. To check: open it on github.com. Next to the name it should say **Private**. If it says Public, go to Settings, scroll to the bottom (Danger Zone), choose Change visibility, and make it private. This matters: the engine stores who you e-mailed and what you wrote inside the repository.
- **Python 3 on your computer.** In a terminal, run `python --version` (on Windows, `py --version` also works). You should see `Python 3.something`. If not, ask Claude to install it.

## Step 1: create a Google Cloud project

1. Go to https://console.cloud.google.com and accept the terms if asked.
2. At the top left, next to the Google Cloud logo, click the project picker (it may say "Select a project").
3. Click **New project**. Name it `my-outreach` (any name works). Leave the location as it is. Click **Create**.
4. When the notification bell says the project is ready, open the project picker again and select `my-outreach`.

**You should see:** `my-outreach` in the bar at the top of the page.

## Step 2: switch on the Gmail API

1. In the search bar at the top, type `Gmail API` and click the result with that name.
2. Click **Enable**.

**You should see:** a page titled Gmail API with a **Manage** button and the words "API enabled".

## Step 3: set up the consent screen

This is the screen Google shows when your script asks for access. Only you will ever see it.

1. Open the menu (three lines, top left), then **APIs & Services**, then **OAuth consent screen**. Google calls this area the **Google Auth Platform**. Click **Get started**.
2. **App information:** App name `My outreach`, User support email: your own address. Click **Next**.
3. **Audience:** pick the first of these that you are offered:
   - **Personal**, if it is listed: only your own account can use it, nothing expires, and there is no warning screen. Best choice.
   - **Internal**, if you use Google Workspace (a company address) and it is listed: only people in your organisation, nothing expires.
   - **External** otherwise (a normal Gmail address). Step 3.6 below is then required.
   Click **Next**.
4. **Contact information:** your own address. Click **Next**.
5. Tick the box to agree to the user data policy, click **Continue**, then **Create**.
6. **Only if you chose External:** in the left menu click **Audience**. Under Publishing status it says **Testing**. Click **Publish app**, then **Confirm**. Do not click "Prepare for verification" and do not submit anything: verification is for apps used by the public, and you are the only user.

**You should see:** the Google Auth Platform overview page. If you chose External, the Audience page now says **In production**.

**Why step 3.6 matters:** while an External app is in Testing, Google cancels its login after seven days. The engine would work for a week and then stop with an `invalid_grant` error. Publishing removes that limit.

## Step 4: create the login key (a "Desktop" client)

1. In the Google Auth Platform left menu, click **Clients**, then **Create client**.
2. Application type: **Desktop app**. Name: `outreach`. Click **Create**.
3. A box shows a **Client ID** and a **Client secret**. Click **Download JSON** or copy both values somewhere safe for the next step. Google may show the secret only this once. If you lose it, open the client and add a new secret.

**You should see:** the client `outreach` in the list, type Desktop.

## Step 5: put the two values in your `.env` file

The `.env` file sits in the top folder of your AIOS and never leaves your computer (git ignores it).

1. Ask Claude: "prepare the Gmail lines in .env". It adds three empty lines and opens the file:
   ```
   GMAIL_CLIENT_ID=
   GMAIL_CLIENT_SECRET=
   GMAIL_REFRESH_TOKEN=
   ```
2. Paste the Client ID after `GMAIL_CLIENT_ID=` and the Client secret after `GMAIL_CLIENT_SECRET=`. Leave the third line empty. Save the file.

Paste the values into the file, never into the chat.

**You should see:** two filled lines and one empty line in `.env`.

## Step 6: let the script log in to your Gmail once

1. In a terminal in your AIOS folder, run:
   ```
   python -m pip install requests
   python scripts/outreach/get_refresh_token.py
   ```
   (On Windows, if `python` is not found, use `py` in both lines.)
2. Your browser opens a Google sign-in page. Choose the Gmail account you send from.
3. If you see **"Google hasn't verified this app"**: that is expected for your own private app. Click **Advanced**, then **Go to My outreach (unsafe)**. The word "unsafe" only means Google has not reviewed it; it is your own project.
4. Google lists what the app may do: send e-mail, and read and organise your mail (the engine needs that to spot replies and bounces on the mails it sent). Tick every box and click **Continue**.

**You should see:** the browser says "Done. You can close this tab", and the terminal says `Refresh token obtained and written to ...`. The third line in `.env` is now filled. The script never prints the token on purpose.

If it says `No refresh_token in the response`: go to https://myaccount.google.com/permissions, remove **My outreach**, and run the script again.

## Step 7: store the three values in GitHub

The send job runs on GitHub's computers, which cannot read your `.env`. You give it the same three values as **repository secrets**: GitHub keeps them encrypted, and nobody (you included) can read them back after saving. Pick one of the two routes.

### 7a. By hand on github.com (no extra tools)

1. Open your backup repository on github.com.
2. Click **Settings** (top right of the repository, not your account settings).
3. In the left menu: **Secrets and variables**, then **Actions**.
4. Click **New repository secret**. Name: `GMAIL_CLIENT_ID`. Secret: paste the value from your `.env` (only the part after the `=`, without quotes). Click **Add secret**.
5. Repeat for `GMAIL_CLIENT_SECRET` and `GMAIL_REFRESH_TOKEN`.

**You should see:** three secrets listed under Repository secrets, with their values hidden.

### 7b. With the helper script (needs the GitHub CLI)

1. If you have never used it: install the GitHub CLI from https://cli.github.com, then run `gh auth login` and follow the prompts.
2. Run:
   ```
   python scripts/outreach/set_github_secrets.py
   ```

**You should see:** `set GMAIL_CLIENT_ID`, `set GMAIL_CLIENT_SECRET`, `set GMAIL_REFRESH_TOKEN`, then `All three secrets set`. The script refuses to run if the repository is public.

## Step 8: fill in your sender details

Run `/outreach` and say "set up my sender". Claude asks for your address, name, role, optional photo link, timezone and where the daily digest should go, and fills `scripts/outreach/outreach.config.json` for you. It also asks which countries you will e-mail, so you can check the cold e-mail rules there first.

## Step 9: test it

1. **The daily monitor.** On github.com, open your repository, click the **Actions** tab, click **Outreach monitor** on the left, then **Run workflow**, then the green **Run workflow** button.
   **You should see:** after a minute, a green check mark next to the run. A red cross means something is off: click the run, then the failed step, and show Claude the error text.
2. **A first real e-mail, to yourself.** Ask `/outreach` for one test e-mail to another address of your own, review it, and say send.
   **You should see:** within a few minutes, the e-mail in that inbox with your signature, and in your Gmail Sent folder.

## Step 10: get told when a job fails

GitHub does not always e-mail you when an automated job fails. Turn it on: go to https://github.com/settings/notifications, find **Actions**, and choose to be notified about failed workflows only. The engine also writes `scripts/outreach/heartbeat.md` every day, and `/outreach` warns you when it is stale, so a silent failure gets caught either way.

## If something goes wrong

| You see | What it means | What to do |
|---|---|---|
| `invalid_grant` in a failed run | The Gmail login expired or was removed | Check step 3.6 (External apps must be In production), then redo step 6 and update the `GMAIL_REFRESH_TOKEN` secret (step 7) |
| `Missing required environment variable GMAIL_...` | A secret is missing or misspelled | Compare the three names in step 7 letter by letter |
| `The Gmail token belongs to ...` | You logged in with another account in step 6 | Redo step 6 in a private window logged in only as the sender |
| `outreach.config.json is not filled in yet` | Step 8 was skipped | Run `/outreach` and say "set up my sender" |
| `Error 403: access_denied` in the browser | The app is in Testing and your account is not a test user, or a company admin blocks it | External: publish the app (step 3.6). Company account: ask your admin to allow it |
| A run is green but nothing arrived | The mail waited for its day or the daily cap, or was held by the lint check | Look in `outbox/` (waiting) and `outbox/held/` (held, with the reason) |

## What this costs

Nothing, for normal use. Google Cloud does not charge for the Gmail API at this volume. GitHub gives private repositories 2,000 free Action minutes a month on the free plan; each send or monitor run takes well under a minute.
