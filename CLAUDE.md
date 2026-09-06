# bconnTech Calculator — Project Notes

**Session closed 2026-09-06.** Working tree is clean; everything in this file is committed and
pushed to `main`, and GitHub Pages is serving the current code. A fresh Claude Code session should
be able to pick up entirely from this file — no prior conversation needed.

## 1. Project purpose & architecture

Two standalone, single-file HTML calculators for a small business ("bconnTech"), built for a
non-technical shop owner (the user) to run on a phone, laptop, or shared as a link — no install,
no backend, no build step.

- **`calculator.html`** — the original piece. A pocket/desk "business calculator" (4-function +
  memory, markup/margin, tax add/remove, grand total), styled to look like a real handheld
  calculator. Built first; superseded in ambition by the file below but kept as-is and still
  shipped in the repo. **Feature-frozen** — no work has been done on it since the POS rebuild
  began, and none is planned unless the user asks.
- **`pos-calculator.html`** (mirrored as **`index.html`**) — the current, actively developed app:
  a POS-style **"Shop Calculator"** with two modes (plain Calculator / full Sales register), a
  running sale ledger, printable receipts, and share-to-WhatsApp/Email/clipboard/OS-share. This is
  what "the project" means in the rest of this doc unless stated otherwise.

**Architecture:** everything (HTML + CSS + JS) lives in one `.html` file per app. No framework, no
bundler, no `package.json`, no server, no database. State lives in in-memory JS variables inside
one `(function () { "use strict"; ... })();` IIFE and is persisted only via `localStorage` (per
browser/device — never synced anywhere). The whole thing runs identically as: a double-clicked
local file, a GitHub Pages site, or a Claude "Artifact" preview (with minor sandbox caveats, see
§9).

**Why this shape:** the user's ask, across the whole project, was for something they could just
open and use — on their phone, on a laptop, shared as a link — with no setup. A single static HTML
file is the simplest thing that satisfies "runs everywhere, no install."

## 2. Technologies, frameworks, libraries, versions

- **Vanilla HTML/CSS/JS** — ES5-leaning syntax (`var`, function declarations, no modules/build
  step) inside one IIFE per file.
- **No frameworks, no npm, no dependencies, no package manager.**
- **Web Audio API** — hand-synthesised UI sounds (filtered noise-burst clicks + sine-wave chimes).
  No audio files, no libraries.
- **Google Fonts** (loaded via `<link>`, no download step):
  - `pos-calculator.html`: **Inter** (400/500/600/700/800) for UI, **JetBrains Mono**
    (400/500/700) for all digits/money.
  - `calculator.html`: **Barlow Semi Condensed** + **Share Tech Mono**.
- **CSS `color-mix()`** used throughout for tints — needs a modern browser (Chrome 111+, Safari
  16.4+, Firefox 113+). No fallback is defined for older browsers.
- **Hosting:** GitHub Pages (static, no Actions/build config — Pages serves the raw files from
  `main`).
- **Tooling used to build/verify this project** (not part of the shipped app): `gh` CLI
  (authenticated as `mgpvt`), git, and local headless Chrome
  (`C:\Program Files\Google\Chrome\Application\chrome.exe`) driven from PowerShell to screenshot
  and print-to-PDF the page during development, since there is no dev server or test runner.

## 3. Important files

| File | Purpose |
|---|---|
| `pos-calculator.html` | Source of truth for the Shop Calculator app. Edit this one. |
| `index.html` | **Byte-for-byte mirror** of `pos-calculator.html`, so GitHub Pages (which serves `index.html` at the repo root) shows the app at `/`. **Must be manually re-copied after every edit to `pos-calculator.html`** — see §9 and §12. |
| `calculator.html` | The earlier standalone pocket/business calculator. Independent of the two files above; not part of the active feature work. |
| `bconntech_logo.png` | Source logo (412 KB, 160×160-ish app-icon style: navy rounded square, glowing node/triangle graphic). Kept in the repo for reference, but **not** what's actually embedded in the pages — see the gotcha in §9. |
| `README.md` | Short public-facing description + the live link, shown on GitHub. Kept in sync with actual behavior (last corrected alongside this file). |
| `CLAUDE.md` | This file. |

There is no `src/`, no build output, no config files (no `.env`, no `package.json`, no CI config).

## 4. "Database" — there isn't one; here's the local-storage schema instead

