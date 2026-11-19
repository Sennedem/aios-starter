---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [wiki, tool, hostinger, hosting, agents]
related: ["[[wiki/tools/hermes-agent]]", "[[wiki/concepts/managed-vs-vps-agent-hosting]]", "[[wiki/concepts/subscription-oauth-vs-api-key-auth]]", "[[wiki/sources/nateherk-managed-hermes-setup]]"]
---

# Hostinger managed agents

Hostinger's hPanel has a dedicated **AI Agents** section (next to its usual websites, domains and email) that deploys three managed agent apps in one click: **Open Claw**, **Hermes** and **N8N**. [02:12-02:53] Each is provisioned as its own app under "AI automation apps"; Nate Herk shows two separate Hermes instances running side by side in one account. Source: [[wiki/sources/nateherk-managed-hermes-setup|Nate Herk's managed Hermes setup video]].

## Provisioning flow

1. hPanel, then AI Agents, then pick the app (for example Hermes Agent), then "Get new app" and "Get started."
2. Choose a plan. Bundled AI credits, 1,000 free web-scraping credits and "Agentic Mail" (an email address for the agent) are optional add-ons at this step. Nate turns the AI credits off ("I don't think you're going to use those").
3. Choose the underlying model: paste an API key, or connect a subscription instead (ChatGPT in the demo). See [[wiki/concepts/subscription-oauth-vs-api-key-auth|subscription OAuth vs API-key auth]].
4. Add environment variables (API keys for tools the agent should use, such as Tavily) later under the app's Environment settings. Applying changes resets the app and forces a fresh login to its web panel (the password can be copied from there). If a just-added key still isn't visible to the agent, restart the app manually from hPanel instead of re-entering the key.

The video includes Nate's own affiliate link and a 10% coupon (yearly plans only) for this signup page. That is how the source makes money, not part of the technique.

The managed-vs-VPS choice for hosting an always-on agent is on [[wiki/concepts/managed-vs-vps-agent-hosting|managed vs VPS agent hosting]].
