# Website Codebase — Claude Code Instructions

**Repo:** ~/websites/mcg-site/ → GitHub → Netlify auto-deploy
**Site:** coyne-green.com

---

## SESSION RULES

1. **Compaction safety:** Before any git operation, run `find .git -name "*.lock" -delete`. Plan commit points up front. Commit in batches of ≤8 files. If context is running low, commit what you have, push, report progress, stop cleanly.
2. **Copy is sacred:** Never invent, paraphrase, or "improve" copy. Use approved text verbatim. If copy isn't provided, ask.
3. **Read before writing:** Read the target file before editing. Read this file before every session.
4. **3-strike rule:** If the same fix fails 3 times, stop. The approach is wrong.
5. **Screenshot after visual changes:** Playwright at 390, 768, 1440 after any visual edit.
6. **No file opening:** Do NOT open files, folders, or Finder windows. Print filepaths as text.
7. **No autonomous actions:** Present the plan, wait for approval, then execute. Never make changes without explicit go-ahead.

---

## ACTIVE PAGES (11)

| URL | File | Notes |
|-----|------|-------|
| `/` | index.html | Homepage |
| `/topfloor` | topfloor.html | Top Floor pitch |
| `/kanvatan` | kanvatan.html | Kan Vatan pitch |
| `/about` | about.html | Career timeline |
| `/tfgame` | tfgame.html | Top Floor game (hidden) |
| `/meatspace` | meatspace.html | Meatspace |
| `/artci` | artci.html | Artçı |
| `/altindamarlari` | altindamarlari.html | Altın Damarları |
| `/losingreality` | losingreality.html | Losing Reality |
| `/turkiye` | turkiye.html | Turkish portfolio (bilingual) |
| `/secret` | secret.html | Kinnikuman treatment (hidden) |
| `/imposter` | imposter.html | Imposter Syndrome one-pager (hidden) |

"All pages" = ALL of these.

**HR standalone pages retired (2026-09-10):** `hr.html`, `hr-deep.html`, `hr-slideshow.html`, `hr-trailer.html`, `hr-watch.html` are gone — HR now lives entirely at hrthefilm.com. `_redirects` already 301s every one of their old routes (`/hr`, `/hr/deep`, `/hr/characters`, `/hr-short`, `/hr-trailer`, etc.) to the matching hrthefilm.com page, so old links/bookmarks still work. The Work dropdown's Human Resource link points straight at `https://hrthefilm.com` (external, `target="_blank"`) on every remaining page, skipping the redirect hop — same pattern index.html always used.

---

## HOMEPAGE STRUCTURE (updated 2026-09-10)

index.html body is: nav → hero → five full-bleed panels → footer. Nothing else lives between hero and footer.

Panel order: `.hr` (Human Resource) → `.tf` (Top Floor) → `.kv` (Kan Vatan) → `.about` → `.connect` (Contact).

