# bconnTech Calculator — Project Notes

Last updated: 2026-09-05, end of session. Working tree is clean; everything below is committed and pushed.

## 1. Project purpose & architecture

Two standalone, single-file HTML calculators for a small business ("bconnTech"), built for a
non-technical shop owner (the user) to run on a phone, laptop, or shared as a link — no install,
no backend, no build step.

- **`calculator.html`** — the original piece. A pocket/desk "business calculator" (4-function +
  memory, markup/margin, tax add/remove, grand total), styled to look like a real handheld
  calculator. Built first; superseded in ambition by the file below but kept as-is and still
  shipped in the repo.
- **`pos-calculator.html`** (mirrored as **`index.html`**) — the current, actively developed app:
  a POS-style **"Shop Calculator"** with two modes (plain Calculator / full Sales register), a
  running sale ledger, printable receipts, and share-to-WhatsApp/Email/Slack/clipboard. This is
  what "the project" means in this doc unless stated otherwise.

**Architecture:** everything (HTML + CSS + JS) lives in one `.html` file per app. No framework,
no bundler, no `package.json`, no server, no database. State lives in in-memory JS variables
inside one IIFE and is persisted only via `localStorage` (per browser/device — never synced
anywhere). The whole thing runs identically as: a double-clicked local file, a GitHub Pages site,
or a Claude "Artifact" preview (with minor sandbox caveats, see §9).

**Why this shape:** the user asked, across the whole conversation, for something they could just
open and use — on their phone, on a laptop, shared as a link — with no setup. A single static
HTML file is the simplest thing that satisfies "runs everywhere, no install."

## 2. Technologies, frameworks, libraries, versions

- **Vanilla HTML/CSS/JS** — ES5-leaning syntax (`var`, function declarations, no modules/build
  step) inside one `(function () { "use strict"; ... })();` IIFE per file.
- **No frameworks, no npm, no dependencies, no package manager.**
- **Web Audio API** — hand-synthesised UI sounds (filtered noise-burst clicks + a two-tone sine
  chime). No audio files.
- **Google Fonts** (loaded via `<link>`, no download step):
  - `pos-calculator.html`: **Inter** (400/500/600/700/800) for UI, **JetBrains Mono**
    (400/500/700) for all digits/money.
  - `calculator.html`: **Barlow Semi Condensed** + **Share Tech Mono**.
- **CSS `color-mix()`** used throughout for tints — needs a modern browser (Chrome 111+, Safari
  16.4+, Firefox 113+). No fallback is defined for older browsers.
- **Hosting:** GitHub Pages (static, no Actions/build config — Pages serves the raw files from
  `main`).
- **Tooling used to build/verify this session** (not part of the shipped app): `gh` CLI
  (authenticated as `mgpvt`), git, and local headless Chrome
  (`C:\Program Files\Google\Chrome\Application\chrome.exe`) driven from PowerShell to screenshot
  and print-to-PDF the page during development, since there is no dev server or test runner.

## 3. Important files

| File | Purpose |
|---|---|
| `pos-calculator.html` | Source of truth for the Shop Calculator app. Edit this one. |
| `index.html` | **Byte-for-byte mirror** of `pos-calculator.html`, so GitHub Pages (which serves `index.html` at the repo root) shows the app at `/`. **Must be manually re-copied after every edit to `pos-calculator.html`** — see §9 and §12. |
| `calculator.html` | The earlier standalone pocket/business calculator. Independent of the two files above; not part of the current feature work. |
| `bconntech_logo.png` | Source logo (412 KB, 160×160-ish app-icon style: navy rounded square, glowing node/triangle graphic). Kept in the repo for reference, but **not** what's actually embedded in the pages — see the gotcha in §9. |
| `README.md` | Short public-facing description + the live link, shown on GitHub. |
| `CLAUDE.md` | This file. |

There is no `src/`, no build output, no config files (no `.env`, no `package.json`, no CI config).

## 4. "Database" — there isn't one; here's the local-storage schema instead

No server, no database. All persistence is `localStorage`, scoped per browser/device, written
directly by `pos-calculator.html`'s JS (see `TAX_KEY`/`MODE_KEY`/`SHOP_KEY`/`SOUND_KEY` near the
top of its `<script>`):

| Key | Values | Meaning |
|---|---|---|
| `bconntech.pos.tax` | number as string, e.g. `"8.5"` | Last committed Tax % in Sale Details. Survives **AC** (only reset by explicitly entering `0`). |
| `bconntech.pos.mode` | `"calc"` \| `"sales"` | User's mode preference. Only visibly matters on mobile (≤760px) — see §10. Defaults to `"calc"`. |
| `bconntech.pos.shop` | string, ≤42 chars | Shop name, editable any time in the bar under the header. Printed on the PDF receipt heading and prefixed to shared text/email subject. Defaults to empty → displays as "bconnTech". |
| `bconntech.pos.sound` | `"on"` \| `"off"` | UI click/confirm sound toggle. Defaults on. |