No server, no database. All persistence is `localStorage`, scoped per browser/device, written
directly by `pos-calculator.html`'s JS (see `TAX_KEY`/`MODE_KEY`/`SHOP_KEY`/`SOUND_KEY`/
`ITEMS_RECENT_KEY`/`ITEMS_COMMON_KEY` near the top of its `<script>`):

| Key | Values | Meaning |
|---|---|---|
| `bconntech.pos.tax` | number as string, e.g. `"8.5"` | Last committed Tax % in Sale Details. Survives **AC** (only reset by explicitly entering `0`). |
| `bconntech.pos.mode` | `"calc"` \| `"sales"` | User's mode preference. Only visibly matters on mobile (≤760px) — see §10. Defaults to `"calc"`. |
| `bconntech.pos.shop` | string, ≤42 chars | Shop name, editable any time in the bar under the header. Printed on the PDF receipt heading and prefixed to shared text/email subject. Defaults to empty → displays as "bconnTech". |
| `bconntech.pos.sound` | `"on"` \| `"off"` | UI click/confirm sound toggle. Defaults on. |
| `bconntech.pos.items.recent` | JSON array, ≤10 entries `{name, unit, qty, price, discount, tax}` | Last 10 distinct item names committed to a sale (most-recent first, by name, case-insensitive). Feeds the `#itemSuggestions` datalist and exact-match autofill. |
| `bconntech.pos.items.common` | JSON array, ≤5 entries `{name, unit, qty, price, discount, tax, count}` | Top 5 item names by usage count (independent ranking from `recent` — an old favorite stays listed even after 10 newer items have been added). Also feeds the datalist. |
| `bconntech.pos.currency` | one of the codes in the `CURRENCIES` table, e.g. `"USD"`, `"KWD"` | Selected currency, chosen from a dropdown in the shop bar. Drives money display/entry decimal places (see §7) — not a currency *symbol*, the app still shows none. Defaults to `"USD"` if unset or invalid. |

`calculator.html` (the older pocket calculator) has its own, separate keys:
`bconntech.taxrate` (persisted tax rate) and `bconntech.sound` (click-sound toggle).

None of this data is ever transmitted anywhere — it's read/written only on the visiting device.

## 5. "API endpoints" / integrations

No backend, so no REST/GraphQL endpoints. "Integrations" are all client-side share targets, wired
in `pos-calculator.html`'s Share Sale panel:

- **Email** — `mailto:?subject=...&body=...` (opens the OS/browser default mail client).
- **WhatsApp** — `https://wa.me/?text=...` (opens WhatsApp app or web with the receipt pre-filled).
- **Copy** — `navigator.clipboard.writeText()`, with a manual `document.execCommand("copy")`
  fallback via a hidden `<textarea>` if the Clipboard API is unavailable.
- **Share…** — `navigator.share()` (native OS share sheet — Slack, Save to Files, etc.). The
  button is only shown (`hidden` removed) if `navigator.share` exists.
- **Print / PDF** — fills a hidden `#receipt` element and calls `window.print()`; a `@media print`
  stylesheet hides the app and shows only the receipt, so "Save as PDF" from the print dialog
  produces a clean receipt document.

## 6. Environment variables

**None.** Fully static/client-side; there is nothing to configure and nothing to keep secret in
the app itself. (Unrelated to the app: the `gh` CLI used during this project is authenticated to
GitHub as the user `mgpvt` via a token already stored in the local `gh` keyring — not part of the
repo, not something to write down here.)

## 7. Features completed (both apps, current state)

**`pos-calculator.html` (the active app) — everything below is shipped, verified, and live:**

- Two modes: **Calc** (bare calculator) and **Sales** (full register), switchable via a header
  toggle. On desktop (>760px) both the Sale Details ledger and the Calculator are **always shown
  side by side**, regardless of the stored mode preference — the toggle only matters on mobile.
- **Sale Details ledger** (desktop only, see mobile note below): Qty / Price / Discount % / Tax %
  input rows, each tappable to make it the active keypad target; computed Subtotal / Discount
  Amount / Tax Amount / Total rows below, all aligned in one label/value column. Equal-height with
  the calculator panel.
