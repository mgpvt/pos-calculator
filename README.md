# bconnTech Calculator

A single-file, dependency-free **POS-style shop calculator**.

**Live:** https://mgpvt.github.io/pos-calculator/

## What it does

- **Calc / Sales modes** — a plain calculator, or a full sale register. On the web both
  panels always show side by side; on mobile there's a single stacked screen (no swiping) —
  the Calc/Sales toggle there switches between just the calculator and the full register.
- **Sale ledger** — Qty × Price, minus Discount %, plus Tax %, giving Subtotal, Discount
  Amount, Tax Amount and Total, all in one aligned column.
- **Current Sale** — add lines to the sale; tap any line to load it back and edit it.
- **Summary** — running Subtotal, Total Tax and Grand Total, with the grand total spelled
  out in cheque form ("… and 24/100").
- **8-digit display** that auto-fits large comma-formatted totals.
- Tax % is remembered between sessions (kept through *AC* unless set to 0).
- Twin LCD, pocket-calculator styling, light/dark aware, keyboard support.

## Files

| File | |
|---|---|
| `index.html` / `pos-calculator.html` | the POS calculator (identical) |
| `calculator.html` | the earlier standalone pocket calculator |
| `bconntech_logo.png` | source logo (inlined as a data URI in the pages) |

Open any HTML file directly in a browser — there is no build step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
