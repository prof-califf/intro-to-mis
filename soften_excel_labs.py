"""Excel-track softening. Lab 2 becomes a pure warm-up (SUMIF out, MAX in).
Lab 3 is rebuilt from scratch: no RAW-file cleaning, just one-question-one-formula
work (COUNTIF/SUMIF families) on the clean workbook; cleaning now debuts in Lab 7.
Lab 5's mini project gains a guided path. All cross-references updated.
All checkpoint answers computed live from the data, never hand-entered."""
import re, csv, base64, json, glob

b64 = lambda v: base64.b64encode(str(v).encode()).decode()
rows = list(csv.DictReader(open('cascadia-sales-2025.csv')))
F = lambda r,k: float(r[k])
cnt_bham   = sum(r['store']=='Bellingham' for r in rows)
cnt_snow   = sum(r['category']=='Snow' for r in rows)
rev_pp     = round(sum(F(r,'revenue') for r in rows if r['store']=='Portland Pearl'),2)
snow_rev   = [F(r,'revenue') for r in rows if r['category']=='Snow']
avg_snow   = round(sum(snow_rev)/len(snow_rev),2)
cnt_tac_m  = sum(r['store']=='Tacoma' and r['is_member']=='Y' for r in rows)
rev_snw_sf = round(sum(F(r,'revenue') for r in rows if r['category']=='Snow' and r['store']=='Seattle Flagship'),2)
total_rev  = round(sum(F(r,'revenue') for r in rows),2)
pp_share   = round(100*rev_pp/total_rev,1)
max_line   = max(F(r,'revenue') for r in rows)

# ================================================== 1. LAB 2 SOFTENING
t = open('lab2-excel-basics.html').read()
P = [
 ('<h2><span class="num">Skills</span>Navigation, SUM, AVERAGE, sort, filter, SUMIF</h2>',
  '<h2><span class="num">Skills</span>Navigation, SUM, AVERAGE, MAX, sort, filter</h2>'),
 ('''<li><strong>Now make Excel answer a question.</strong> SUMIF revenue by store name. COUNTIF rows where
<code class="inline">is_member</code> is "N": you'll meet that number again later in the course.</li>''',
  '''<li><strong>One more single-cell answer.</strong> Use MAX on the revenue column to find the
single biggest sale of the year. That is the whole skill set for today: one cell, one function, one
answer. Next week, Lab 3 turns questions like "how much revenue came from one store?" into equally
short formulas; this week, getting comfortable is the entire job.</li>'''),
 ('{"q": "Checkpoint 6 \\u00b7 Use SUMIF: revenue for the Seattle Flagship store only?", "t": "num", "a": "MTQ4NDcxLjc1", "tol": 1, "h": "=SUMIF(store_column,\\"Seattle Flagship\\",revenue_column)"}',
  json.dumps({"q":"Checkpoint 6 \u00b7 Use MAX on the revenue column. What is the single largest sale line of the year, in dollars?","t":"num","a":b64(max_line),"tol":0,"h":"=MAX(K:K) if revenue is in column K. One cell, one function, one answer, and a nice trivia fact about the co-op's biggest single sale."})),
 ('what SUMIF does', 'what a function does'),
 ('For the\n  next month, you are their analyst.',
  '''For the
  next month, you are their analyst. This first lab is deliberately a warm-up: if you have used Excel
  before, it will feel comfortable, and if you have not, every step below is spelled out.'''),
]
for old,new in P:
    assert t.count(old)==1, ('LAB2', old[:60], t.count(old))
    t = t.replace(old,new)
open('lab2-excel-basics.html','w').write(t)
print('lab2 softened')

# ================================================== 2. LAB 3 REBUILD
lab2 = open('lab2-excel-basics.html').read()
head = lab2[:lab2.index('<main id="top">')]
tail = lab2[lab2.index('</main>'):]
cpblock = lab2[lab2.index('<h2 id="checkpoints"'):lab2.index('<h2 id="submit"')]