`calculator.html` (the older pocket calculator) has its own, separate keys:
`bconntech.taxrate` (persisted tax rate) and `bconntech.sound` (click-sound toggle).

None of this data is ever transmitted anywhere — it's read/written only on the visiting device.

## 5. "API endpoints" / integrations

No backend, so no REST/GraphQL endpoints. "Integrations" are all client-side share targets,
wired in `pos-calculator.html`'s Share Sale panel:

- **Email** — `mailto:?subject=...&body=...` (opens the OS/browser default mail client).
- **WhatsApp** — `https://wa.me/?text=...` (opens WhatsApp app or web with the receipt pre-filled).
- **Copy** — `navigator.clipboard.writeText()`, with a manual `document.execCommand("copy")`
  fallback via a hidden `<textarea>` if the Clipboard API is unavailable.
- **Share…** — `navigator.share()` (native OS share sheet — Slack, Save to Files, etc.). The
  button is only shown (`hidden` removed) if `navigator.share` exists.
- **Print / PDF** — fills a hidden `#receipt` element and calls `window.print()`; a
  `@media print` stylesheet hides the app and shows only the receipt, so "Save as PDF" from the
  print dialog produces a clean receipt document.

## 6. Environment variables

**None.** Fully static/client-side; there is nothing to configure and nothing to keep secret in
the app itself. (Unrelated to the app: this session's `gh` CLI session is authenticated to GitHub
as the user `mgpvt` via a token already stored in the local `gh` keyring — not part of the repo,
not something to write down here.)

## 7. Features completed (both apps, current state)

**`pos-calculator.html` (the active app):**
- Two modes: **Calc** (bare calculator) and **Sales** (full register), switchable via a header
  toggle. On desktop (>760px) both the Sale Details ledger and the Calculator are **always shown
  side by side**, regardless of the stored mode preference — the toggle only matters on mobile.
- **Sale Details ledger**: Qty / Price / Discount % / Tax % input rows, each tappable to make it
  the active keypad target; computed Subtotal / Discount Amount / Tax Amount / Total rows below,
  all aligned in one label/value column. Equal-height with the calculator panel on desktop.
- **Calculator**: twin LCD (Entry/Input on the left, Total/Result on the right, both auto-shrink
  font size in three size tiers so an 8-digit number never overflows or truncates), a Qty/Price/
  Discount/Tax quick-jump row, CE/⌫/±/% controls, and a 4×4 keypad (`7 8 9 ÷ …`). Values are
  capped at 8 digits (`MAX_VALUE = 99999999`); anything larger displays `ERROR`.
- **`=` is dual-purpose in Sales mode**: if there's a pending calculation it evaluates it first;
  if not, it commits the current line to the sale (same as pressing **Add to Sale**) — and the
  key turns green to signal this. On press, the result **flies from the display into its Current
  Sale row** (`flyResultToList()`): a pure-yellow (`#ffff00`) token in a plain dark navy pill —
  **no yellow border/halo around the pill itself**, only the digits glow (via `text-shadow`) —
  that pops big then glides (~1.3s total) down into place, with a brief highlight flash on
  landing. Scales up more on phones (`narrowMq.matches`: 2.3× base font / 1.7× pop / settles at
  0.7×) than on desktop (1.6× / 1.4× / 0.55×) so it reads at arm's length. Skips the animation
  under `prefers-reduced-motion`.
- **Current Sale list**: each line shows `n) qty × price (−disc% · +tax%)` plus **Subtotal / Tax /
  Total** in their own aligned columns under a sticky column header (stays aligned even when the
  list scrolls, via `scrollbar-gutter: stable`). Serial numbers (`1)`, `2)`, …) only appear once
  there's more than one item. Tapping a row loads it back into the fields for editing — the Add
  button becomes **Update Item**, with a Cancel option (a `Cancel` button on desktop, an
  "Editing #N · cancel" pill next to "Current Sale" on mobile, since the ledger itself is hidden
  there). Removing/undoing renumbers `editIndex` correctly.
- **Summary**: Subtotal / Total Tax / Grand Total cards, plus the grand total spelled out in
  cheque form ("Twelve thousand seven hundred sixteen and 78/100") below them.
- **Share Sale panel**: Email / WhatsApp / Copy / Share… / Print-PDF, all built from one
  formatted plain-text receipt (`receiptText()`) or one formatted HTML receipt
  (`fillReceiptHTML()`), both headed with the shop name and both showing the same per-item
  Subtotal/Tax/Total breakdown. The PDF adds a thin rule above a single "Totals" row (aligned to
  the item columns) and a thicker rule above Grand Total.
