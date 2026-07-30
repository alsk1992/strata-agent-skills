# Strata public contract reference

## Interfaces

- Hosted MCP: `https://api.stratabook.app/mcp`
- TypeScript and terminal package: `@stratabook/sdk`
- Rust crates: `strata-public-contract`, `strata-sdk`, `strata-agent-cli`
- Product documentation: `https://stratabook.org/docs/hello-agents`

Prefer MCP for an interactive agent, the terminal for scripts and exploration,
and a language SDK for application code. All interfaces consume the same
versioned public contract.

## MCP workflow

Use the available Strata tools in this order:

1. `strata_capabilities`
2. `strata_markets`
3. `strata_quote`

The tool list follows live capability policy. Never assume a tool remains
available because it appeared earlier in a session.

## Terminal workflow

```sh
npx -y @stratabook/sdk capabilities --json
npx -y @stratabook/sdk markets --json
npx -y @stratabook/sdk quote \
  --market SOL/USDC \
  --side sell \
  --amount-atoms 10000000 \
  --slippage-bps 50 \
  --json
```

## Quote fields

- `quote_id`: opaque identifier for this short-lived quote.
- `server_time_ms` and `expires_at_ms`: authoritative validity window.
- `market_id`: public identifier of the selected market.
- `side`: `buy` or `sell`.
- `amount_in_atoms`: exact requested input.
- `amount_in_consumed_atoms`: input the quote expects to consume.
- `amount_out_atoms`: quoted output before the user's minimum-output guard.
- `minimum_output_atoms`: minimum acceptable output at the requested slippage.
- `input_fee_atoms`: fee denominated in the input asset.
- `output_fee_atoms`: fee denominated in the output asset.
- `reference_price`: public reference price as a decimal string.
- `price_impact_pct`: public price-impact estimate as a decimal string.
- `provider`: always `Sonar` for this contract.

All token amounts are unsigned base-10 atomic strings. Do not convert them
through floating point.

## Failure handling

- Retry only when the public error explicitly marks the failure retryable.
- Refresh capabilities and markets after a policy or availability error.
- Request a new quote after expiry; never extend an old quote locally.
- Stop on unknown fields, unsupported contract versions, binding mismatches, or
  inconsistent economics.
- If a requested breakdown is not present, explain that the response is a
  unified Sonar quote and report the published economic fields instead.

## Safety boundary

The `0.1.x` tools are read-only. They discover capabilities, list markets, and
request quotes. They do not prepare, sign, or submit transactions and do not
accept wallet material.