head = head.replace('<title>Lab 2: Excel Basics | MIS 320</title>',
                    '<title>Lab 3: Excel Functions | MIS 320</title>')
head = re.sub(r'<meta name="description" content="[^"]*">',
 '<meta name="description" content="One question, one formula: COUNTIF, SUMIF, AVERAGEIF and their two-condition cousins on the clean Cascadia workbook. No cleaning, no tricks, seven checkpoints.">',
 head, count=1)
head = head.replace('class="current" href="lab2-excel-basics.html"', 'href="lab2-excel-basics.html"')
head = head.replace('<a href="lab3-excel-dataprep.html">', '<a class="current" href="lab3-excel-dataprep.html">')
head = re.sub(r'<nav id="chapnav">.*?</nav>',
 '''<nav id="chapnav">
    <a href="#top">Overview</a><a href="#anatomy">The formula, once</a>
    <a href="#part1">Part 1 · COUNTIF</a><a href="#part2">Part 2 · SUMIF &amp; AVERAGEIF</a>
    <a href="#part3">Part 3 · Two conditions</a><a href="#part4">Part 4 · Making a share</a>
    <a href="#checkpoints">Checkpoints</a><a href="#submit">What to submit</a>
    <a href="chapter3-dominos.html">↳ Chapter 3 · Business Processes</a>
  </nav>''', head, flags=re.S)

QS = [
 {"q":"Checkpoint 1 \u00b7 COUNTIF: how many sales lines came from the Bellingham store?","t":"num","a":b64(cnt_bham),"tol":0,
  "h":"=COUNTIF(C:C,\"Bellingham\") with store names in column C. Type it in any empty cell and press Enter."},
 {"q":"Checkpoint 2 \u00b7 COUNTIF again, different column: how many sales lines are in the Snow category?","t":"num","a":b64(cnt_snow),"tol":0,
  "h":"Same shape, new target: =COUNTIF(F:F,\"Snow\") with category in column F. Notice you already know this function."},
 {"q":"Checkpoint 3 \u00b7 SUMIF: total revenue from the Portland Pearl store, in dollars?","t":"num","a":b64(rev_pp),"tol":1,
  "h":"=SUMIF(C:C,\"Portland Pearl\",K:K): look in C for the store, add up the matching rows of K. Three arguments, read left to right."},
 {"q":"Checkpoint 4 \u00b7 AVERAGEIF: the average revenue per sales line in the Snow category, to the cent?","t":"num","a":b64(avg_snow),"tol":0.05,
  "h":"=AVERAGEIF(F:F,\"Snow\",K:K). Identical shape to SUMIF; only the verb changed. Snow gear is expensive, so expect a big number."},
 {"q":"Checkpoint 5 \u00b7 COUNTIFS (plural): how many sales lines at the Tacoma store were member sales (is_member = Y)?","t":"num","a":b64(cnt_tac_m),"tol":0,
  "h":"=COUNTIFS(C:C,\"Tacoma\",N:N,\"Y\"). The S version takes pairs: column, condition, column, condition. Two questions at once."},
 {"q":"Checkpoint 6 \u00b7 SUMIFS: revenue from Snow-category sales at the Seattle Flagship, in dollars?","t":"num","a":b64(rev_snw_sf),"tol":1,
  "h":"=SUMIFS(K:K,F:F,\"Snow\",C:C,\"Seattle Flagship\"). One quirk: in the S version the sum column moves to the front. Everything else is the same idea."},
 {"q":"Checkpoint 7 \u00b7 Put two formulas together: what percent of the co-op's total revenue came from Portland Pearl, to one decimal?","t":"num","a":b64(pp_share),"tol":0.1,
  "h":"=SUMIF(C:C,\"Portland Pearl\",K:K)/SUM(K:K)*100. Your Checkpoint 3 answer divided by Lab 2's total, times one hundred. Two functions you already own, one business answer."},
]
REFLECT = ("Think of a business, team, or club you know from the inside. Write the one question about it you "
 "would answer first with a COUNTIF or SUMIF if you had its data in a spreadsheet, and name the decision "
 "that number would actually change. If the number would not change any decision, pick a better question.")

