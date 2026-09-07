# bconnTech Calculator

A single-file **POS-style shop calculator** — no install, no backend, no build step.

**Live:** https://mgpvt.github.io/pos-calculator/

## What it does

- **Calc / Sales modes** — a plain calculator, or a full sale register. On the web both
  panels always show side by side; on mobile there's a single stacked screen (no swiping) —
  the Calc/Sales toggle there switches between just the calculator and the full register.
- **Sale ledger** — Qty × Price, minus a per-item Discount (as a **%** or a **flat amount**,
  your choice per line), plus Tax %, giving Subtotal, Discount Amount, Tax Amount and Total.
- **Twin display** — the left LCD is a big Unit Price readout; the right shows the running line
  Total. An 8-digit display that auto-fits large comma-formatted numbers.
- **Item name + unit** per line, with per-device autocomplete (recent + most-used items) that
  fills in price/discount/tax when you pick a saved name. Units like `kg`, `pcs`, `box`.
- **Current Sale** — add lines to the sale; tap any line to load it back and edit it.
- **Overall Discount** — one flat amount knocked off the whole sale's grand total.
- **Summary** — running Subtotal, Total Tax and Grand Total, with the grand total spelled
  out in cheque form ("… and 24/100").
- **Currency** — pick from 15 codes; decimals and the symbol/code follow your choice.
- **Share a receipt** — Email, WhatsApp, copy as text, the OS share sheet, or **Download PDF**
  (a proper itemised PDF receipt, generated in the browser).
- Tax % is remembered between sessions (kept through *AC* unless set to 0). Shop name, mode,
  sound and currency are remembered per device.
- Light/dark aware, keyboard support, synthesised key-click / confirm sounds (toggleable).

## Files

| File | |
|---|---|
| `index.html` / `pos-calculator.html` | the POS calculator (byte-identical) |
| `calculator.html` | the earlier standalone pocket calculator |
| `bconntech_logo.png` | source logo (inlined as a data URI in the pages) |

Open any HTML file directly in a browser — there is no build step. The PDF receipt pulls jsPDF
from a CDN the first time a browser loads the page; everything else is self-contained, and all
data stays on the device (nothing is sent anywhere).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
