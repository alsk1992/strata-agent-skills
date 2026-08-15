---
name: strata
description: Discover and use Strata's capability-gated market, Sonar quote, account, execution, and persistent order-command interfaces. Use when an agent needs live market data, exact trade economics, externally signed operations, safe resting-order automation, dead-man cancellation, or order-stream latency certification.
---

# Strata

Use Strata's official interfaces to discover live capabilities, inspect markets,
request Sonar quotes, and—when the external agent owner has configured signer
authority—prepare and submit externally signed operations.

## Choose an interface

1. Prefer the configured Strata MCP tools for discovery and interactive work.
2. Use `npx -y @stratabook/sdk` for terminal discovery, scripted action
   primitives, and non-trading certification.
3. Use the TypeScript or Rust SDK for persistent market, account, or order-command streams.

Do not call undocumented HTTP paths or reconstruct private behavior.

## Enter through discovery

1. Read live capabilities before every objective.
2. Read the executable action graph and follow only edges whose required live
   capabilities are enabled.
3. List markets and select an opaque market ID marked ready.
4. Resolve the exact side, atomic amount, tolerance, and owner-configured signer
   authority. Ask when an economically meaningful input is ambiguous.
5. Request a fresh Sonar quote and verify its market, side, input, fees, minimum
   output, server time, and expiry.
6. Report consumed input, expected and minimum output, fees by asset side,
   price impact, and remaining validity.

Never silently convert a human token amount without confirmed token decimals.
Preserve every atomic amount as a base-10 string.

## Execute when available

- Treat preparation and submission as separate live capabilities. Package
  support or an earlier session never enables an operation.
- Keep all signing external to Strata. Request canonical authorization bytes,
  have the owner-configured signer sign them, verify the prepared transaction,
  and submit with a stable idempotency key.
- For resting orders, select an explicit self-trade prevention policy. Never
  infer one and never accept a mode that permits a self-fill.
- Prefer the official persistent order-command client for latency-sensitive
  place, cancel, cancel-all, replace, and batch operations when WebSocket
  transport is advertised.
- Treat placement success as RPC broadcast only. Consume the pushed terminal
  status or recover it durably before claiming completion.
- Before leaving resting exposure unattended, arm an exact externally verified
  and pre-signed cancel-all ticket and maintain its SDK heartbeat. Lost
  heartbeats must fail closed into cancellation; disarm only through an
  explicit owner-authorized operation.
- Run the non-trading `order-slo` certification before making latency claims.
  It uses an authenticated nonce echo that cannot prepare, sign, submit, or
  cancel an order. Require both the controlled-latency and saturated-capacity
  gates to pass.
- Let the official SDK batch concurrent command and result frames. Agent code
  keeps calling the ordinary command methods; do not construct transport
  batches or infer shared results.

## Interpret safely

- Describe the response as one unified Sonar quote.
- Base explanations on the returned quote fields; do not invent a breakdown
  that is not present.
- Treat expiry and minimum output as hard constraints.
- Treat a disabled capability, unavailable market, contract mismatch, or expired
  quote as a stop condition.
- Recover any stream sequence gap from a fresh snapshot or durable status read.
- Never request or accept a private key, keypair, seed phrase, session secret,
  or production credential in a prompt.
- Never claim chain completion from preparation, signing, or the immediate
  broadcast receipt.

Read [references/public-contract.md](references/public-contract.md) when exact
field semantics, terminal commands, errors, or interface selection matter.
