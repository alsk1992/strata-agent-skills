# Strata Agent Skills

Give coding agents the context they need to work confidently with Strata and
Sonar.

These portable skills teach agents how to discover markets, request Sonar
quotes, preserve exact token amounts, and interpret quote results. They work
alongside Strata MCP, the terminal client, or either official SDK.

## Choose your setup

For the fastest experience, connect your agent directly to the hosted Strata MCP
server:

```text
https://api.stratabook.app/mcp
```

Install the skill when you also want reusable product guidance in a coding
agent's context.

## Install

Clone this repository:

```sh
git clone https://github.com/alsk1992/strata-agent-skills.git
cd strata-agent-skills
```

### Codex

```sh
mkdir -p ~/.codex/skills
cp -R skills/strata ~/.codex/skills/strata
```

Invoke it with `$strata`, or let Codex select it for Strata-related work.

### Claude Code

Install it for your user:

```sh
mkdir -p ~/.claude/skills
cp -R skills/strata ~/.claude/skills/strata
```

For a single project, copy the directory to `.claude/skills/strata`. Invoke it
with `/strata`, or let Claude Code select it automatically.

Other tools that support the open `SKILL.md` layout can load
[`skills/strata`](skills/strata) directly.

## Try asking

- “Show me the Strata markets that can return a Sonar quote.”
- “Get a sell quote for SOL/USDC and explain every amount.”
- “Write a TypeScript script that requests a Sonar quote.”
- “Use the Strata CLI and return machine-readable JSON.”

## What the skill adds

- Chooses the right Strata interface for the task.
- Checks live market availability before requesting a quote.
- Handles token amounts as exact atomic-unit strings.
- Explains expected output, fees, minimum output, price impact, and expiry.
- Keeps agents within the capabilities currently available from Strata.

## Official integrations

- [Strata MCP](https://github.com/alsk1992/strata-mcp)
- [TypeScript SDK and CLI](https://github.com/alsk1992/strata-sdk-ts)
- [Rust SDK and CLI](https://github.com/alsk1992/strata-sdk-rs)
- [Agent documentation](https://stratabook.app/docs/hello-agents)

Security issues should be reported privately as described in
[SECURITY.md](SECURITY.md).

Licensed under either [Apache-2.0](LICENSE-APACHE) or [MIT](LICENSE-MIT).