- **No buttons.** None of the five panels use `.btn`/`.btn-primary`/`.btn-row`. Each panel is a single full-panel `<a class="panel-link">` (the whole panel is the link) with a `.cta` label that's hidden by default and revealed on hover (desktop) — on mobile (`≤860px`) the `.cta` is always visible instead, since there's no hover. Captions: `.hr` = "View Site" (it links out to hrthefilm.com, not an in-repo project page), `.tf`/`.kv` = "View Project". The `.about` panel has no `.cta` and no eyebrow label anymore — just the photo, name, subtitle, and bio paragraph.
- **Hero name (`<h1>MAX COYNE-GREEN</h1>`) is plain text, not a link.** It used to link to `/about`; that was removed.
- **`.hr` and `.kv`:** background image bleeds on one side (`.hr-img` right, `.kv-img` left), text sits in `.wrap .txt` on the other side. `.hr` text is left-aligned, `.kv` text is right-aligned.
- **`.hr` mobile/tablet is a one-sheet, not a scaled-down desktop layout.** Below 861px the still fills the card with the text block lower-left; below 600px the still becomes a 104vw frame with the title pulling up over its bottom edge, logline and laurels stacked below. The mobile hero only ever shows its first slide (`hr_hero_new.webp`, the empty office) — the rest of the slideshow rotation is suppressed below 861px so it doesn't compete with the HR card's own still right after it.
- **`.tf` (Top Floor) is a flat image card, not built from HTML/CSS.** `images/tf_card.webp` is a pre-designed 1920×1080 card (title, tagline, art all baked into the image) — `.tf-card-img` just displays it at 16:9. Don't rebuild the card's title/tagline as HTML text.
- **`images/hero_slide_07.webp`** is reserved for the `.hr` panel background (`.hr-img`) — it was removed from the hero slideshow rotation to avoid it appearing twice.
- **`images/kv_keyart.webp`** is a generated crop/grade of `images/img_41.webp` (see git history for the exact Pillow transform) — regenerate from that source if it needs updating, don't hand-edit the webp.
- A generic `section { padding:100px 0; opacity:0; transform:translateY(30px); }` rule (site-wide scroll-reveal fade-in) still applies to all five panels since they're `<section>` elements. A `.hr,.tf,.kv{padding:0}` override neutralizes the padding specifically for the three full-bleed panels (`.about`/`.connect` already override padding themselves) — don't remove that override without re-checking panel heights.
- **Desktop-only scroll-snap:** at `min-width:861px` and `min-height:700px`, `.hero`/`.hr`/`.tf`/`.kv`/`.about` snap to each panel on scroll (`scroll-snap-type:y proximity`). Both conditions must hold — a short window (e.g. 1440×600) or any mobile width falls back to normal scrolling, since snapping traps the page on short viewports.
- Design source files (sketches, mockup HTML, unconverted PNGs) live in `design/`, which is gitignored — never expect those to be deployed; only the converted `.webp` in `images/` ships.

---

## LEGACY SPA ROUTES (DO NOT EDIT)

index.html contains old `#topfloor` and `#kanvatan` SPA sections. Never edit these unless explicitly told "edit the SPA version."

---

## CROSS-FILE CONSISTENCY

When editing ANY page, verify these patterns match across all pages:

**Nav dropdown:** Human Resource (→ `https://hrthefilm.com`, external, `target="_blank"`), Top Floor, Kan Vatan, ———, Türk Projeleri → /turkiye. NO individual Turkish sub-items. No LR or Meatspace. About → /about. Connect → mailto (see below). turkiye.html has standard sitewide nav + EN/TR toggle, plus a mobile-menu duplicate of the Work dropdown links that must stay in sync with the desktop ones.

