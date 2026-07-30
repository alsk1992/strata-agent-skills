---
name: strata
description: Explore Strata markets and request validated Sonar quotes through the official MCP server or terminal SDK. Use when an agent needs to inspect live Strata capabilities, discover quote-ready markets, compare buy or sell economics, reason about token-atomic amounts, or explain a Sonar quote without exposing private liquidity or matching composition.
---

# Strata

Use Strata's public, capability-driven interfaces to inspect markets and request
read-only Sonar quotes. Treat Sonar as the product-level liquidity and matching
system; never infer or reveal its internal composition.

## Choose an interface

1. Prefer the configured Strata MCP tools.
2. Otherwise use `npx -y @stratabook/sdk` from a terminal.
3. Use a language SDK only when writing or changing application code.

Do not call undocumented HTTP paths or reconstruct private behavior.

## Request a quote

1. Read capabilities first. Proceed only when the required public read
   capability is currently enabled.
2. List markets and select a market marked ready.
3. Resolve the side, exact input amount in token atoms, and slippage tolerance.
   Ask the user when any of these are ambiguous.
4. Request the Sonar quote.
5. Check that the response binds to the selected market, side, and input amount.
6. Report output atoms, consumed input atoms, fees by asset side, minimum output,
   price impact, and remaining validity.

Never silently convert a human token amount without confirmed token decimals.
Preserve every atomic amount as a base-10 string.

## Interpret safely

- Describe the result as a Sonar quote across the complete eligible market.
- Do not speculate about routes, venues, liquidity layers, matching order, or
  private infrastructure.
- Treat expiry and minimum output as hard constraints.
- Treat a disabled capability, unavailable market, contract mismatch, or expired
  quote as a stop condition.
- Never request or accept a wallet, private key, keypair, seed phrase, session
  key, or production credential.
- Never claim that this read-only release prepared, signed, or submitted a
  transaction.

Read [references/public-contract.md](references/public-contract.md) when exact
field semantics, terminal commands, errors, or interface selection matter.