new_tail = tail
new_tail = new_tail.replace('const LAB="LAB2"', 'const LAB="LAB3"')
new_tail = re.sub(r'QS=\[.*?\];', lambda m: 'QS='+json.dumps(QS)+';', new_tail, count=1, flags=re.S)
old_ref = re.search(r"splitTextToSize\('Prompt: (.*?)',480\)", new_tail, re.S).group(1)
new_tail = new_tail.replace(old_ref, REFLECT.replace("'","\\'"))
old_nm = re.search(r"p\.text\('(Lab 2 [^']*)',280,222", new_tail).group(1)
new_tail = new_tail.replace(old_nm, 'Lab 3 \\u00B7 Excel Functions: One Question, One Formula')

old_prompt = re.search(r'<div class="certbox" id="reflectbox">\s*<h3>[^<]*</h3>\s*<p style="font-family:var\(--sans\);font-size:\.88rem">(.*?)</p>', cpblock, re.S).group(1)
cpblock3 = cpblock.replace(old_prompt, REFLECT)
cpblock3 = re.sub(r'Checkpoint progress: 0 / \d+', 'Checkpoint progress: 0 / 7', cpblock3)

MAIN = f'''<main id="top">
<header class="chaphead">
  <p class="eyebrow">Lab 3 · Week 3</p>
  <h1>Excel Functions: One Question, One Formula</h1>
  <div class="meta-row"><span>Lab session · 80 min</span><span class="alt"><a href="chapter3-dominos.html" style="color:inherit;text-decoration:none">Pairs with Chapter 3 · Business Processes &#8594;</a></span></div>
</header>

<p class="lede">Last week you toured the client's workbook and totaled it. This week you interrogate
it. Every business question in this lab has the same three-part shape: which column to look in, what
to look for, and what to do with the rows that match. Learn that shape once and you have learned six
functions at the same time. There is nothing to clean, nothing hidden, and no trick: seven questions,
seven short formulas, and the exact formula pattern is printed in every checkpoint's hint.</p>

<div class="callout"><strong>Download</strong>
<p style="font-family:var(--sans);font-size:.9rem">Same workbook as last week: <a href="cascadia-sales-2025.xlsx">cascadia-sales-2025.xlsx</a>.
If you still have your Lab 2 file, keep working in it; add a new sheet for this week. Columns you will
use today: <code class="inline">C</code> store, <code class="inline">F</code> category,
<code class="inline">K</code> revenue, <code class="inline">N</code> is_member.</p></div>

<div class="callout callout-bridge"><strong>From lecture to lab</strong><p><strong>Lab professor's intro (10 min):</strong>
Open with the mantra and write it on the board: one question, one formula. Demo Checkpoint 1 live and
slowly: type =COUNTIF(C:C,"Bellingham"), narrating the three parts as you go, where to look, what to
match, and (for the SUM version) what to add up. Then show that Checkpoint 2 is the same formula with
a different column, so the room sees the pattern transfer before working alone. Reassure directly:
every hint in this lab contains the full formula shape, so nobody is being tested on memory, only on
reading a question and picking the right column. Early finishers get the summary-block challenge in
the callout near the end; it feeds directly into next week's charts.</p></div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach</strong>
  <p>If a formula errors or a function's arguments confuse you, paste the formula (not the checkpoint
  question) into an AI and ask it to explain what each argument does. Then fix it yourself in the
  workbook. The checkpoints measure whether your workbook answers questions, and the workbook is
  yours.</p></div>
</div>

<div id="anatomy"></div>
<h2><span class="num">Skills</span>The formula, learned once</h2>

<p>Here is the whole lab in one line: <code class="inline">=COUNTIF(C:C,"Bellingham")</code>. Read it
the way Excel does. <strong>COUNTIF</strong> is the verb: count. <code class="inline">C:C</code> is
where to look: all of column C, the stores. <code class="inline">"Bellingham"</code> is what to look
for, in quotes because it is text. Excel scans the column, counts the matches, and puts one number in
one cell.</p>

<p>Every function today is that sentence with a different verb or one extra clause:</p>

<table class="lab">
<thead><tr><th>Function</th><th>The question it answers</th><th>Shape</th></tr></thead>
<tbody>
<tr><td><code class="inline">COUNTIF</code></td><td>How many rows match?</td><td>=COUNTIF(where, what)</td></tr>
<tr><td><code class="inline">SUMIF</code></td><td>Add a column, but only matching rows</td><td>=SUMIF(where, what, add-this)</td></tr>
<tr><td><code class="inline">AVERAGEIF</code></td><td>Average a column, but only matching rows</td><td>=AVERAGEIF(where, what, average-this)</td></tr>
<tr><td><code class="inline">COUNTIFS / SUMIFS</code></td><td>Same, with two or more conditions at once</td><td>pairs of (where, what)</td></tr>
</tbody>
</table>

<details class="howto"><summary>How to enter and check a formula</summary><div class="howto-body">
<ol>
<li>Click any empty cell to the right of the data, for example P2.</li>
<li>Type the formula starting with <code class="inline">=</code> and press Enter. Excel replaces what you typed with the answer; the formula still lives in the cell, visible in the formula bar.</li>
<li>Label it: type the question in the cell next to it. An unlabeled number is a future mystery.</li>
<li>If you get <code class="inline">#NAME?</code>, a function name is misspelled. If you get 0 unexpectedly, check the quotes and the spelling of the store or category, it must match the data exactly.</li>
</ol>
</div></details>

<div id="part1"></div>
<h2><span class="num">Part 1</span>COUNTIF: how many?</h2>
<p>Checkpoints 1 and 2. Same function twice, pointed at two different columns, so the pattern sinks
in. Both answers are plain counts of sales lines.</p>

<div id="part2"></div>
<h2><span class="num">Part 2</span>SUMIF and AVERAGEIF: how much?</h2>
<p>Checkpoints 3 and 4. One new argument appears: the column to add up (or average). Read each
formula aloud to yourself as a sentence, "look in C for Portland Pearl, and total the matching rows
of K," and the arguments stop being arbitrary.</p>

<div id="part3"></div>
<h2><span class="num">Part 3</span>Two conditions at once</h2>
<p>Checkpoints 5 and 6. Real business questions usually have two clauses: <em>this store AND member
sales</em>, <em>this category AND that location</em>. The plural functions, COUNTIFS and SUMIFS, take
condition pairs. One quirk to know before it bites: in SUMIFS the column being summed moves to the
front. The hint shows exactly where everything goes.</p>

<div id="part4"></div>
<h2><span class="num">Part 4</span>Making a share: two formulas, one answer</h2>
<p>Checkpoint 7 is the week's small graduation: divide one formula by another to turn two raw numbers
into a percentage a manager would actually ask for. This is how nearly every business metric is born,
one measured thing divided by another, and it is the move you will make constantly from Lab 5
onward.</p>

<div class="callout callout-good"><strong>Finished early? Build the summary block</strong>
<p>In a blank area, list the eight store names down a column (type them or copy unique values). Next
to each, write a COUNTIF for its number of lines, a SUMIF for its revenue, and a COUNTIFS for its
member lines, then fill the formulas down. Eight rows, four columns: you have just built, by hand,
the table every dashboard is secretly made of. Keep it in your workbook. Next week's lab turns
exactly this block into charts.</p></div>

{cpblock3}
<h2 id="submit"><span class="num">Canvas</span>What to submit</h2>
<p style="font-family:var(--sans);font-size:.92rem">Your workbook as LAB3_Last_First.xlsx with your
labeled formulas (and the summary block if you built it), plus your completion certificate PDF (your
reflection is page 2 of it).</p>
</main>'''

