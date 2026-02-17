# Website Codebase — Claude Code Instructions

## SESSION RULES

**Compaction strategy:** Before starting, plan commit points. Group related fixes (e.g., all nav changes, all OG changes) and commit each group. Never accumulate more than ~8 file changes uncommitted. If context is getting long, commit what you have, push, report progress, and stop cleanly. An incomplete session with committed work beats a complete session lost to compaction.

**Copy is sacred:** Never invent, paraphrase, reword, or "improve" any copy. If a prompt includes text to use, use it verbatim. If copy is needed but not provided, stop and ask. The only exception is OG descriptions derived from existing page content.

**Read before writing:** Before editing any file, read it first. Don't assume you know what's in it from a previous session or from CLAUDE.md descriptions. Files change between sessions.

---

## ACTIVE PAGES

| URL | File | Notes |
|-----|------|-------|
| / | index.html | SPA: homepage + HR section |
| /topfloor | topfloor.html | Standalone producer pitch |
| /kanvatan | kanvatan.html | Standalone cinematic pitch |
| /about | about.html | Horizontal-scroll career timeline |
| /hr/deep | hr-deep.html | HR project deep dive |
| /hr/characters | hr-slideshow.html | HR character slideshow |
| /tfgame | tfgame.html | Top Floor interactive game (hidden) |
| /meatspace | meatspace.html | Meatspace project page |
| /gomuldu | gomuldu.html | Gömüldü project page |
| /altindamarlari | altindamarlari.html | Altın Damarları project page |
| /losingreality | losingreality.html | Losing Reality project page |
| /turkiye | turkiye.html | Turkish-language portfolio |

When a prompt says "all pages," it means ALL 12 of these.

## Legacy SPA Routes (DO NOT EDIT unless explicitly told)

index.html contains old `#topfloor` and `#kanvatan` SPA sections. These are legacy routes that still serve basic info but are NOT the primary pages. Never make changes to these sections unless the user specifically says "edit the SPA version."

- The real Top Floor page is `topfloor.html`
- The real HR deep dive is `hr-deep.html`

---

## CROSS-FILE CONSISTENCY RULES

These define patterns that must be identical across all pages. When editing ANY page, check that these haven't drifted.

**Nav dropdown (all pages):**
- HR, Top Floor, ─────, Türk Projeleri (→/turkiye), Kan Vatan (indented), Gömüldü (indented), Altın Damarları (indented)
- About → /about
- Connect → local modal
- Türk Projeleri is a clickable `<a>`, not a dim label
- NO Losing Reality or Meatspace in nav
- turkiye.html has additional Turkish left-nav (Projeler, Hakkımda, İletişim) but same Work dropdown

**Connect modal checkboxes (all pages with modals):**
- Human Resource, Top Floor, Kan Vatan, General meeting with Max
- turkiye.html has its own Turkish modal with both English and Turkish project groups (no LR or Meatspace in either)

**OG tag pattern (every page):**
- og:title — page-specific (not generic site title)
- og:description — page logline or first sentence of body copy
- og:image — page-specific image, absolute URL with `https://coyne-green.com` prefix
- og:url — correct page URL, no trailing slash
- twitter:card — `summary_large_image` (never `summary`)
- twitter:title, twitter:description, twitter:image — match og equivalents

**Footer:** Same copyright block on every page. turkiye.html has Turkish translation.

**Fonts:** Bebas Neue (headings), EB Garamond (body). No exceptions.

**Colors:** Base `#0a0d10`, gold accents `#b8a472`. turkiye.html uses charcoal `#0a0d10` with terracotta `#c47a5a`.

---

## IMAGE RULES

- ALL paths must be absolute: `/images/...` (never relative `images/...`)
- Convert to WebP with `cwebp -q 85` — never use `sips`
- Add cache buster `?v=N` after replacing any image

---

## #1 VISUAL RULE — NO ORPHAN WORDS (ENFORCE ON EVERY CHANGE)

No heading, logline, tagline, or hero text may wrap to leave 1–2 orphan words on a new line at 375px or 430px. Every line of display text must use the available viewport width. If text wraps, make it bigger or adjust letter-spacing/padding until it fills the line — never shrink it to avoid wrapping. Use `text-wrap: pretty`, `text-indent`, or manual `<br>` as needed. Test at 375px with Playwright before every commit. If any line has a hanging word, fix it before pushing.

---

## QA REQUIREMENTS

**When to screenshot:** After any visual change. Always.

**Breakpoints:** 390x844 (mobile), 768x1024 (tablet), 1440x900 (desktop).

**What to check:** Horizontal overflow, orphan words on headings, broken images, font consistency, touch targets ≥44px on mobile.

---

## PENDING / DO NOT TOUCH

These items are in progress or blocked. Do not modify unless a prompt explicitly says to:

- Top Floor hero redesign (sandbox in topfloor-art-deco-test.html)
- Top Floor elevator reverse-scroll mechanics in topfloor.html (fragile)
- 9th festival laurel (Downtown Film Fest — no image yet)
- Laurel images or festival counts (managed separately)
- HR SPA extraction (deferred)
- turkiye.html copy (pending wife review)
- Top Floor game content (tfgame.html — separate workflow)
- `Live/backups-*` folders

---

## LOCKED DECISIONS (reference only)

- TF primary logline: "An ambitious Manhattan doorman moves into his doppelgänger's penthouse, only to get trapped in a dangerous new identity."
- TF comps: "Parasite meets The Talented Mr. Ripley"
- Portfolio order: HR → Top Floor → Kan Vatan → Türk Projeleri → Coming Up (LR, Meatspace)

---

## SERVER

- Port 8878, threaded Python server
- Open pages via AppleScript only
