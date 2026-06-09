# CLAUDE.md

Project context for Claude Code. Human-facing documentation is in [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

- Dashboard: `docs/index.html` (static, open directly in browser — no server needed)
- Dataset: `assets/data/coffee-shop-dataset.csv`
- EDA notebook: `notebooks/analysis.ipynb`

## Dataset quirks

- Currency: `"R$ 45,00"` — strip `R$ `, replace `,` with `.` before casting to float
- Dates: `DD-MM-YYYY` (day-first, not ISO 8601)
- `Day of Week`: 0-indexed Monday-first (0 = Monday, 6 = Sunday)
- 149 116 rows, 3 stores (Hell's Kitchen, Lower Manhattan, Astoria), Jan–Jun 2023

## Dashboard stack

TailwindCSS · Lucide icons · Iconify/Solar · Google Fonts — all bundled locally in `docs/assets/`.  
Grid: `grid-cols-1 md:grid-cols-8 lg:grid-cols-12`.
