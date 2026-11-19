---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, claude-code, mods, privacy, screen-recording]
related: ["[[wiki/concepts/claude-code-mods]]", "[[wiki/sources/nateherk-claude-code-mods]]"]
---

# Mod: Recording mode

**What it does.** A toggle, typed as a slash command named "record" (then "off", or the command again to turn it back on), that hides sensitive text on screen while you record video: emails, internal and financial figures. Claude still receives and works with the real values [05:21-07:05]. Source: [[wiki/sources/nateherk-claude-code-mods|Nate Herk, Claude Code mods]].

## What Nate showed

- Asked for his GitHub account email, the reply used placeholders instead of the address [05:51-06:06].
- He pasted HTML with a price to change from $29 to $39. The pasted numbers appeared blurred in the chat, yet the file really changed from 29 to 39. So it masks the display and leaves the model input alone [06:24-06:47].
- Toggling off un-blurs everything; toggling on blurs again [06:50-07:04].

## Setup

Turned on with a slash command; mods live in local files as an installed plugin [07:06-07:14]. No code was shown.

## Caveats

Nate mixes two behaviours: placeholders the model writes (a prompt effect) and display blur (a UI effect). The model still sees the real data, so the mod cannot stop the model from echoing it into a file or tool call, and screen blur is only as good as its detector (unverified: no adversarial test was shown). Anthropic says mods can also redact secrets from tool output before Claude reads it, which is a stronger mechanism than display blur.
