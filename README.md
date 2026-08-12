# MIS 320 · Introduction to Information Systems

A free, case-based digital textbook for MIS 320 at Western Washington University,
College of Business and Economics.

**Live site:** enable GitHub Pages (Settings → Pages → Deploy from a branch → `main` → `/ (root)`).
The site serves from `index.html`.

## What's here

**Pages (15)**
- `index.html` — landing page
- `schedule.html` — the 11-week course schedule
- `chapter0` … `chapter6` — six case chapters (Ch 0, 1, 2, 3, 4, 6)
- `lab1` … `lab7` — seven checkpoint-gated labs

**Client dataset (Cascadia Outfitters, 2025)**
- `cascadia-sales-2025.xlsx` — clean workbook, used from Lab 2 on
- `cascadia-sales-2025-RAW.xlsx` — deliberately dirty version for the Lab 3 cleaning exercise
- `cascadia-sales-2025.csv` — flat file for Tableau (Lab 6)
- `cascadia.db` — SQLite database for the in-browser SQL sandbox (Lab 7)

**Build and instructor files**
- `build_cascadia.py` — regenerates the entire dataset deterministically (seed 320)
- `build_labs.py` — regenerates all lab pages; checkpoint answers are computed from the
  database at build time, never typed by hand
- `add_nav.py` — injects the site-wide dropdown navigation; idempotent, run after any rebuild
- `shared-inline.css` — the canonical stylesheet, inlined into each page at build time
- `answer-key.json` — instructor answer key

## How the labs work

Students do the work in Excel, Tableau, or the SQL sandbox, then paste each answer into
the lab page. A correct answer unlocks the next checkpoint. After the final checkpoint they
write a short reflection, and the page generates a two-page PDF: page 1 is the completion
certificate with a verification code, page 2 is their reflection. Students upload that one
PDF to Canvas.

Verification codes are derived from the student's name plus the lab, so they are
reproducible. If a code looks wrong, have the student regenerate it in front of you.

## Instructor notes

- **Lab 5's anomaly is meant to be discovered.** Don't preview it. Students find the same
  finding again in Tableau (Lab 6) and SQL (Lab 7).
- **Lab 7's SQL sandbox needs http(s).** It works on GitHub Pages but not from a local
  `file://` open. A fallback message points students to sqliteonline.com.
- **`answer-key.json` is public in this repo.** Remove it if you'd rather it not be.
- **`.nojekyll`** tells GitHub Pages to serve files as-is. Leave it in place.

## Rebuilding

```
python3 build_cascadia.py    # regenerate dataset (deterministic)
python3 build_labs.py        # regenerate lab pages from the dataset
python3 add_nav.py           # re-inject navigation
python3 verify_facts.py      # REQUIRED: checks every stated fact against the database
```

`verify_facts.py` exits nonzero if any checkpoint answer or prose claim disagrees with
the data. Run it after every content change, not just after regenerating the dataset.

## Still to build

Chapters 5 and 7–12; Labs 8 (UX), 9 (AI/ML), and 10 (Information Architecture).

Free to use for educational purposes.