- **Shop name** field under the header, saved per device, shown on every receipt/share/PDF.
- **Sound toggle** (speaker icon next to the shop name field, reachable even in mobile Calc mode)
  — synthesised key-click and a rising two-note "confirm" chime on `=`/Add to Sale.
- **Mobile layout**: no swipe/carousel — the Sale Details screen was intentionally removed from
  mobile (see §10); Sales mode on mobile is one stacked screen (Calculator → Current Sale →
  Summary → Share).
- Light/dark theme aware (CSS custom properties, no manual toggle). Keyboard support for typing
  digits/operators; typing in the shop-name field doesn't leak into the calculator.

**`calculator.html` (pocket calculator, feature-frozen):**
Basic 4-function entry plus memory (MRC/M+/M-), Grand Total (GT), Markup/Margin (MU), Tax add/
remove (TAX+/TAX−) with a settable RATE (persisted), %, √, double-zero, sign toggle, number-to-
words readout, synthesised key-click sound with a toggle. Not being extended currently.

## 8. Features currently being worked on

**None.** The fly-to-list animation went through three follow-up refinement requests in a row
(slower/bigger/brighter overall → bigger + purer yellow specifically on mobile → drop the yellow
border/halo around the pill) and the last one has been implemented, verified, committed, and
deployed. There is no half-finished work in either file.

## 9. Known bugs / limitations / things to watch

- **`index.html` and `pos-calculator.html` must be kept in sync by hand.** There is no build step
  that generates one from the other. Every edit to `pos-calculator.html` must be followed by
  `cp pos-calculator.html index.html` before committing, or GitHub Pages (which serves
  `index.html`) will drift from the source of truth. (Every commit in this session's history did
  this — check `git diff` between the two files if in doubt.)
- **The logo is a pre-optimized, already-inlined base64 PNG (~53 KB of base64), not a fresh
  encoding of `bconntech_logo.png`** (which is 412 KB and would bloat the page). It was originally
  extracted from a small `<img>` in an early version of `calculator.html` and reused as-is. If the
  logo ever needs to change, re-optimize/resize the new image first (roughly 160×160, a few tens
  of KB) before base64-inlining it — don't inline the raw 412 KB file.
- **PowerShell + UTF‑8 gotcha (already hit once, fixed):** `Get-Content -Raw` in Windows
  PowerShell 5.1 does *not* read as UTF‑8 by default, so round-tripping the HTML file through
  PowerShell string replace + `[System.IO.File]::WriteAllText` **corrupts** the `−`/`×`/`·`
  characters used throughout (mojibake like `â€"`). When scripting edits or logo-substitution
  from Bash/PowerShell, either use the `Edit`/`Write` tools directly, or do text substitution in
  the **Bash** tool (`perl`/`sed`, which are byte-safe), never via `Get-Content`→PowerShell
  string→`WriteAllText`.
- **Inside the Claude "Artifact" preview sandbox**, `window.print()`, `navigator.share()`,
  clipboard access, and file downloads may be blocked or degraded by the iframe sandbox. They all
  work fully on the deployed GitHub Pages URL, the local file, and real mobile/desktop browsers —
  that's the environment these features were designed and tested for.
- **No automated tests, no linter, no CI.** All verification in this session was done by manual
  screenshotting/PDF-printing via headless Chrome (see §13) and visual review — there's no
  regression safety net for future changes.
- **No real-device testing performed** — the mobile layout, the sound toggle, and the fly-to-list
  animation have only been verified via headless Chrome window-size emulation, not on an actual
  phone. Headless Chrome was also observed to sometimes render at a wider virtual viewport than
  the requested `--window-size` and crop the screenshot to it — don't be fooled by a screenshot
  that looks "cut off"; check `document.documentElement.scrollWidth` vs `clientWidth` before
  concluding there's a real overflow bug (this happened once and cost a lot of back-and-forth).
- Browsers without `color-mix()` support will show broken/transparent tints in several places
  (buttons, tags, tinted panels) — no fallback colors are defined.
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
- **Mobile dropped the Sale Details screen entirely (no more swipe/carousel).** The user
  explicitly asked to avoid swiping. Rather than keep a two-screen carousel, Sales mode on mobile
  is now a single vertical stack (Calculator → Current Sale → Summary → Share); editing a line
  still works because the Calculator's Qty/Price/Discount/Tax buttons double as the editor, with a
  small "Editing #N · cancel" pill replacing the ledger's own Cancel button on mobile.
- **`=` doubles as Add to Sale (only when nothing is pending).** Requested explicitly. The
  branch in `equals()` evaluates a pending calculation first if there is one, and only commits the
  line when the entry is "settled" — so `=` remains a normal calculator key for in-field math
  (e.g. computing a price) as well as the "commit this sale line" gesture.
