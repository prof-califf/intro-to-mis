# MIS 320 · Introduction to Information Systems

A free, case-based digital textbook for MIS 320 at Western Washington University,
College of Business and Economics.

**Live site:** https://prof-califf.github.io/intro-to-mis/
Served from `index.html` via GitHub Pages (Settings → Pages → Deploy from a branch → `main` → `/ (root)`).

The course spine is the **five components of MIS** (hardware, software, data, networks,
people) and the weakest component rule: a system is only as strong as its weakest
component. Every chapter maps its case onto the five, and every lab practices locating
the break.

## What's here

**Pages (23)**

- `index.html` — landing page
- `schedule.html` — the 11-week course schedule
- `chapter0` … `chapter12` — thirteen case chapters
- `lab1` … `lab8` — eight checkpoint-gated labs
- `join-builder.html` — supporting interactive for the database chapter

**Client dataset (Cascadia Outfitters, 2025)**

- `cascadia-sales-2025.xlsx` — clean workbook; Labs 2, 4, 5
- `cascadia-sales-2025-RAW.xlsx` — deliberately dirty version; Lab 3 cleaning exercise
- `cascadia-sales-2025.csv` — flat file for Tableau (Lab 6)
- `cascadia.db` — SQLite database for the in-browser SQL sandbox (Lab 7)

Both workbooks open on an **Analyst** tab: one numbered row per checkpoint, the answer in
column B, an optional note in column C. The layout is identical in every lab, so
checkpoint 3 is always `B7` whether it is week 2 or week 5. Students download the same
file each week and save it as `LAB2_Last_First.xlsx`, `LAB3_Last_First.xlsx`, and so on.

**Build and instructor files**

- `build_cascadia.py` — regenerates the entire dataset deterministically (seed 320)
- `build_labs.py` — regenerates lab pages; checkpoint answers are computed from the
  database at build time, never typed by hand
- `build_analyst_tab.py` — rebuilds the Analyst tab in both workbooks
- `add_nav.py` — injects the site-wide dropdown navigation; idempotent, run after any rebuild
- `verify_facts.py` — checks every stated fact against the database
- `shared-inline.css` — the canonical stylesheet, inlined into each page at build time
- `.nojekyll` — tells GitHub Pages to serve files as-is. Leave it in place.

## How the labs work

Students do the work in Excel, Tableau, or the SQL sandbox, then paste each answer into
the lab page. A correct answer unlocks the next checkpoint. After the final checkpoint
they write a reflection, and the page generates a two-page PDF: page 1 is the completion
certificate, page 2 is their reflection.

Progress saves to browser storage, so a student can close the tab and come back. It does
not follow them to a different computer or survive a private window, and clearing browser
data clears it. Each lab has a **Reset this lab** button.

Every lab submits the same way: the work as one file named `LABn_Last_First`, plus the
certificate PDF. Lab 5 adds a third file, the board memo. Canvas assignments must be named
`Lab 1` through `Lab 8`, because the pages point at them by name.

**In Labs 2 through 5, the formula must be live in the answer cell.** A typed-in number
does not count. This is the enforcement mechanism for the no-AI rule in those four labs:
open the Analyst tab, click the cell, and it either shows a formula or it does not.

## AI policy

Lab 1 sets a three-light policy in week 1, before any other lab runs. Green is asking AI to
explain, quiz, or critique. Yellow is drafting with disclosure. Red is submitting AI output
as your own.

**Labs 2 through 5 are the exception: no AI at all**, including error explanations. Those
four weeks build hand skills in Excel, and AI returns as a coach in Lab 6. Lab 1's green
light names this exception explicitly, and its green-light example deliberately uses a
Tableau error from Lab 6 rather than an Excel one, so the two pages do not contradict
each other.

Any change to the red-light boxes in Labs 2–5 must be checked against Lab 1's green-light
definition and checkpoint 2.

## Instructor notes

- **Lab 5's anomaly is meant to be discovered.** Don't preview it. Students find the same
  finding again in Tableau (Lab 6) and SQL (Lab 7).
- **Lab 7's SQL sandbox needs http(s).** It works on GitHub Pages but not from a local
  `file://` open. A fallback message points students to sqliteonline.com.
- **Certificate codes are not proof of work.** The code is derived from the student's name
  plus the lab number and checkpoint count, nothing about their answers. That makes codes
  reproducible on request, which is how a lost certificate gets recovered. It also means a
  student who reads the page source can generate one without doing the lab. Treat the
  certificate as a completion receipt, not as evidence.
- **Checkpoint answers are base64-encoded in each page.** That is encoding, not encryption,
  and it is readable by anyone who looks. This is deliberate: on a static site there is
  nowhere to hide an answer, and the graded artifact is the submitted workbook, not the
  checkpoint.
- **Hints must not contain their answers.** Nine of them did, which combined with a CSS bug
  meant Lab 1 displayed five of its six answers on page load. Hints point at the method.
- **Anything committed to this repo is public**, whether or not a page links to it.
- **Instructor intro scripts live in a separate Word document**, not on the lab pages.
  Regenerate it rather than editing it by hand, or it will drift from the site.

## Rebuilding

```
python3 build_cascadia.py      # regenerate dataset (deterministic, seed 320)
python3 build_analyst_tab.py   # rebuild the Analyst tab in both workbooks
python3 build_labs.py          # regenerate lab pages from the dataset
python3 add_nav.py             # re-inject navigation
python3 verify_facts.py        # REQUIRED: checks every stated fact against the database
```

`verify_facts.py` exits nonzero if any checkpoint answer or prose claim disagrees with the
data. Run it after every content change, not just after regenerating the dataset.

**Also check the JavaScript.** `verify_facts.py` does not parse the inline scripts, and a
single unescaped apostrophe in a JS string silently kills an entire script block with no
visible error on the page. This has happened once, in Lab 8's SQL sandbox. Before
deploying, run `check_js.py` (below) and confirm it reports zero failures.

## Deploying

The working copy is whatever is currently in GitHub, not a local folder. **Download the
repo fresh before starting any editing session**, or edits made in the browser by a
co-instructor will be silently overwritten on the next upload. Prefer uploading only the
files that changed over replacing the whole tree.

## Still to build

Labs 9 (UX Design) and 10 (Information Architecture).

Free to use for educational purposes.
