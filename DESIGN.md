---
name: ProteinDB
description: Live comparison engine for Indian protein supplements — ranked by cost per verified gram.
colors:
  primary: "#6366f1"
  primary-muted: "#818cf8"
  primary-tint: "rgba(99, 102, 241, 0.1)"
  surface-base: "#0f172a"
  surface-elevated: "#1e293b"
  surface-floating: "rgba(30, 41, 59, 0.6)"
  text-primary: "#f8fafc"
  text-secondary: "#cbd5e1"
  text-tertiary: "#94a3b8"
  text-muted: "#64748b"
  border-subtle: "rgba(51, 65, 85, 0.5)"
  border-default: "#334155"
  success: "#10b981"
  success-tint: "rgba(16, 185, 129, 0.1)"
  danger: "#f43f5e"
  danger-tint: "rgba(244, 63, 94, 0.1)"
  warning: "#f59e0b"
  warning-tint: "rgba(245, 158, 11, 0.1)"
typography:
  display:
    fontFamily: "Geist Sans, Arial, Helvetica, sans-serif"
    fontSize: "clamp(2.25rem, 5vw, 3rem)"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Geist Sans, Arial, Helvetica, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Geist Sans, Arial, Helvetica, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Geist Sans, Arial, Helvetica, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.01em"
  caption:
    fontFamily: "Geist Sans, Arial, Helvetica, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.05em"
    textTransform: "uppercase"
rounded:
  sm: "6px"
  md: "12px"
  lg: "16px"
  xl: "24px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  2xl: "40px"
components:
  button-primary:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "{colors.primary-tint}"
    textColor: "{colors.primary-muted}"
  card-product:
    backgroundColor: "rgba(30, 41, 59, 0.4)"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.xl}"
    padding: "20px 24px"
  badge-indigo:
    backgroundColor: "{colors.primary-tint}"
    textColor: "{colors.primary-muted}"
    rounded: "{rounded.sm}"
    padding: "4px 12px"
  badge-success:
    backgroundColor: "{colors.success-tint}"
    textColor: "{colors.success}"
    rounded: "{rounded.sm}"
    padding: "4px 12px"
  input-range:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.lg}"
    padding: "8px 16px"
---

# Design System: ProteinDB

## 1. Overview

**Creative North Star: "The Lab Report"**

ProteinDB is a clean, clinical workspace where data speaks for itself. Like a premium laboratory dashboard — precise, trustworthy, unembellished. Every number is clearly labeled, every comparison is honest. The interface exists to present comparison data with radical transparency, not to sell or persuade.

The aesthetic is **minimal, modern, transparent** (per PRODUCT.md). The dark slate foundation creates a focused, premium environment that feels like a professional tool rather than a consumer marketplace. The indigo accent carries authority without aggression — it's the color of verified data, not marketing hype.

This system explicitly rejects e-commerce clutter (no urgency timers, no "BUY NOW" spam), generic SaaS admin panels (no sidebar nav, no dense data tables), and bro-science aggression (no red/black macho vibes, no "GET SHREDDED" typography). The tone is smart and informed.

**Key Characteristics:**
- Data-first hierarchy: cost-per-gram is the primary signal, everything else supports it
- Mobile-first pragmatism: most users browse on phones, touch targets are generous
- Restrained confidence: premium feel without pretension — solid colors, clean typography, no gradients
- Trust through transparency: lab badges, stock status, price freshness are all visible and honest

## 2. Colors

The palette is **Deep Indigo Night** — a dark slate base with indigo accents that feels like a premium tech tool used after hours. Calm, focused, sophisticated.

### Primary
- **Indigo Signal** (`#6366f1`): The primary action and accent color. Used for cost-per-gram badges, active filters, slider thumbs, and interactive highlights. Its rarity on the dark surface makes it punchy without being garish.
- **Indigo Muted** (`#818cf8`): Hover states, secondary highlights, and softer accents where the full primary would be too intense.
- **Indigo Tint** (`rgba(99, 102, 241, 0.1)`): Background fills for badges, tags, and selected states. Provides indigo presence at 10% opacity.

### Neutral
- **Slate Base** (`#0f172a`): The foundation — page background, deepest layer. Almost black but tinted blue-gray to avoid the harshness of pure #000.
- **Slate Elevated** (`#1e293b`): Cards, panels, input backgrounds. One step up from base for tonal layering.
- **Slate Floating** (`rgba(30, 41, 59, 0.6)`): Glassmorphism surfaces — sticky control panel, product cards. Semi-transparent to show depth through the base layer.
- **Text Primary** (`#f8fafc`): Headlines, key numbers, active labels. Near-white for maximum contrast.
- **Text Secondary** (`#cbd5e1`): Body text, descriptions, inactive labels. Comfortable contrast without competing with primary text.
- **Text Tertiary** (`#94a3b8`): Metadata, timestamps, helper text. Deliberately receded.
- **Text Muted** (`#64748b`): Placeholders, disabled states, least important information.
- **Border Subtle** (`rgba(51, 65, 85, 0.5)`): Dividers inside cards, separators. Barely visible but provides structure.
- **Border Default** (`#334155`): Card outlines, input borders, panel edges. More visible than subtle for containing elements.