**Connect is a plain mailto link everywhere — no modal (removed 2026-09-10).** Nav trigger and every other former "Connect"/"Request..." trigger on every page is now `<a href="mailto:mcoynegreen@gmail.com?subject=...">`, subject varies by context (generic triggers use `Hello%20from%20coyne-green.com`; Top Floor's "Request the Script" and Kan Vatan's "Request the Pilot" use their own project-specific subjects). There is no `#connectModal` markup, no modal JS (`openConnectModal`/`closeConnectModal`), no modal CSS (`.modal-overlay`/`.modal-btn`/`.checkbox-*`/etc.), and no hidden Netlify detection form (`<form name="connect" netlify hidden>`) on any page anymore — don't re-add any of it without being told to. Netlify Forms itself stays enabled at the account level; it's just unused now. If a `<button>` needed to become a mailto link, it was converted to an `<a>` (buttons can't carry `href`) — keep that pattern for any new mailto trigger.

**OG tags (every page):** Page-specific og:title, og:description, og:image (absolute URL with https://coyne-green.com), og:url (no trailing slash). twitter:card = summary_large_image.

**Footer:** © 2026 Max Coyne-Green line only (IP-protection paragraph removed 2026-09-10, all pages including turkiye.html's bilingual `.site-footer`). tfgame.html has NO footer. If a page's footer CSS still has a `p:first-child` rule left over from when there were two paragraphs, delete it — it now has higher specificity than a plain `.copyright-footer p{...}` rule and will silently win the cascade once there's only one child paragraph left.

**Type roles (added 2026-09-10):** Bebas Neue — name, nav links, eyebrows, captions, buttons/CTAs. EB Garamond roman — body text, loglines, bio, contact links, footer; italic reserved for taglines only. Project-page section headings (Story/Tone & Influences/Production Considerations/Context/etc.) — Garamond, uppercase, gold, matching across topfloor.html and kanvatan.html. Cinzel is used only for the Top Floor title itself — don't spread it elsewhere.

**Fonts:** Bebas Neue (headings), EB Garamond (body). No exceptions except tfgame.html game UI.

**Colors:** Base #0a0d10, gold #b8a472, text #e4e4e4, muted #6b7a88, border #1a1f28. Page-specific: turkiye #c47a5a, artci #8B7355, altindamarlari #B8860B, losingreality #2A7B9B.

---

## IMAGE RULES

- Absolute paths only: `/images/...`
- Convert to WebP: `cwebp -q 85` (never `sips`)
- Cache buster `?v=N` after replacing any image
- Check if background images contain baked-in text before adding HTML text

---

## #1 VISUAL RULE — NO ORPHAN WORDS

No heading, logline, tagline, or hero text may wrap to leave 1–2 orphan words on a new line at 375px or 430px. Every line of display text must fill the available width. Use `text-wrap: pretty`, `text-indent`, or manual `<br>`. Test at 375px with Playwright before every commit.

---

## QA REQUIREMENTS

**When to screenshot:** After any visual change. Always.
**Breakpoints:** 390x844 (mobile), 768x1024 (tablet), 1440x900 (desktop).
**Check:** Horizontal overflow, orphan words, broken images, font consistency, touch targets ≥44px on mobile.

---

## LOCKED DECISIONS

- HR comp: "Severance meets Margin Call" (NOT "Black Mirror meets Margin Call")
- TF comp: "Parasite meets The Talented Mr. Ripley" (never Trading Places)
- TF logline: "An ambitious Manhattan doorman moves into his doppelgänger's penthouse, only to get trapped in a dangerous new identity."
- TF logline verb: "get trapped" (not "be trapped")
- TF tone refs: RIPLEY, PARASITE, ROSEMARY'S BABY (not FARGO)
- Portfolio order: HR → Top Floor → Kan Vatan → Türk Projeleri → Coming Up (LR, Meatspace)
- TF section heading: "THERE ARE LEVELS TO THIS CITY" (not "The World")
- TF writer bio: REMOVED from page
- TF "Contained. Commercial. Castable.": REMOVED (stats grid kept)
- TF four-act still (`tf_4acts_full.webp`) and the old poster/hairline Final CTA section: REMOVED (2026-09-10) — replaced by a plain bordered "Request the Script" / "Play the Story" button pair
- TF tower logline (the three `.pyramid-line-1/2/3` lines in the hero) is `white-space:nowrap` with a `min()`-clamped fluid font-size — it must never wrap at any width; if the copy changes, the divisor constants in the `calc()` formula need recalibrating to the new character count, not just the base rem sizes
- Kan Vatan character portraits are intentionally rotated one step from their filenames (2026-09-10): `kv_abe.webp` displays as Sezen, `kv_sezen.webp` displays as Kaan, `kv_kaan.webp` displays as Abe. Alt text and card order (Sezen, Kaan, Abe) stayed put — only the `src` attributes moved. Don't "fix" this by matching filenames back to their own card.

---

## PENDING / DO NOT TOUCH

- Laurel images or festival counts (managed separately)
- Top Floor game content (tfgame.html — separate workflow; not touched in the 2026-09-10 refresh)

---

## SCREENPLAY PDFs

Files in `files/` directory. Primary share links:
- `/human-resource.pdf` — retired 2026-09-10, redirects to hrthefilm.com/read via `_redirects`. `files/HUMAN RESOURCE.pdf` stays here only as the Update Screenplay Shortcut's drop point; hrthefilm pulls its copy from this path.
- `/top-floor.pdf` → `files/TOP FLOOR.pdf`
- `/kan-vatan.pdf` → `files/Kan Vatan.pdf`

Legacy links still work as fallbacks. All PDF routing in `_redirects`. Content-Disposition headers in `_headers`.

Update workflow: User runs "Update Screenplay" Mac Shortcut → copies from Latest Drafts to this repo's `files/` → then tells Code to `deploy`.

---

## SERVER

Port 8878, threaded Python server. For local preview only. No start script exists in the repo — launch manually: `python3 -m http.server 8878` from the repo root.

---

## GOTCHAS / LESSONS

- **No shared JS/CSS on this site.** Every page is a fully self-contained file — inline `<style>` and `<script>` only, no shared includes. A few pages independently copy-paste a mobile-nav-dropdown click listener, but it's per-page, not global, and doesn't exist on pages without that nav. Don't assume a "global" behavior affects a new page without checking that page's own `<script>` tags (or lack thereof). turkiye.html additionally has its own full `#mobileMenu` overlay (separate from the desktop Work dropdown) that duplicates every nav link — when the desktop dropdown changes, check this overlay too, it's easy to miss (the 2026-09-10 refresh initially missed adding Kan Vatan here).
- **This section IS "LESSONS."** If a future prompt cites a dated "LESSONS" entry, this section is the only such log in the repo — verify the claim is actually written here before treating it as established fact.
- **Coupled breakpoints create pinch zones.** If a responsive variant-switch (e.g. showing different markup above/below a width) shares its breakpoint with another rule that also changes available width at that same width (e.g. a padding step), the width just past the shared breakpoint can be *tighter* than the width just before it — because both changes land at once. Give content-switch breakpoints their own value, comfortably clear of any spacing/padding breakpoint, and verify the exact boundary pixels empirically (not just round test widths).
- **`clamp()` font-size + a `max-width` container can re-wrap a fitted headline at wide viewports.** If a title's font-size keeps scaling with `vw` past the point where its container hits its own `max-width` cap, the available width freezes while the font keeps growing — so a headline that fits at a mid-range viewport can wrap again at 768px/1440px. Check wide breakpoints too, not just mobile, when a heading depends on `clamp()`.
- **`text-wrap: pretty` doesn't catch every single-word orphan in Chromium**, especially when the last words are split across inline elements (e.g. a `<span>` styled differently from surrounding text). Verify last-line word count directly (Range-based measurement, not just trusting the property); fall back to a manual `&nbsp;` between the last two words when it fails.
- **Width-measurement scripts must wait on `document.fonts.ready`.** Measuring text width immediately after navigation can silently use the fallback font (e.g. Georgia instead of a webfont) before it finishes loading, giving numbers ~20% off from the real rendered width.
- **`Element.getClientRects()` on a block element returns one rect for the whole box, not one per visual line.** To detect wrapping/line count inside a block, use a `Range` over its contents (or per-word Ranges) and cluster by `top` with a few px of tolerance — exact-equality clustering breaks when mixed inline elements (different font-size/baseline) land sub-pixel-different tops on the same visual line.
- **Playwright navigating to a URL it already visited this session can silently serve a stale cached response**, even after the file on disk changed — `page.goto()` to the identical URL doesn't guarantee a fresh network fetch. Confirmed disk file and `curl` both showed correct content while the live DOM still showed the pre-edit version. Fix: append a throwaway query param (`?cachebust=N`, incrementing each time) to force a real reload before any post-edit screenshot or DOM check.
- **`window.scrollTo(0, bottom)` then `window.scrollTo(0, 0)` does NOT reliably trigger `IntersectionObserver`-based `.reveal` animations for content in the middle of a long page.** Both scroll calls only ever put the very top or very bottom of the page in the viewport — anything in between (e.g. topfloor.html's/kanvatan.html's long-form story sections) never actually intersects the viewport during either jump, so it stays at `opacity:0` and screenshots as a blank gap. This isn't a site bug — real users scrolling naturally pass through every position and trigger every reveal. For screenshot capture, don't rely on scroll-jump timing at all: run `document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'))` right before capturing to force every reveal state deterministically.
- **index.html's five homepage panels use a DIFFERENT reveal mechanism than topfloor.html/kanvatan.html** — they're plain `<section>` elements (not `.reveal`-classed) observed by `document.querySelectorAll('section:not(.hero), .project-card-section')`, which adds a `.visible` class on intersection. Forcing `.reveal` visible does nothing for these panels. To force-reveal index.html for a screenshot: `document.querySelectorAll('.reveal, section:not(.hero), .project-card-section').forEach(el => el.classList.add('visible'))`, then wait the full `0.7s` transition before capturing — the opacity is still mid-transition at +300ms and will screenshot as half-invisible panels if you don't wait it out.
- **Negative `margin-right` on an `auto`-width block element does NOT pull its right edge inward — it pushes the right edge further out.** For a block with `margin-left:0` and `width:auto`, the browser solves `width = containing-block-width − margin-left − margin-right`; a negative margin-right *increases* the solved width, growing the box past its container rather than shrinking it to compensate for trailing letter-spacing. (Bit us on the `.kv` panel's eyebrow/title: a `margin-right:-.14em`/`-.16em` "fix" for perceived misalignment actually created a 17px/3px overflow that hadn't existed before — the panel was already perfectly right-aligned with zero margin.) To compensate for trailing letter-spacing pulling a right-aligned line's visual edge inward, use a *positive* margin-right, and verify empirically via `getBoundingClientRect().right` on all the elements you're aligning — don't trust the sign intuitively.
- **Homepage snap sections (2026-09-10):** `section.hero,.hr,.tf,.kv,.about` now fade-only on scroll-reveal (`opacity` transition, `transform:none!important`) instead of also translating — the translateY was fighting `scroll-snap-align:start` and made desktop scrolling choppy. Don't reintroduce a transform on these five sections without re-checking snap behavior.
- **Mobile hero slideshow interval is matchMedia-gated (2026-09-10):** the `setInterval` that auto-advances `.hero-slide`s only starts when `window.matchMedia('(min-width:861px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches` — below 861px the slideshow doesn't run at all (mobile only ever shows the first slide), and it won't start regardless of width for reduced-motion users. The first slide's CSS also has `transform:none!important;transition:none!important` at ≤860px so it can't "breathe" from a stale `.active` scale transform.
- **Images now get a 1-week edge cache (`_headers`: `/images/* Cache-Control: public, max-age=604800`, added 2026-09-10).** Any future image replacement needs its `?v=N` query string bumped in every HTML file that references it, or visitors will see the stale cached version for up to a week.
- **OG cards are the three `og-*.jpg` files in `images/`** (`og-home.jpg`, `og-kanvatan.jpg`, `og-topfloor.jpg`), all exactly 1200×630, generated by center-cropping the page's hero/key-art image — regenerate the same way if the source art changes, don't hand-crop.
- **Laurel images are stored pre-shrunk to 200px tall** (displayed at ≤48px, so 200px is retina-safe) — don't re-upload them at original festival-laurel-PNG resolution (some were 800px+ tall).
- **`:focus-within`/`:focus` CSS pseudo-classes don't repaint when the browser automation pane lacks real window focus.** `document.hasFocus()` can be `false` in this pane even though `document.activeElement` and `Element.matches(':focus-within')` correctly report the focused element — `getComputedStyle()` will still show the *un*-focused state in that condition, which looks like a broken CSS rule but isn't. Front the tab (`tabs_select`) and drive focus with a real `computer{action:"key", text:"Tab"}` press (not a JS `.focus()` call) before trusting a computed-style check of any `:focus`/`:focus-within`/`:hover` rule.