open('lab3-excel-dataprep.html','w').write(head + MAIN + new_tail)
print('lab3 rebuilt:', len(head+MAIN+new_tail))

# ================================================== 3. LAB 5 GUIDED PATH
t5 = open('lab5-excel-analysis.html').read()
i = t5.index('Memo from the board')
end = t5.index('</div>', i) + len('</div>')
GUIDE = '''

<details class="howto"><summary>Guided path, if the open brief feels like a cliff</summary><div class="howto-body">
<p>The investigation is meant to be yours, but the tools are all things you own. If you are stuck,
work this ladder, and stop the moment you have a suspect:</p>
<ol>
<li>The board's worry is about <em>members</em>. Get one number per store that measures membership, not revenue: for each store, =COUNTIFS(store, name, is_member,"Y") divided by =COUNTIF(store, name). That ratio is the store's member attach rate. (Your Lab 3 summary block is this table, one column short.)</li>
<li>Or the pivot version: rows = store, values = count of sale_id, columns = is_member, then compute the Y share per row in the cells beside the pivot.</li>
<li>Now read the eight rates side by side. Seven of them will look like siblings. The eighth is your answer to Checkpoint 3, and everything after that is measuring how bad it is.</li>
</ol>
<p>Using this ladder is not cheating; it is the method. The skill being graded is noticing that
revenue could not answer the board's question and choosing a measure that could.</p>
</div></details>'''
t5 = t5[:end] + GUIDE + t5[end:]
open('lab5-excel-analysis.html','w').write(t5)
print('lab5 guided path added')

