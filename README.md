# Strata Agent Skills

Official portable guidance for agents interacting with Strata and Sonar. The
skills follow the open `SKILL.md` layout used by modern coding agents and keep
detailed references out of the default context until needed.

## Fastest path: hosted MCP

Connect a Streamable HTTP MCP client to:

```text
https://api.stratabook.app/mcp
```

The server exposes only the tools allowed by Strata's live public capability
policy.

## Install the Strata skill

Clone this repository, then copy [`skills/strata`](skills/strata) into your
agent's personal or project skill directory.

For Codex:

```sh
mkdir -p ~/.codex/skills
cp -R skills/strata ~/.codex/skills/strata
```

For Claude Code:

```sh
mkdir -p ~/.claude/skills
cp -R skills/strata ~/.claude/skills/strata
```

For a project-scoped Claude Code installation, copy it to
`.claude/skills/strata`. Other Agent Skills-compatible tools can load the same
directory directly.

The skill can be invoked explicitly as `$strata` in Codex or `/strata` in Claude
Code. It may also activate automatically for requests about Strata markets or
Sonar quotes.

## What agents learn

- Discover live capabilities before taking action.
- Select only quote-ready markets.
- Preserve token amounts as exact atomic strings.
- Validate quote binding, fees, minimum output, and expiry.
- Treat Sonar as one unified product without exposing or guessing its internal
  liquidity and matching composition.
- Stay inside the current read-only safety boundary.

The package SDKs live in
[`alsk1992/strata-sdk-ts`](https://github.com/alsk1992/strata-sdk-ts) and
[`alsk1992/strata-sdk-rs`](https://github.com/alsk1992/strata-sdk-rs). The
official MCP adapter lives in
[`alsk1992/strata-mcp`](https://github.com/alsk1992/strata-mcp).