- **Item name + Unit fields**: one row, just below the Qty/Price/Discount/Tax buttons — present in
  *both* the Sale Details panel and the Calculator panel (so it's there on mobile too, where Sale
  Details is hidden), all four inputs (2 name + 2 unit) kept in sync live. **Item name** is backed
  by a shared `<datalist id="itemSuggestions">` fed from two per-device `localStorage` lists (see
  §4): the last 10 distinct names used, and the top 5 by usage count. Typing (or picking a
  suggestion) that exactly matches a saved name (case-insensitive) autofills unit/qty/price/
  discount/tax from that item's last-used values. **Unit** (e.g. `kg`, `pcs`, `box`) is a narrow
  companion field next to it with a static `<datalist id="unitSuggestions">` of common units,
  appended to Qty everywhere it's displayed (`5 kg`) — on-screen fields, the Current Sale list,
  both receipt formats, and the PDF's Qty column — and saved per item alongside price/discount/tax.
  The item name itself flows through everywhere a line item shows up: bold above the qty×price
  line in the Current Sale list, its own line in the plain-text/WhatsApp/Email receipt (unnamed
  items keep the original compact single-line format), and its own **Item name** column in the
  printed/PDF receipt table (see below).
- **Calculator**: twin LCD (Entry/Input on the left, Total/Result on the right, both auto-shrink
  font size in three tiers so an 8-digit number never overflows or truncates), a Qty/Price/
  Discount/Tax quick-jump row, CE/⌫/±/% controls, and a 4×4 keypad (`7 8 9 ÷ …`). Values are capped
  at 8 digits (`MAX_VALUE = 99999999`); anything larger displays `ERROR`, and a red banner just
  below the calculator (`#calcErr`, both modes, both panels) explains why ("amount exceeds the
  maximum this calculator supports (99,999,999)"), clearing again once the values are fixed —
  driven by a `sawError` flag `money8()` sets whenever it has to return `"ERROR"`, checked once at
  the end of `render()`.
- **Adding/updating a sale line requires Qty > 0 and Price > 0, individually** (`addToSale()`) —
  not just a positive subtotal, which a negative Qty times a negative Price could otherwise satisfy
  while still being invalid.
- **`=` is dual-purpose in Sales mode**: if there's a pending calculation it evaluates it first; if
  not, it commits the current line to the sale (same as pressing **Add to Sale**) — and the key
  turns green to signal this. On press, the result **flies from the display into its Current Sale
  row** (`flyResultToList()`): a pure-yellow (`#ffff00`) token in a plain dark navy pill — no
  yellow border/halo around the pill itself, only the digits glow (via `text-shadow`) — that pops
  big then glides (~1.3s total) down into place, with a brief highlight flash on landing. Scales up
  more on phones (`narrowMq.matches`: 2.3× base font / 1.7× pop / settles at 0.7×) than on desktop
  (1.6× / 1.4× / 0.55×) so it reads at arm's length. Skips the animation under
  `prefers-reduced-motion`.
- **Current Sale list**: each line shows `n) qty × price (−disc% · +tax%)` plus **Subtotal / Tax /
  Total** in their own aligned columns under a sticky column header (stays aligned even when the
  list scrolls, via `scrollbar-gutter: stable`). Serial numbers (`1)`, `2)`, …) only appear once
  there's more than one item. Tapping a row loads it back into the fields for editing — the Add
  button becomes **Update Item**, with a Cancel option (a `Cancel` button on desktop, an "Editing
  #N · cancel" pill next to "Current Sale" on mobile, since the ledger itself is hidden there).
  Removing/undoing renumbers `editIndex` correctly.
- **Summary**: Subtotal / Total Tax / Grand Total cards, plus the grand total spelled out in
  cheque form ("Twelve thousand seven hundred sixteen and 78/100") below them.
- **Share Sale panel**: Email / WhatsApp / Copy / Share… / Print-PDF, all built from one formatted
  plain-text receipt (`receiptText()`) or one formatted HTML receipt (`fillReceiptHTML()`), both
  headed with the shop name (or the "Generated by bconnTech" fallback — see below). The PDF's item
  table has one row per line with **Sl.no / Item name / Qty / Subtotal / Discount / Tax / Total**
  columns: Sl.no center-aligned under its header; blank item name shows **NA**; discount/tax shown
  as their rate, "—" when zero; Qty includes the unit, e.g. "5 kg"; **Subtotal** shows the line's
  subtotal with a small "(qty × unit price)" breakdown beneath it, in place of a separate Unit
  Price column. The footer is one **Totals** row with Subtotal/Tax/Total each aligned under its own
  column, then a bold **Grand Total** row with a thick rule above it — same three numbers as the
  on-screen Summary cards.
- **Shop name** field under the header, saved per device, shown on every receipt/share/PDF.
  Falls back to **"Generated by bconnTech"** (not a bare "bconnTech") when left blank.
- **Currency selector** (a small dropdown in the shop bar, next to the sound toggle, visible in
  every mode including mobile Calc-only): 15 codes (USD, EUR, GBP, INR, AED, SAR, QAR, KWD, BHD,
  OMR, PKR, EGP, JPY, CAD, AUD), saved per device. Only changes *decimal places* actually used for
  money — 3 for KWD/BHD/OMR, 0 for JPY, 2 for everything else — for both display (`money()`,
  the cheque-style words' fraction, e.g. "...and 345/1000" for KWD) and entry (the keypad stops
  accepting further decimal digits once a money field — Price, or the plain Calculator's own
  result — has as many as the currency allows; JPY can't even start a decimal point). Qty/
  Discount/Tax are untouched by currency and stay at plain 2dp. **No currency symbol is shown
  anywhere** — this is decimal-precision correctness, not full currency formatting; the app's
  existing no-symbol design (see §10, cheque-style words) is unchanged.
- **Sound toggle** (speaker icon next to the shop name field, reachable even in mobile Calc mode)
  — synthesised key-click and a rising two-note "confirm" chime on `=`/Add to Sale.
- **Mobile layout**: no swipe/carousel — the Sale Details screen was intentionally removed from
  mobile entirely (see §10); Sales mode on mobile is one stacked screen (Calculator → Current Sale
  → Summary → Share). The calculator's own Qty/Price/Discount/Tax buttons double as the line
  editor there.
- Light/dark theme aware (CSS custom properties, no manual toggle). Keyboard support for typing
  digits/operators; typing in the shop-name field doesn't leak into the calculator.

**`calculator.html` (pocket calculator, feature-frozen):** basic 4-function entry plus memory
(MRC/M+/M-), Grand Total (GT), Markup/Margin (MU), Tax add/remove (TAX+/TAX−) with a settable RATE
(persisted), %, √, double-zero, sign toggle, number-to-words readout, synthesised key-click sound
with a toggle.

## 8. Features currently being worked on

**None. The session is closed with no open or half-finished work.** The last thread of work was:
Qty/Price > 0 validation, the `#calcErr` reason banner below the calculator, the "Generated by
bconnTech" shop-name fallback, and the PDF's Subtotal-column/aligned-Totals rework (see §7) — all
implemented, verified (CDP-driven test of the validation rejection, the error banner appearing and
clearing, the new PDF layout, plus desktop/mobile screenshots), committed, and deployed. The
browser's own print header/footer (showing the source URL) was also raised this session — see the
dedicated §9 entry for why that one can't be fixed in code.

## 9. Known bugs / limitations / things to watch

- **`index.html` and `pos-calculator.html` must be kept in sync by hand.** There is no build step
  that generates one from the other. Every edit to `pos-calculator.html` must be followed by
  `cp pos-calculator.html index.html` before committing, or GitHub Pages (which serves
  `index.html`) will drift from the source of truth. Every commit in this project's history did
  this — check `git diff pos-calculator.html index.html` if in doubt (should be empty).
- **The logo is a pre-optimized, already-inlined base64 PNG (~53 KB of base64), not a fresh
  encoding of `bconntech_logo.png`** (which is 412 KB and would bloat the page). It was originally
  extracted from a small `<img>` in an early version of `calculator.html` and reused as-is. If the
  logo ever needs to change, re-optimize/resize the new image first (roughly 160×160, a few tens of
  KB) before base64-inlining it — don't inline the raw 412 KB file.
- **PowerShell + UTF‑8 gotcha (already hit once, fixed):** `Get-Content -Raw` in Windows
  PowerShell 5.1 does *not* read as UTF‑8 by default, so round-tripping the HTML file through
  PowerShell string replace + `[System.IO.File]::WriteAllText` **corrupts** the `−`/`×`/`·`
  characters used throughout (mojibake like `â€"`). When scripting edits or logo-substitution from
  Bash/PowerShell, either use the `Edit`/`Write` tools directly, or do text substitution in the
  **Bash** tool (`perl`/`sed`, which are byte-safe) — never via `Get-Content` → PowerShell string →
  `WriteAllText`.
- **Inside the Claude "Artifact" preview sandbox**, `window.print()`, `navigator.share()`,
  clipboard access, and file downloads may be blocked or degraded by the iframe sandbox. They all
  work fully on the deployed GitHub Pages URL, the local file, and real mobile/desktop browsers —
  that's the environment these features were designed and tested for.
- **No automated tests, no linter, no CI.** All verification was manual: screenshotting/PDF-printing
  via headless Chrome (see §13) plus visual review. There's no regression safety net for future
  changes.
- **The printed page's own browser header/footer (showing the source URL/file path and date) is
  not something this app's code can remove.** The user asked for this once; it's the browser
  print dialog's own "Headers and footers" option (under "More settings"), which exists so a page
  can't hide from the person printing it where the content came from — there is no CSS/JS API a
  page can use to disable it. The fix is on the user's/shop's end: uncheck "Headers and footers"
  in the print dialog once (Chrome remembers the setting for future prints). The receipt's own
  `<p class="r-foot">Generated by bconnTech Calculator</p>` is what's guaranteed to print
  regardless of that setting — don't try to "fix" this again in code without re-confirming the
  browser actually gained a way to control it.
- **Headless Chrome can be driven interactively via CDP, not just screenshotted at load.** This
  environment has Python's `websocket-client` installed, so beyond the static
  `--screenshot`/`--print-to-pdf` flags, you can launch
  `chrome.exe --headless=new --remote-debugging-port=9333 --remote-allow-origins=* --user-data-dir=<scratch dir>`,
  open a tab with `PUT http://localhost:9333/json/new?<file-url>` (must be `PUT`, not `GET`), then
  speak CDP over the returned `webSocketDebuggerUrl` (`Runtime.evaluate` to click buttons/type into
  fields/read `localStorage`, `Emulation.setDeviceMetricsOverride` for viewport,
  `Emulation.setEmulatedMedia:{media:"print"}` + a real click on the Print/PDF button — not a bare
  reference to the page's closure-scoped `fillReceiptHTML`, which is invisible to
  `Runtime.evaluate` and throws — to render the print stylesheet, `Page.captureScreenshot` to save
  a PNG). This was used this session to actually exercise the Item Name autofill/storage logic
  end-to-end (not just eyeball the layout) and is worth reaching for again whenever a change is
  behavioral, not just visual. Stub `window.print = function(){}` before clicking Print/PDF so it
  doesn't hang. **After editing the file, there's no need to relaunch Chrome** — `GET
  http://localhost:9333/json/list` finds the still-open tab, then `Page.reload` (or
  `Page.navigate` to the same file URL) on that tab's `webSocketDebuggerUrl` picks up the edit,
  same as a normal browser refresh; only kill and relaunch chrome.exe once, at the very end of a
  verification session.
- **A `�` in this tool's own captured command output does not mean the app mangled a character.**
  Printing non-ASCII (×, −, —, ·) through this Windows shell to the harness can itself mangle the
  *display* of otherwise-correct UTF-8; before concluding the app corrupted a character, verify by
  writing the value to a file with explicit `encoding="utf-8"` and inspecting bytes/codepoints (or
  screenshot it) rather than trusting the printed terminal text.
- **No real-device testing performed** — the mobile layout, the sound toggle, and the fly-to-list
  animation have only been verified via headless Chrome window-size emulation, not an actual phone.
  Two headless-Chrome quirks to remember when verifying future changes:
  - It sometimes renders at a wider internal viewport than the requested `--window-size` and only
    crops the screenshot to it — don't mistake that crop for a real horizontal-overflow bug; check
    `document.documentElement.scrollWidth` vs `clientWidth` before concluding there's one.
  - `--virtual-time-budget` (used to force a screenshot at a specific point in time) is **not**
    reliable for catching a CSS `transition` mid-flight — the same script/timing combo captured the
    flying yellow token clearly in one run and showed nothing on an otherwise-identical rerun.
    When verifying a CSS-animation tweak, prefer a static isolated-HTML swatch of the "at rest"
    styling (font-size, color, shadows) over trying to screenshot the motion itself.
- Browsers without `color-mix()` support will show broken/transparent tints in several places
  (buttons, tags, tinted panels) — no fallback colors are defined.
- **`.carousel`'s grid columns must stay `minmax(0, 1fr) 242px`, not bare `1fr 242px`.** A bare
  `1fr` track can't auto-shrink below the automatic minimum (content min-width) of whatever's in
  it — so adding almost anything to the Sale Details panel that itself can't shrink past some
  width (a fixed-width sibling in a nested flex row, an un-ellipsized label, etc.) can silently
  force the whole `.carousel` wider than `.app`'s 500px `max-width`, which `.app`'s own
  `overflow-x: clip` then slices off the right edge of — invisibly, since `getBoundingClientRect()`
  still reports the (wrong) unclipped geometry and nothing errors. This actually happened when the
  Qty unit field was added (an extra fixed-width sibling next to Item name) and was only caught by
  screenshotting, not by the CDP functional checks. If a future change to the Sale Details panel's
  content produces a similarly cropped-looking screenshot, check `.panel-calc`'s
  `getBoundingClientRect().right` against `.app`'s — if the former exceeds the latter, this is the
  bug, and the fix is always `minmax(0, ...)`, never a bigger `.app` max-width or removing the clip.
- **Possible pre-existing cosmetic issue, not yet confirmed or fixed:** a 390px-wide mobile
  screenshot taken this session showed the Current Sale list's sticky column header rendering
  "SUBTOTALTAX" with no gap between the two words (`.salelist__cols` in the CSS). Not touched or
  introduced by this session's item-name work — noticed only incidentally in a screenshot at that
  exact width. Worth a look next time the mobile ledger header is on screen, but not investigated
  further since it's outside what was asked.
- **Two different Claude Artifacts share the exact title "bconnTech Calculator"** — don't confuse
  them (`Artifact` → `action: "list"` shows both):
  - `https://claude.ai/code/artifact/b8ac173a-8651-44e9-a270-ee020f901148` (favicon 🛒) is
    **`pos-calculator.html`** — the active app, most recently updated.
  - `https://claude.ai/code/artifact/01d7bd16-8fd4-4bb0-894d-e0acf1acca41` (favicon 🔢) is the
    **older `calculator.html`** pocket calculator, published earlier and not touched since.
  Republishing to update one **must** pass that artifact's own `url`, or it creates a third,
  disconnected artifact instead of updating either.

## 10. Important decisions and why

- **One HTML file per app, no framework.** The user's ask was always "something I can open/share
  and just use" (phone, laptop, a link) — a static file satisfies that with zero setup and works
  identically as a local file, a Pages site, or an Artifact.
- **`localStorage`, not a backend.** Shop name / tax rate / mode / sound are "this device's
  settings," not shared data — no sync was ever requested, so no backend was introduced.
- **Desktop always shows both panels; mobile's Calc/Sales toggle only matters there.** Early on,
  Calc mode hid the Sale Details/summary/list *everywhere*, which the user flagged as data going
  missing on the web. Fixed by making `emode()` fall back to `"sales"` behavior whenever the
  viewport is wide (`window.matchMedia("(max-width: 760px)")`), so the stored `"calc"` preference
  only ever produces the calculator-only view on a phone.
- **Mobile dropped the Sale Details screen entirely (no more swipe/carousel).** The user explicitly
  asked to avoid swiping. Rather than keep a two-screen carousel, Sales mode on mobile is now a
  single vertical stack (Calculator → Current Sale → Summary → Share); editing a line still works
  because the Calculator's Qty/Price/Discount/Tax buttons double as the editor, with a small
  "Editing #N · cancel" pill replacing the ledger's own Cancel button on mobile.
- **`=` doubles as Add to Sale (only when nothing is pending).** Requested explicitly. The branch
  in `equals()` evaluates a pending calculation first if there is one, and only commits the line
  when the entry is "settled" — so `=` remains a normal calculator key for in-field math (e.g.
  computing a price) as well as the "commit this sale line" gesture.
- **8-digit cap with tiered LCD shrinking instead of ellipsis.** A calculator that truncates its own
  numbers is unacceptable — so amounts step down through three font sizes to always show the whole
  number instead of cutting it off. `ERROR` only appears above the 8-digit ceiling.
- **Cheque-style amount-in-words ("...and NN/100")** was chosen over a currency-specific phrasing
  (no "dollars"/"rupees") because the app has no currency symbol anywhere and shouldn't assume one.
  Adding the currency selector didn't change this — the fraction denominator now correctly follows
  the selected currency's decimal places (.../1000 for a 3-decimal currency), but no symbol or
  currency name was added to the phrase itself.
- **Currency selector changes decimal places only, never adds a symbol.** The ask was specifically
  about "the decimal point" being correct per currency (2 vs 3 vs 0 places) — not full currency
  formatting. Keeping the app symbol-free everywhere (as it always has been) means this feature is
  additive/low-risk: existing receipts, the words phrase, and every screen still read exactly as
  before for a 2-decimal currency (the default, USD), and only genuinely gain precision for
  KWD/BHD/OMR (3dp) or lose a decimal point entirely for JPY (0dp).
- **`entryDecimals()` distinguishes money fields (Price, the plain-Calculator result) from
  Qty/Discount/Tax**, which stay at plain 2dp regardless of currency — qty and percentages aren't
  money amounts, so there's no reason a 3-decimal currency should suddenly let you type "3.456" kg
  or "8.25%" further out than before. Only fields that actually hold a currency amount follow the
  selected currency's own precision.
- **Serial numbers only shown once there's more than one item** — a single-item sale reads better
  without a redundant "1)".
- **Item name is a plain `<input>`, not routed through the numeric buffer/`activeField` system**
  that Qty/Price/Discount/Tax use. Free-text product names need a real keyboard, not the calculator
  keypad, so it's wired independently: `input` events write straight to `line.name` and mirror the
  *other* copy of the field (Sale Details panel vs. Calculator panel each have their own `<input
  class="itemname">`, kept in sync so either can be used depending on which panel is visible).
  `render()` only overwrites a field's `.value` when it isn't `document.activeElement`, so it never
  fights the one currently being typed into.
- **Autofill triggers on exact case-insensitive name match, not on every keystroke.** "Fill the
  rest" only fires once what's typed matches a saved item's name exactly (typing further past a
  match, e.g. continuing to type after a match, simply stops re-triggering it) — picking a
  `<datalist>` suggestion produces the same exact-match `input` event, so it works both ways.
  Qty *and* price/discount/tax are all overwritten from the saved record on a match, since the ask
  was explicitly to "fill the rest," not just the price.
- **Two separate localStorage lists (`recent`, capped 10; `common`, capped 5) rather than one**,
  matching the user's own wording — an item used often in the past but not recently would fall out
  of a single MRU-only list; keeping a frequency-ranked list alongside it means an old favorite
  stays suggested.
- **Unit is a separate narrow field next to Item name, not folded into the Qty button itself.**
  Qty's own numeric entry is driven by the shared buffer/`activeField` keypad system, which isn't a
  good fit for free-text like `kg`; and the Qty/Price/Discount/Tax buttons are already a fixed
  4-column grid with no room for a 5th cell. Placing Unit beside Item name (both plain, independent
  `<input>`s) keeps the keypad grid untouched and reads naturally as "what am I selling, and in
  what unit" on one line. Its datalist is a small static curated list (no separate per-device
  storage) since the per-item template already remembers whatever unit was last used for a named
  item — a second learned list wasn't worth the added complexity.
- **PDF's Sl.no column center-aligned, matching its header** — it was previously right-aligned
  (`class="num"`, shared with the money columns) while its `<th>` used the table's default
  left-align, so the numbers didn't sit under the word "Sl.no" at all. Given its own `.ctr` class
  now, used for both the header and body cells.
- **Fly-to-list animation deliberately slow/large/bright, tuned across three passes** — from an
  initial ~0.7s subtle version (too quick/small to register), to a slower/bigger global pass, to a
  mobile-specific size bump (phones scale the token up further than desktop, since it's read at
  arm's length) — because the point is to *feel* the item land in the sale, especially on a phone
  in a shop. The pill's box-shadow was finally stripped down to a plain dark drop shadow (no yellow
  ring/halo around the pill) after the user found the yellow border distracting — only the digits
  themselves glow yellow now, via `text-shadow`, not the container. This is considered done; no
  further passes are expected unless the user asks.

## 11. Current task / status — exactly where we stopped

**The session is being closed intentionally, at a clean stopping point.** All requested work is
implemented, verified, committed, and deployed:

- `git status` is clean; `main` is pushed; GitHub Pages last build succeeded and served HTTP 200
  at the moment this was written.
- `pos-calculator.html` and `index.html` are byte-identical.
- The last app-code commit was **"Validate qty/price, show error reasons, rework PDF
  Subtotal/Totals"** (hash `0b58cbf` as of this writing); this `CLAUDE.md` update is committed
  immediately after it as a documentation-only follow-up. **Run `git log -1` for the true current
  HEAD — any hash printed in this file is a snapshot, not a promise.**
- Repo: https://github.com/mgpvt/pos-calculator (public)
- Live site: https://mgpvt.github.io/pos-calculator/
- Claude Artifact for `pos-calculator.html` (private preview):
  `https://claude.ai/code/artifact/b8ac173a-8651-44e9-a270-ee020f901148` — **not republished this
  session**, so it no longer reflects the Item Name feature above; it still shows whatever was last
  published there. Republish with that same `url` (see §12 step 5) if the user wants the Artifact
  preview current too. There is a second, similarly-titled artifact for the other file; see the
  disambiguation note in §9 before republishing either.

**No open questions are pending from the user.** There is nothing mid-flight to resume — the next
session starts fresh on whatever the user asks for next.

## 12. Next steps to do after starting a fresh session

1. Re-read this file, then skim `pos-calculator.html` top-to-bottom once (it's ~1,900 lines but all
   in one place) before making changes — the whole app is state + render functions in one IIFE, so
   it's more useful to understand the flow (`render()`, `renderList()`, `applyMode()`,
   `addToSale()`, `flyResultToList()`) than to jump straight to a line number.
