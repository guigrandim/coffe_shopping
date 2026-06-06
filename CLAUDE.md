# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a coffee shop analytics/dashboard project containing:
- Transaction dataset (CSV) for a multi-location coffee shop chain
- A static HTML design mockup (`design-system/index.html`) for a bento-grid dashboard UI

There is no build system, backend, or test suite — all artifacts are static files.

## Viewing the design system

Open `design-system/index.html` directly in a browser. It is self-contained and loads all dependencies (TailwindCSS, Lucide icons, Iconify Solar icons, Google Fonts) from the bundled `assets/` files — no server required.

## Dataset schema

File: `assets/data/coffee-shop-dataset.csv`

| Column | Notes |
|--------|-------|
| `transaction_id` | Unique transaction identifier |
| `transaction_date` | Format: `DD-MM-YYYY` |
| `transaction_time` | Format: `HH:MM:SS` |
| `store_id` / `store_location` | Multi-location (e.g. Hell's Kitchen, Lower Manhattan) |
| `product_id`, `product_category`, `product_type`, `product_detail` | Product hierarchy |
| `transaction_qty` | Units sold |
| `unit_price` / `Total_Bill` | Brazilian Real (R$), comma as decimal separator |
| `Size` | `Not Defined` for most records |
| `Month Name`, `Day Name`, `Hour`, `Month`, `Day of Week` | Pre-computed time dimensions |

**Key data quirks:**
- Currency values use Brazilian formatting: `"R$ 45,00"` — treat as strings when importing; strip `R$ ` and replace `,` with `.` before parsing as float.
- Date strings use day-first format (`17-01-2023`), not ISO 8601.
- `Day of Week` is 0-indexed Monday-first (0 = Monday, 6 = Sunday).

## Design system stack

The `design-system/index.html` uses:
- **TailwindCSS** (via `assets/resource_3fa48481346f.js`)
- **Lucide icons** (via `assets/lucide_latest_2eebd0ebe8c2.js`, initialized with `lucide.createIcons()` on DOMContentLoaded)
- **Iconify + Solar icon set** (via `assets/iconify_654a1ef798a3.js`, icons declared with `data-icon="solar:*"`)
- **Multiple Google Fonts** loaded from bundled CSS files in `design-system/assets/`

The current design is a garden irrigation control UI used as a template/reference. The component structure is a 12-column bento grid (`grid-cols-1 md:grid-cols-8 lg:grid-cols-12`) with `<section>` cards of varying column spans.