# ================================================== 4. CROSS-REFERENCES
def patch(fn, pairs):
    t = open(fn).read(); n=0
    for old,new in pairs:
        c = t.count(old)
        assert c==1, (fn, old[:70], c)
        t = t.replace(old,new); n+=1
    open(fn,'w').write(t); print(fn, ':', n, 'patches')

patch('lab7-sql.html', [
 ("In Lab 3 you cleaned Cascadia's messy sales export by hand in Excel. It took",
  "Cascadia's controller has been sitting on a dirty sales export all quarter. Cleaning it by hand in Excel would take"),
 ("the same dirty export they cleaned by hand in Lab 3, this time",
  "the controller's dirty export, not in a spreadsheet but"),
 ("What took\n  a full Excel session takes six functions",
  "What would take\n  a full Excel session takes six functions"),
 ("Every VLOOKUP you wrote in Lab 3 was a hand-built imitation of this one line, and the last two checkpoints ask you to use it.",
  "Every SUMIF you wrote in Lab 3 asked one question of one table; a JOIN asks one question across two tables at once, and the last two checkpoints ask you to make that move."),
 ("This is the same export you cleaned by hand in Lab 3.",
  "This is the controller's export exactly as her system produced it."),
 ("In Lab 3 you found these by eye in Excel.",
  "In Excel you would hunt these down by eye; LIKE finds them in one line."),
])

patch('chapter5-walmart.html', [
 ("You have already watched it fail. In Lab 3, the RAW file handed you prices",
  "You are about to watch it fail. In this week's lab, the controller's RAW export hands you prices"),
 ("The lesson under Lab 3", "The lesson under Lab 7"),
 ("The cleaning you did by hand in Excel, standardizing formats,",
  "The cleaning this week's lab walks you through, standardizing formats,"),
])

patch('chapter7-moneyball.html', [
 ("which after Labs 3 and 7 you know is not the copy the\nregisters write",
  "which after Lab 7 you know is not the copy the\nregisters write"),
])