2. If the user reports a new bug or asks for a change: edit `pos-calculator.html` only, then
   **`cp pos-calculator.html index.html`** before committing (see §9's sync gotcha).
3. Verify changes visually before shipping — there's no test suite, so use headless Chrome
   screenshots (see §13) for both a desktop-width and a mobile-width (≤760px) render, and a
   `--print-to-pdf` render if the change touches the receipt/PDF. For animation/motion tweaks,
   prefer a static isolated-HTML swatch over trying to screenshot the transition itself (see §9).
4. Commit with a descriptive message (`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
   trailer per this repo's convention), `git push origin main`, then poll
   `gh api repos/mgpvt/pos-calculator/pages` until `"status":"built"` before telling the user it's
   live.
5. If updating the Claude Artifact too: republish with the same `file_path` (or pass the existing
   `url`) so it updates in place rather than creating a new artifact — and double-check you're
   passing the `pos-calculator.html` artifact's URL, not the pocket calculator's (see §9).
6. Ask the user before touching `calculator.html` (the pocket calculator) — it hasn't been part of
   the active feature work and no instructions have been given to change it.
7. Genuinely worth raising with the user at some point (not yet requested, so not done): a real
   on-device test pass (iPhone Safari + an Android phone) for the mobile layout, sounds, and the
   fly animation; and a small script or note to prevent `index.html`/`pos-calculator.html` drift
   automatically (e.g. a pre-commit hook) rather than relying on memory.

## 13. Commands to run / test / deploy

There is no build, no dev server, no package manager, and no test runner. Everything is "open the
file" or "push and let Pages rebuild."

**Run locally** (Windows):
```powershell
Start-Process "e:\GEO-Programs\Claude\MyProject\3Dcalculator\pos-calculator.html"
```
or just double-click the file / open `calculator.html` the same way.

**Visual verification during development** (no test framework exists — this is the pattern used
throughout this project): headless Chrome screenshots and print-to-PDF, run from PowerShell or
Bash. Example (desktop width):
```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Start-Process -FilePath $chrome -ArgumentList @(
  '--headless','--disable-gpu','--hide-scrollbars',
  '--screenshot=C:\path\to\out.png','--window-size=980,780',
  'file:///e:/GEO-Programs/Claude/MyProject/3Dcalculator/pos-calculator.html'
) -Wait -WindowStyle Hidden
```
Repeat with `--window-size` ≤760 width for the mobile layout, and
`--print-to-pdf=out.pdf --no-pdf-header-footer` in place of `--screenshot=...` to check the printed
receipt. See §9 for the two headless-Chrome quirks to watch for (viewport cropping, and
unreliable mid-transition capture with `--virtual-time-budget`).

**Sync the two HTML files** (do this before every commit that touches `pos-calculator.html`):
```bash
cp pos-calculator.html index.html
```

**Commit & deploy:**
```bash
git add -A
git commit -m "Describe the change

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
git push origin main
```

**Check GitHub Pages build status** (the `gh` CLI is already authenticated as `mgpvt`):
```bash
gh api repos/mgpvt/pos-calculator/pages
# poll until the JSON shows "status":"built"
curl -s -o /dev/null -w "%{http_code}\n" -L https://mgpvt.github.io/pos-calculator/
```

**No env vars, no secrets, nothing to install.**
