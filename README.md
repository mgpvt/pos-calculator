# Shop Calculator

**POS. BILLING. SALES.** — a POS-style shop calculator by **bconnTech**. No backend, no build
step, works offline, and installs on a phone like an app.

**Live:** https://mgpvt.github.io/pos-calculator/

## Install on a phone or tablet

- **Android (Chrome):** open the link, then menu → *Install app* / *Add to Home screen*.
- **iPhone / iPad (Safari):** open the link, tap *Share* → *Add to Home Screen*.

After the first load it runs fully offline.

## What it does

- **Calc / Sales modes** — a plain calculator, or a full sale register. On wide screens both
  panels show side by side; on a phone there's a single stacked screen (no swiping) —
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
  (a proper itemised PDF receipt, generated on the device).
- **Sales history** — tap **Save sale** to record a finished sale and start a new one. Open the
  clock icon next to the currency to see saved sales, **daily totals**, and any **from / to date
  range** (Today, Yesterday, Last 7 days, This month, All). Export that range as a **PDF** or an
  **Excel** file (Summary, Daily totals, Sales and Items sheets). Sales are kept on the device for
  2 months and older ones are removed automatically.
- Tax % is remembered between sessions (kept through *AC* unless set to 0). Shop name, mode,
  sound and currency are remembered per device.
- Light/dark aware, keyboard support, synthesised key-click / confirm sounds (toggleable).

## Files

| File | |
|---|---|
| `index.html` / `pos-calculator.html` | the Shop Calculator app (byte-identical) |
| `manifest.webmanifest`, `sw.js`, `icons/` | installable-app setup (home-screen icon, offline cache) |
| `vendor/` | bundled PDF and Excel libraries and fonts, so nothing loads from the internet |
| `calculator.html` | the earlier standalone pocket calculator |

All data stays on the device (nothing is sent anywhere).