### Semantic
- **Success** (`#10b981`): In-stock status, verified badges, positive indicators. Emerald green — calm and trustworthy.
- **Success Tint** (`rgba(16, 185, 129, 0.1)`): Background for lab-verified sections. Green presence at 10%.
- **Danger** (`#f43f5e`): Out-of-stock status, error states. Rose red — clear but not alarming.
- **Danger Tint** (`rgba(244, 63, 94, 0.1)`): Background for out-of-stock badges.
- **Warning** (`#f59e0b`): Price unavailable, partial data, attention-needed states. Amber — warm, not aggressive.
- **Warning Tint** (`rgba(245, 158, 11, 0.1)`): Background for N/A price badges.

### Named Rules
**The One Voice Rule.** The primary indigo accent is used on ≤10% of any given screen. Its rarity is the point — when you see indigo, it means "this is the number that matters." Never use indigo for decorative fills or background tints larger than a badge.

**The Tinted Neutral Rule.** No pure #000 or #fff anywhere. Every neutral is tinted toward the indigo hue at low chroma (chroma 0.005–0.01). The base background is slate-950, not black. Text is slate-50, not white. This creates cohesion without monotony.

## 3. Typography

**Display Font:** Geist Sans (with Arial, Helvetica, sans-serif fallback)
**Body Font:** Geist Sans (same stack)
**Label/Mono Font:** Geist Sans (same stack)

**Character:** A single sans-serif family with a technical, confident feel. Geist's geometric precision pairs with the lab-report aesthetic — every glyph feels measured and intentional. The tight tracking on display sizes adds urgency without aggression.

### Hierarchy
- **Display** (800 weight, clamp(2.25rem, 5vw, 3rem), line-height 1.1, -0.025em tracking): Hero headline only — "ProteinDB 🇮🇳" at the top of the page. One use per page maximum.
- **Headline** (700 weight, 1.5rem, line-height 1.2, -0.01em tracking): Product names, section headers, filter panel title. The workhorse for important labels.
- **Body** (400 weight, 1rem, line-height 1.5): Descriptions, explanations, card content. Max line length 65–75ch.
- **Label** (600 weight, 0.875rem, line-height 1.4, 0.01em tracking): Form labels, filter names, metadata keys. Slightly bolder than body for scanability.
- **Caption** (500 weight, 0.75rem, line-height 1.4, 0.05em tracking, uppercase): Tiny metadata — "Lab Verified", "In Stock", "Last Updated". Uppercase with wide tracking for instant recognition.

### Named Rules
**The Flat Scale Rule.** Typography hierarchy is built through weight contrast (≥1.25 ratio between steps) and size, not color. Display is 800, Headline is 700, Body is 400 — the gap between 700 and 400 is intentional and forceful. Avoid intermediate weights (500, 600) for body text.

## 4. Elevation

Depth is conveyed through a hybrid of **tonal layering** and **subtle ambient shadows**. Surfaces are flat at rest — no default shadows on cards. Shadows appear only as a response to state (hover, sticky positioning) and are always soft, diffuse, and dark.

The base layer is slate-950. Cards sit on slate-900/40 (semi-transparent). The sticky control panel uses slate-900/60 with backdrop-blur-xl — the most elevated surface, visually "above" the scrollable content. This creates depth without relying on heavy shadows.

### Shadow Vocabulary
- **Ambient Hover** (`0 8px 30px rgb(0, 0, 0, 0.4)`): Appears on product cards on hover. Soft, dark, diffuse — lifts the card without making it feel like a popup.
- **Sticky Panel** (`shadow-lg` default + `backdrop-blur-xl`): The filter panel uses a large shadow plus heavy blur to separate it from scrolling content. The blur is functional, not decorative.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. Shadows appear only as a response to state (hover, elevation, focus). A card without hover has zero shadow — it sits in the tonal layer stack purely through background opacity.

**The Functional Blur Rule.** Backdrop blur is used only for the sticky control panel and only because it needs to visually separate from scrolling content beneath it. Never use blur decoratively on cards or static surfaces.

## 5. Components