- **8-digit cap with tiered LCD shrinking instead of ellipsis.** A calculator that truncates its
  own numbers is unacceptable — so amounts step down through three font sizes to always show the
  whole number instead of cutting it off. `ERROR` only appears above the 8-digit ceiling.
- **Cheque-style amount-in-words ("...and NN/100")** was chosen over a currency-specific phrasing
  (no "dollars"/"rupees") because the app has no currency symbol anywhere and shouldn't assume
  one.
- **Serial numbers only shown once there's more than one item** — a single-item sale reads better
  without a redundant "1)".
- **Fly-to-list animation deliberately slow/large/bright, tuned twice already** — from an
  initial ~0.7s subtle version (too quick/small to register), to a slower/bigger global pass, to
  a mobile-specific size bump (phones scale the token up further than desktop, since it's read at
  arm's length) — because the point is to *feel* the item land in the sale, especially on a phone
  in a shop. The pill's box-shadow was later stripped down to a plain dark drop shadow (no yellow
  ring/halo around the pill) after the user found the yellow border distracting — only the digits
  themselves glow yellow now, via `text-shadow`, not the container.

## 11. Current task / status — exactly where we stopped

Clean stopping point. The fly-to-list animation had three refinement passes in a row (see §8);
the most recent removed the yellow border/glow-ring from around the pill so only the digits glow
— that change and this `CLAUDE.md` update are committed together in the commit you're reading
this from. `git status` is clean; `main` is pushed; GitHub Pages last build succeeded and served
HTTP 200.

- The commit containing this doc update is titled "Remove the yellow border/halo from the
  fly-to-list token" (or similar — check its message). The one immediately before it was
  `18d96b1` — "Bigger, brighter yellow fly-to-list token on mobile". **Don't trust either hash for
  long — run `git log -1` for the real current HEAD.**
- Repo: https://github.com/mgpvt/pos-calculator (public)
- Live site: https://mgpvt.github.io/pos-calculator/
- Claude Artifact for `pos-calculator.html` (private preview, same content as the last publish
  in-session): `https://claude.ai/code/artifact/b8ac173a-8651-44e9-a270-ee020f901148` — **there is
  a second, similarly-named artifact for the other file; see the disambiguation note in §9 before
  republishing either.**

No open questions are pending from the user.

## 12. Next steps to do after starting a fresh session

1. Re-read this file, then skim `pos-calculator.html` top-to-bottom once (it's ~1,900 lines but
   all in one place) before making changes — the whole app is state + render functions in one
   IIFE, so it's more useful to understand the flow (`render()`, `renderList()`, `applyMode()`,
   `addToSale()`) than to jump straight to a line number.
2. If the user reports a new bug or asks for a change: edit `pos-calculator.html` only, then
   **`cp pos-calculator.html index.html`** before committing (see §9's sync gotcha).
3. Verify changes visually before shipping — there's no test suite, so use headless Chrome
   screenshots (see §13) for both a desktop-width and a mobile-width (≤760px) render, and a
   `--print-to-pdf` render if the change touches the receipt/PDF.
4. Commit with a descriptive message (`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
   trailer per this repo's convention), `git push origin main`, then poll
   `gh api repos/mgpvt/pos-calculator/pages` until `"status":"built"` before telling the user it's
   live.
5. If updating the Claude Artifact too: republish with the same `file_path` (or pass the existing
   `url`) so it updates in place rather than creating a new artifact.
6. Ask the user before touching `calculator.html` (the pocket calculator) — it hasn't been part
   of the active feature work and no instructions have been given to change it.
7. Genuinely worth raising with the user at some point (not yet requested, so not done): a real
   on-device test pass (iPhone Safari + an Android phone) for the mobile layout, sounds, and the
   fly animation; and a small script or note to prevent `index.html`/`pos-calculator.html` drift.

## 13. Commands to run / test / deploy

There is no build, no dev server, no package manager, and no test runner. Everything is "open the
file" or "push and let Pages rebuild."

**Run locally** (Windows):
```powershell
Start-Process "e:\GEO-Programs\Claude\MyProject\3Dcalculator\pos-calculator.html"
```
or just double-click the file / open `calculator.html` the same way.

**Visual verification during development** (no test framework exists — this is the pattern used
throughout this session): headless Chrome screenshots and print-to-PDF, run from PowerShell or
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
`--print-to-pdf=out.pdf --no-pdf-header-footer` in place of `--screenshot=...` to check the
printed receipt. Note: headless Chrome sometimes renders at a wider internal viewport than
`--window-size` and only crops the screenshot to it — don't mistake that crop for a real
horizontal-overflow bug (see §9).

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
