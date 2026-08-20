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

## ACTIVE PAGES (16)

| URL | File | Notes |
|-----|------|-------|
| `/` | index.html | Homepage |
| `/hr` | hr.html | HR standalone |
| `/hr-trailer` | hr-trailer.html | HR trailer standalone page |
| `/topfloor` | topfloor.html | Top Floor pitch |
| `/kanvatan` | kanvatan.html | Kan Vatan pitch |
| `/about` | about.html | Career timeline |
| `/hr/deep` | hr-deep.html | HR deep dive |
| `/hr/characters` | hr-slideshow.html | HR characters |
| `/hr-short` | hr-watch.html | HR festival screener (hidden, Vimeo embed) |
| `/tfgame` | tfgame.html | Top Floor game (hidden) |
| `/meatspace` | meatspace.html | Meatspace |
| `/artci` | artci.html | Artçı |
| `/altindamarlari` | altindamarlari.html | Altın Damarları |
| `/losingreality` | losingreality.html | Losing Reality |
| `/turkiye` | turkiye.html | Turkish portfolio (bilingual) |
| `/secret` | secret.html | Kinnikuman treatment (hidden) |
| `/imposter` | imposter.html | Imposter Syndrome one-pager (hidden) |

"All pages" = ALL of these.

---

## LEGACY SPA ROUTES (DO NOT EDIT)

index.html contains old `#topfloor` and `#kanvatan` SPA sections. Never edit these unless explicitly told "edit the SPA version."

---

## CROSS-FILE CONSISTENCY

When editing ANY page, verify these patterns match across all pages:

**Nav dropdown:** HR, Top Floor, ———, Türk Projeleri → /turkiye. NO individual Turkish sub-items. No LR or Meatspace. About → /about. Connect → modal. turkiye.html has standard sitewide nav + EN/TR toggle.

**Connect modal checkboxes (English):** Human Resource, Top Floor, Turkish Projects, General meeting, Other. NO "Collaborating on new concepts." Title: "CONNECT" with no subtitle. turkiye.html has Turkish modal with individual Turkish project checkboxes.

**OG tags (every page):** Page-specific og:title, og:description, og:image (absolute URL with https://coyne-green.com), og:url (no trailing slash). twitter:card = summary_large_image.

**Footer:** © 2026 Max Coyne-Green + IP protection paragraph. turkiye.html has Turkish translation. tfgame.html has NO footer.

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

---

## PENDING / DO NOT TOUCH

- Laurel images or festival counts (managed separately)
- Top Floor game content (tfgame.html — separate workflow)

---

## SCREENPLAY PDFs

Files in `files/` directory. Primary share links:
- `/human-resource.pdf` → `files/HUMAN RESOURCE.pdf`
- `/top-floor.pdf` → `files/TOP FLOOR.pdf`
- `/kan-vatan.pdf` → `files/Kan Vatan.pdf`

Legacy links still work as fallbacks. All PDF routing in `_redirects`. Content-Disposition headers in `_headers`.

Update workflow: User runs "Update Screenplay" Mac Shortcut → copies from Latest Drafts to this repo's `files/` → then tells Code to `deploy`.

---

## SERVER

Port 8878, threaded Python server. For local preview only.
