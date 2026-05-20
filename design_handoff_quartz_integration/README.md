# Handoff: IsAbel Design System → Quartz Wiki

## Overview

This bundle hands off a complete design system for **IsAbel** — the Spiritist Doctrine study wiki at [`gabrielgmendonca/isabel-wiki`](https://github.com/gabrielgmendonca/isabel-wiki). The site is built with **Quartz** (a static-site generator for Obsidian vaults) and deployed via GitHub Pages.

Your job is to apply the design system in this bundle to the Quartz site. You'll need to edit Quartz's config, replace the logo, and write a custom SCSS override file for things Quartz's config doesn't expose.

---

## About the Design Files

The files in `reference_ui_kit/` are **design references created in HTML/React** — a click-thru prototype showing the intended look and behavior. They are **not production code to copy directly**. They are written against vanilla React with inline JSX (no build step) so they can be opened in a browser; the real site is **Quartz + Preact**.

Your task is to **port these design decisions into the existing Quartz codebase**, using Quartz's established patterns (its `quartz.config.ts`, its SCSS files, its component overrides).

---

## Fidelity

**High-fidelity (hifi).** Final colors, typography, spacing, and behavior are all decided. The design is built on top of Quartz's existing wiki UI — the goal is *refinement and consistency*, not a redesign. Match values exactly.

---

## Target Repository

- **Owner / repo:** `gabrielgmendonca/isabel-wiki`
- **Generator:** Quartz (v4)
- **Deployment:** GitHub Pages

Clone it locally, then apply the changes below.

---

## What changes (high level)

| Area | What | Where in Quartz |
| --- | --- | --- |
| Color tokens | Update `--tertiary`, decouple `--fg-3` from `--gray` | `quartz.config.ts` (partial) + custom SCSS (rest) |
| Typography | Schibsted Grotesk (headers), Source Sans 3 (body), IBM Plex Mono (code), EB Garamond (wordmark + blockquotes + ceremonial slides) | `quartz.config.ts` + Google Fonts import |
| Logo | Replace tagline color, sage instead of blue-gray | `static/icon.png` (or wherever the wordmark lives) — replace with `assets/logo-isabel.svg` from this bundle |
| Blockquotes | EB Garamond **upright** (not italic), 3px sage left rule | Custom SCSS |
| Heading colors | All four levels share `--fg-1` (Quartz tints h4 `--secondary` by default — remove that) | Custom SCSS override |
| Layout | Narrower side rails (200 / fluid / 220), tighter gap (40px) | Quartz layout config or custom SCSS |
| Tagline subtitle | "WIKI ESPÍRITA" was illegible light-blue-gray; now sage | Wherever the page subtitle is rendered |

---

## Step-by-step

### 1. Update `quartz.config.ts`

```ts
configuration: {
  // ... existing config ...
  theme: {
    fontOrigin: "googleFonts",
    cdnCaching: true,
    typography: {
      header: "Schibsted Grotesk",
      body: "Source Sans 3",
      code: "IBM Plex Mono",
    },
    colors: {
      lightMode: {
        light:         "#faf8f8",
        lightgray:     "#e5e5e5",
        gray:          "#b8b8b8",
        darkgray:      "#4e4e4e",
        dark:          "#2b2b2b",
        secondary:     "#4a6741",
        tertiary:      "#6cb55a",   // widened from #6b9e5e — needed for hover differentiation
        highlight:     "rgba(106, 158, 94, 0.15)",
        textHighlight: "#fff236aa",
      },
      darkMode: {
        light:         "#161618",
        lightgray:     "#393639",
        gray:          "#646464",
        darkgray:      "#d4d4d4",
        dark:          "#ebebec",
        secondary:     "#7db87a",
        tertiary:      "#9ed49b",
        highlight:     "rgba(125, 184, 122, 0.15)",
        textHighlight: "#fff23633",
      },
    },
  },
}
```

Quartz handles the Google-Fonts injection automatically when `fontOrigin: "googleFonts"`.

> **Note:** EB Garamond is NOT a typography token in Quartz's config — it's used only for the wordmark in the logo SVG and selectively in custom CSS (blockquotes, ceremonial slide titles). Add it as a separate Google Fonts import in your custom SCSS (see step 2) or in `quartz/components/Head.tsx`.

### 2. Add a custom SCSS override

Quartz does not expose every value via config. Create a new file `quartz/styles/custom.scss` (or append to your existing custom file) with:

```scss
// === IsAbel design system overrides ===

// (a) EB Garamond — used for blockquotes and ceremonial copy.
//     Not part of Quartz's typography tokens; load it directly.
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&display=swap');

// (b) Decouple "meta text" from "disabled gray".
//     Quartz uses --gray (#b8b8b8) for both, which fails on cream backgrounds.
//     --gray stays for rules and disabled UI; meta text gets its own value.
:root {
  --fg-meta: #6e6e6a;        // light mode — was binding to --gray, too pale
}
:root[saved-theme="dark"] {
  --fg-meta: #9c9c98;
}

// (c) Headings: all four levels share --dark (Quartz tints h4 --secondary by default).
article h4,
.popover-inner h4 {
  color: var(--dark) !important;
}

// (d) Blockquote: EB Garamond UPRIGHT (Quartz uses italic serif by default).
article blockquote,
.popover-inner blockquote {
  font-family: "EB Garamond", Garamond, Georgia, serif;
  font-style: normal;
  font-weight: 400;
  font-size: 1.1rem;
  line-height: 1.5;
  border-left: 3px solid var(--secondary);
  padding: 6px 20px;
  letter-spacing: 0.002em;
}

// (e) Meta lines / breadcrumbs — use --fg-meta, not --gray.
//     Selectors here may need to match Quartz's actual class names; inspect the DOM.
.content-meta,
.breadcrumb-container,
.tags { color: var(--fg-meta); }

// (f) Breadcrumb separator — was --gray, too faint
.breadcrumb-container > .breadcrumb-element + .breadcrumb-element::before {
  color: #6e6e6a;
}

// (g) Tagline (the "WIKI ESPÍRITA" small caps below the wordmark)
.page-title-sub {
  color: var(--secondary) !important;
  letter-spacing: 0.24em;          // was 0.32em — too airy
  font-weight: 500;
}

// (h) Sidebar tree chevrons
.folder-icon,
.explorer .chevron { color: #6e6e6a; }
```

> **Important:** the exact class selectors above (`.content-meta`, `.breadcrumb-container`, `.folder-icon`, `.page-title-sub`, etc.) are Quartz-version-dependent. Open the rendered HTML in DevTools and adapt the selectors. The reference UI kit in `reference_ui_kit/wiki.css` uses our own class names — use it as a **specimen of intent**, not selectors.

### 3. Replace the logo

The current logo has its tagline ("WIKI ESPÍRITA") rendered in `#8E9EAB` — a light blue-gray that fails on cream backgrounds. The fixed version is in `assets/logo-isabel.svg` in this bundle.

- Replace `quartz/static/icon.png` (or wherever the site icon lives) with the SVG.
- If Quartz expects a PNG, render the SVG to PNG at 2x (e.g. `inkscape -w 940 logo-isabel.svg -o icon.png`) — or update the asset reference to use SVG directly.
- The wordmark uses **EB Garamond** at 700 (big caps "I", "A") + 400 (small "s", "bel"). The tagline is sage `#4A6741` at 13px, weight 500, letter-spacing 4.

### 4. Layout: narrower side rails

If the user has customized the layout (`quartz.layout.ts`), or you're using `Component.MobileOnly`/`DesktopOnly` rails, the design targets:

- **Left rail:** 200px (was wider — Quartz default ~320px)
- **Right rail:** 220px
- **Center column:** fluid `minmax(0, 1fr)`
- **Gap between columns:** 40px
- **Max page width:** 1320px

In `quartz/styles/base.scss` or your custom SCSS, look for the page grid rule and adjust. The reference is `reference_ui_kit/wiki.css` lines 17–30.

### 5. Verify in dark mode

The token system has light + dark modes. After applying changes, toggle Quartz's dark mode and verify:

- Meta text (`--fg-meta` / `--fg-3`) is readable
- Blockquote sage rule is visible on dark bg
- Tertiary (`#9ed49b`) is a clear step above secondary (`#7db87a`)

---

## Interactions & behavior

These were not part of the design changes — Quartz's existing interactions stay:

- Explorer tree expand/collapse
- Search modal (Ctrl/Cmd-K)
- Font-size widget (`Aa A− A+`)
- Dark-mode toggle
- Graph rendering (just verify the node color uses `--tertiary` = `#6cb55a` now, not the old `#6b9e5e`)
- Backlinks / TOC scroll-spy

---

## Design Tokens (full reference)

The canonical source is `design_tokens/colors_and_type.css`. Key values:

### Colors — Light

| Token | Value | Used for |
| --- | --- | --- |
| `--light` | `#faf8f8` | Page background (warm off-white) |
| `--lightgray` | `#e5e5e5` | Rules, card borders, code-bg |
| `--gray` | `#b8b8b8` | Disabled text, faint ornaments (NOT meta text) |
| `--darkgray` | `#4e4e4e` | Body text |
| `--dark` | `#2b2b2b` | Headings (all levels) |
| `--secondary` | `#4a6741` | Sage — links, accent rules, headings tint when needed |
| `--tertiary` | `#6cb55a` | Brighter sage — link hover, graph node fill |
| `--highlight` | `rgba(106, 158, 94, 0.15)` | Selection / callout background |
| `--textHighlight` | `#fff236aa` | Inline `==marker==` highlight |
| `--fg-meta` (custom) | `#6e6e6a` | Article meta, breadcrumbs, captions — replaces `--gray` for body-sized meta text |

### Colors — Dark

See `design_tokens/colors_and_type.css` lines 115–131.

### Typography

| Token | Family | Used for |
| --- | --- | --- |
| `--headerFont` | Schibsted Grotesk | UI headings (h1–h4), article titles |
| `--bodyFont` | Source Sans 3 | Body, paragraph, lists, tags |
| `--codeFont` | IBM Plex Mono | Code, kbd, citation refs, eyebrow tokens |
| `--brandFont` | EB Garamond | Wordmark, blockquotes (upright), ceremonial slide titles |

### Type scale (light mode, desktop)

| Token | px | Use |
| --- | --- | --- |
| `--fs-3xl` | 44 | Article h1 |
| `--fs-2xl` | 32 | Article h2 |
| `--fs-xl` | 24 | Article h3 |
| `--fs-lg` | 18 | Article h4, lead paragraph |
| `--fs-base` | 16 (18 mobile) | Body |
| `--fs-sm` | 14 | Meta, breadcrumbs, footer |
| `--fs-xs` | 12 | Tags, captions |

### Spacing / radii / borders

| Token | Value |
| --- | --- |
| `--space-2` to `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 px |
| `--radius-sm` | 4px (chips, buttons) |
| `--radius-md` | 6px (cards, callouts) |
| `--radius-lg` | 10px (logo plate) |
| `--border-1` | `1px solid var(--rule)` |
| `--border-accent` | `3px solid var(--secondary)` (blockquote rule) |

---

## Assets

- `assets/logo-isabel.svg` — updated logo with sage tagline
- `design_tokens/colors_and_type.css` — full token definitions (the authoritative source)
- `reference_ui_kit/` — interactive design reference. Open `index.html` in a browser to see the intended visual outcome. Inspect class names + CSS for component patterns.

---

## Files in this bundle

- `README.md` — this document
- `design_tokens/colors_and_type.css` — full design token CSS (colors, type, spacing, motion)
- `assets/logo-isabel.svg` — updated logo
- `reference_ui_kit/` — React (no-build) UI kit demonstrating the design in context:
  - `index.html` — entry point (open in browser)
  - `wiki.css` — stylesheet showing every component's final state
  - `App.jsx`, `Article.jsx`, `LeftRail.jsx`, `RightRail.jsx`, `Screens.jsx`, `Icons.jsx` — components

---

## How to verify when done

1. Build Quartz locally (`npx quartz build --serve`).
2. Open a sample article. Check:
   - "tipo: conceito · fontes: ESE, LE" is readable (not light gray on white).
   - Breadcrumb `›` arrows are visible.
   - h4 is dark, not sage.
   - Blockquote is EB Garamond upright, sage left rule.
   - Link hover is visibly brighter (test against `#6cb55a`).
   - Wordmark tagline "WIKI ESPÍRITA" is sage, readable.
   - Sidebar tree chevrons are visible.
3. Toggle dark mode. Re-verify all of the above.
4. Compare against `reference_ui_kit/index.html` opened in a browser side-by-side.

---

## Gotchas

- **Don't bind `--fg-3` / `--fg-meta` to `--gray`.** Quartz's `--gray` (`#b8b8b8`) is for disabled UI; using it for meta text caused half of this design system's revisions.
- **EB Garamond is not a UI heading font.** Use it only for: wordmark, blockquotes, ceremonial slide titles. UI headings stay Schibsted Grotesk.
- **Avoid italic serifs.** The user explicitly rejected italic blockquotes / italic numerals as "too bent over". Use upright EB Garamond.
- **Avoid the `#8E9EAB` blue-gray.** The original logo SVG used it for the tagline. It does not pass contrast on cream. Use `--secondary` instead.
- **Tertiary jump matters.** `--tertiary` was originally `#6b9e5e` — almost indistinguishable from `--secondary`. The widened `#6cb55a` makes hover states actually perceptible.