# chapter 3: dynamic capture of the lab tie-in sentence
t3 = open('chapter3-dominos.html').read()
m = re.search(r'The lab this week[^<]*(?:<[^>]+>[^<]*)*?cleaning the evidence of one\.</p>', t3, re.S)
assert m, 'ch3 lab tie-in not found'
t3 = t3.replace(m.group(0),
 '''The lab this week, Lab 3: Excel Functions, continues the Cascadia Outfitters engagement, and the
connection is direct: a swimlane tells you where a process runs, and a one-line formula tells you how
it is performing. Domino's tracker is, underneath, a wall of exactly such single-question answers.
This week you learn to write them.</p>''')
open('chapter3-dominos.html','w').write(t3); print('chapter3 tie-in rewritten')

# schedule: new blurb, pill gone
patch('schedule.html', [
 ('''<h4><a href="lab3-excel-dataprep.html">Lab 3: Data Preparation</a><span class="pill hard">Hardest so far</span></h4>
      <p>The controller's dirty export. Budget the full session.</p>''',
  '''<h4><a href="lab3-excel-dataprep.html">Lab 3: Excel Functions</a></h4>
      <p>One question, one formula: COUNTIF, SUMIF, and their two-condition cousins on the clean workbook.</p>'''),
])

# index: card + downloads pill
patch('index.html', [
 ('<h4>Data Preparation. The RAW File</h4><p>The controller\'s dirty export. 7 checkpoints.</p>',
  '<h4>Excel Functions: One Question, One Formula</h4><p>COUNTIF, SUMIF, and friends on the clean workbook. 7 checkpoints.</p>'),
 ('RAW workbook: Lab 3 (.xlsx)', 'RAW workbook: Lab 7 (.xlsx)'),
])

# global label passes
OLD_LBL = '<span class="lbl">Lab 3 &middot; Week 3</span>Data Preparation: The RAW File'
NEW_LBL = '<span class="lbl">Lab 3 &middot; Week 3</span>Excel Functions: One Question, One Formula'
OLD_DL  = 'Cascadia sales, RAW for Lab 3 (.xlsx)'
NEW_DL  = 'Cascadia sales, RAW export for Lab 7 (.xlsx)'
for fn in glob.glob('*.html'):
    t = open(fn).read(); o=t
    t = t.replace(OLD_LBL, NEW_LBL).replace(OLD_DL, NEW_DL)
    if t!=o: open(fn,'w').write(t)
print('global labels updated')

# ================================================== 5. VERIFY_FACTS SYNC
v = open('verify_facts.py').read()
v = v.replace("TRUTH['top_store'], None],",
              "TRUTH['top_store'], round(q1(f\"SELECT MAX({R}) FROM sales\"),2)],", 1)
m = re.search(r"'lab3-excel-dataprep\.html': \[.*?\],\n", v, re.S)
assert m, 'lab3 entry not found in verify_facts'
NEW_L3 = (" 'lab3-excel-dataprep.html': ["
 "q1(\"SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham'\"),\n"
 "                   q1(\"SELECT COUNT(*) FROM sales s JOIN products p ON p.product_id=s.product_id WHERE p.category='Snow'\"),\n"
 "                   round(q1(f\"SELECT SUM({R}) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Portland Pearl'\"),2),\n"
 "                   round(q1(f\"SELECT AVG({R}) FROM sales s JOIN products p ON p.product_id=s.product_id WHERE p.category='Snow'\"),2),\n"
 "                   q1(\"SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Tacoma' AND s.member_id IS NOT NULL\"),\n"
 "                   round(q1(f\"SELECT SUM({R}) FROM sales s JOIN products p ON p.product_id=s.product_id JOIN stores st ON st.store_id=s.store_id WHERE p.category='Snow' AND st.store_name='Seattle Flagship'\"),2),\n"
 "                   round(100*q1(f\"SELECT SUM({R}) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Portland Pearl'\")/TRUTH['total_revenue'],1)],\n")
v = v.replace(m.group(0), NEW_L3)
open('verify_facts.py','w').write(v)
print('verify_facts synced')