### Buttons
- **Shape:** 12px radius (`rounded-md`), fully rounded corners for a friendly but precise feel.
- **Primary:** Slate-800 background (`#1e293b`), slate-200 text, 1px slate-700 border, 12px 24px padding. Solid and trustworthy.
- **Hover / Focus:** Background shifts to indigo tint (`rgba(99, 102, 241, 0.1)`), text shifts to indigo muted (`#818cf8`), border shifts to indigo-500/20. A subtle lift — never a color inversion.
- **Active:** Scale to 0.95 (`active:scale-95`), immediate feedback without animation delay.

### Cards / Containers (Product Cards)
- **Corner Style:** 24px radius (`rounded-3xl`). Generous rounding softens the data density.
- **Background:** Slate-900/40 (`rgba(30, 41, 59, 0.4)`) with backdrop-blur-sm. Semi-transparent to show tonal depth.
- **Shadow Strategy:** Zero shadow at rest. On hover: Ambient Hover shadow (`0 8px 30px rgb(0, 0, 0, 0.4)`) plus subtle border lightening (`hover:border-slate-700/80`).
- **Border:** 1px slate-800 (`#1e293b`). Visible but not prominent — provides containment without visual weight.
- **Internal Padding:** 20px 24px (`p-5 md:p-6`). Generous breathing room around data.

### Inputs / Fields (Range Slider, Brand Select)
- **Style:** Slate-800 track (`bg-slate-800`), indigo-500 thumb (`accent-indigo-500`), rounded-lg (8px) track.
- **Focus:** Indigo-400 thumb on hover (`hover:accent-indigo-400`). No glow, no ring — just the accent color intensifying.
- **Dropdown:** Slate-800 background, slate-700 border, rounded-xl (12px), shadow-2xl for the open panel. Max-height 16rem with overflow-y-auto.

### Navigation (Sticky Control Panel)
- **Style:** Slate-900/60 background, backdrop-blur-xl, 1px slate-800 border, rounded-3xl (24px), shadow-lg.
- **Position:** Sticky top-4, z-10. Floats above content as the user scrolls.
- **Hover:** Shadow intensifies (`hover:shadow-slate-900/50`), no other change.

### Badges / Tags
- **Indigo Badge:** Indigo tint background (`bg-indigo-500/10`), indigo muted text (`text-indigo-300`), 1px indigo-500/20 border, rounded-md (6px), px-3 py-1. Used for "Cost per Gram" highlight, active filters.
- **Success Badge:** Emerald tint background (`bg-emerald-500/10`), emerald text (`text-emerald-400`), 1px emerald-500/20 border. Used for "Lab Verified" and "In Stock".
- **Danger Badge:** Rose tint background, rose text, rose border. Used for "Out of Stock".

### [Signature Component: Product Data Grid]
The product card's internal data grid is the system's signature pattern. A 2-column grid of metric tiles — each tile has:
- Slate-800/50 background, rounded-2xl (16px), 1px slate-700/50 border
- Label in caption style (uppercase, 0.75rem, wide tracking)
- Value in bold body or display weight, depending on importance
- Color coding: green for verified data, amber for missing data, white for normal data

## 6. Do's and Don'ts

### Do:
- **Do** use tonal layering (opacity variations of slate) to create depth before reaching for shadows.
- **Do** reserve indigo for the most important data point on any screen — cost per gram.
- **Do** use generous border-radius (24px for cards, 12px for buttons) to soften the data density.
- **Do** present lab verification with emerald green — it's the color of trust in this system.
- **Do** use uppercase + wide tracking for micro-labels ("Price", "Stock", "Protein"). It makes metadata scannable.
- **Do** ensure 4.5:1 contrast ratios for all body text against the slate-950 background.

### Don't:
- **Don't** use gradient text (`background-clip: text`). Decorative, never meaningful. Use a single solid color. (From PRODUCT.md anti-references)
- **Don't** use glassmorphism as a default. Blurs and glass cards used decoratively are forbidden. The sticky panel's blur is functional, not decorative. (From PRODUCT.md anti-references)
- **Don't** use side-stripe borders (`border-left` > 1px as a colored accent). Never intentional. Use full borders, background tints, or leading icons instead. (From shared design laws)
- **Don't** use the hero-metric template (big number, small label, supporting stats, gradient accent). SaaS cliché. (From shared design laws)
- **Don't** create identical card grids. Same-sized cards with icon + heading + text, repeated endlessly. Each product card should feel like a unique data point. (From shared design laws)
- **Don't** use modals as a first thought. Modals are usually laziness. Exhaust inline alternatives first. (From shared design laws)
- **Don't** add "BUY NOW" buttons, urgency timers, or stock scarcity badges. This is a comparison tool, not a store. (From PRODUCT.md anti-references)
- **Don't** use red/black aggressive gym aesthetics. No "GET SHREDDED", no macho imagery. (From PRODUCT.md anti-references)
