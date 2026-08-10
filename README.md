# MIS 320 · Introduction to Information Systems
A free, case-based digital textbook — Western Washington University, College of Business and Economics.

**Live site:** enable GitHub Pages (Settings → Pages → deploy from `main`, root) and the site serves from `index.html`.

## Layout
Flat, by design — all links are relative.
- `index.html` — landing page (chapters, labs, data)
- `chapter*.html` — case chapters (Ch 0–4, 6 live)
- `lab*.html` — checkpoint-gated labs (L1–L7 live) with reflection + PDF certificate
- `cascadia*` — the Cascadia Outfitters client dataset (clean/RAW workbooks, CSV, SQLite)
- `build_cascadia.py` / `build_labs.py` — regenerate the dataset (seed 320) and lab pages; checkpoint answers are computed from the database, never hand-entered
- `answer-key.json` — instructor answer key (consider a private repo copy if students get curious)
- `shared-inline.css` — canonical stylesheet, inlined into chapter/lab pages at build time

## Instructor notes
- Lab certificates: verification codes are deterministic (name + lab + checkpoint count). Suspicious code → have the student regenerate it live.
- Lab 5's anomaly is meant to be discovered, not announced.
- Lab 7's SQL sandbox requires http(s) — it works on Pages, not from a local file:// open.
