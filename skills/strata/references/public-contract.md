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
2. `strata_action_graph`
3. `strata_platform_graph`
4. `strata_status`
5. `strata_markets`
6. The task-specific read or prepare tool

The tool list follows live capability policy. Never assume a tool remains
available because it appeared earlier in a session. Read
`strata_action_graph` after capabilities to discover permitted transitions.

## Market-making workflow

For the ordinary path:

1. Read `strata_market_making_status` and
   `strata_market_making_reputation` for the maker public key and market.
2. Call `strata_market_making_prepare` with `action: "start"`, the market
   label, `product: "strand"` or `"current"`, maker public key, spread bps,
   decimal base size such as `0.01 SOL`, and duration.
3. Verify and externally sign only `prepared.transaction_base64`.
4. Call `strata_market_making_submit_and_wait` with the maker control ID, the
   signed transaction, and the unchanged `preparationToken`.
5. Accept success only when the call returns matching chain-derived maker
   state. Stop through the same pair with `action: "stop"`.

The preparation token contains no signing authority. It carries the strictly
validated public preparation across separate hosted HTTP requests or a process
restart; the external wallet signature and byte-exact verifier remain the
authority boundary. Never reconstruct or modify the token.

The high-level path resolves public IDs, token decimals, the fresh Strata mark,
tick math, fixed arrays, expiry, and bounded defaults. Current follows Strata's
live mark and needs no separate oracle publisher transaction. Use the
product-specific Strand/Current tools only when the strategy intentionally
manages every low-level field.

TypeScript exposes `marketMaking.start(...)`, `stop(...)`, `prepareStart(...)`,
`prepareStop(...)`, and `submitPrepared(...)`. Rust exposes
`platform_maker_start(...)`, `platform_maker_stop(...)`,
`platform_maker_quickstart_prepare(...)`, and
`platform_maker_submit_prepared(...)`.

For collateral, initialize the market Vault if needed, activate the Strand or
Current, then deposit exact atoms with the public Vault prepare/submit flow.
Collateral stays assigned while any control remains live and returns to the
canonical Vault balance only after chain state observes the last control as
disabled, exhausted, expired, or cancelled.

## Terminal workflow

```sh
npx -y @stratabook/sdk capabilities --json
npx -y @stratabook/sdk action-graph --json
npx -y @stratabook/sdk markets --json
npx -y @stratabook/sdk quote \
  --market SOL/USDC \
  --side sell \
  --amount-atoms 10000000 \
  --slippage-bps 50 \
  --json
```

For a non-trading production latency certificate:

```sh
npx -y @stratabook/sdk order-slo \
  --market-id MARKET_ID \
  --owner-wallet OWNER_PUBLIC_KEY \
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

## Account and execution

- `account.read` requires an external signature over the exact wallet, opaque
  market, request time, and fill limit. Replace local state from a fresh signed
  snapshot after a sequence gap.
- Execution prepare and submit are independently gated. A prepared transaction
  must preserve the selected quote or exact opaque order set and be verified
  before external signing.
- Submission is idempotent. The immediate receipt means RPC broadcast, not
  terminal chain completion.
- Persistent order commands use an authenticated SDK WebSocket connection with
  contiguous sequences and correlated request IDs. Terminal status is pushed
  after broadcast and remains durably queryable.
- Both SDKs automatically coalesce concurrent commands into bounded frames and
  negotiate compact bounded result frames. Every command still has an
  independent request ID and sequence; batching never changes signing,
  ordering, idempotency, or receipt semantics.
- `probe(nonce)` is an authenticated non-trading round trip. It only echoes the
  validated nonce and cannot prepare, sign, submit, cancel, or mutate an order.
  The `order-slo` terminal uses it to gate authentication p99, controlled-load
  command p50/p95/p99, at least 25,000 commands/second under saturation, zero
  sequence faults, and bounded error rate.
- Every resting order selects `cancel_taker`, `cancel_maker`, `cancel_both`, or
  `skip_own_liquidity`; none permits a self-fill.
- A dead-man ticket is a pre-signed cancel-all whose durable deadline is
  extended only by authenticated heartbeats. Dropping the guard leaves it
  armed; explicit owner authorization is required to disarm it.

## Authority and safety boundary

The external agent owner controls permissions and signer authority. Strata
exposes capability-gated operations, verifies signatures and immutable
bindings, and never receives private keys. Do not call a write operation unless
its live capability is enabled and the configured signer is authorized for the
exact operation.
