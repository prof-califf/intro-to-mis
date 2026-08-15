"""Excel labs become tutorials: Part A 'follow along' (keystroke-level steps),
Part B 'now you' (same skills, solo). AI fully banned for Labs 2-5 with a
standardized red light carrying each lab's specific rationale. Lab 2 and Lab 3
mains rebuilt wholesale; Labs 4-5 restructured surgically. Answers unchanged
except Lab 3's order (checkpoints 2 and 3 swap so the tutorial pair comes first)."""
import re, csv, base64, json

b64 = lambda v: base64.b64encode(str(v).encode()).decode()
rows = list(csv.DictReader(open('cascadia-sales-2025.csv')))
F = lambda r,k: float(r[k])
V = dict(
 n_rows   = len(rows),
 tot_rev  = round(sum(F(r,'revenue') for r in rows),2),
 tot_qty  = int(sum(F(r,'quantity') for r in rows)),
 avg_line = round(sum(F(r,'revenue') for r in rows)/len(rows),2),
 max_line = max(F(r,'revenue') for r in rows),
 cnt_bham = sum(r['store']=='Bellingham' for r in rows),
 cnt_snow = sum(r['category']=='Snow' for r in rows),
 rev_pp   = round(sum(F(r,'revenue') for r in rows if r['store']=='Portland Pearl'),2),
 cnt_tacm = sum(r['store']=='Tacoma' and r['is_member']=='Y' for r in rows),
 rev_ss   = round(sum(F(r,'revenue') for r in rows if r['category']=='Snow' and r['store']=='Seattle Flagship'),2),
)
snow=[F(r,'revenue') for r in rows if r['category']=='Snow']
V['avg_snow']=round(sum(snow)/len(snow),2)
V['pp_share']=round(100*V['rev_pp']/V['tot_rev'],1)

def redbox(specific):
    return f'''<div class="ailight r">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Red &middot; No AI in the Excel labs</strong>
  <p>For Labs 2 through 5, AI tools stay closed entirely: no formula help, no error explanations, no
  checking your work. These four weeks build hand skills, and an AI can produce everything in this lab
  in seconds, which is exactly why it is off: whatever it does for you never becomes yours.
  {specific} If you are stuck, that is what the walkthrough steps, the hints, and your lab professor
  are for. AI returns as a coach in Lab 6, under the Lab 1 lights.</p></div>
</div>'''

def swap_ailight(fn, newbox):
    t=open(fn).read()
    i=t.find('class="ailight')
    assert i>0, fn
    start=t.rfind('<div',0,i)
    j=t.find('</p></div>', i); assert j>0
    end=t.find('</div>', j+10)+len('</div>')
    t=t[:start]+newbox+t[end:]
    assert t.count('class="ailight')==1, (fn, t.count('class="ailight'))
    open(fn,'w').write(t); print(fn,'red light installed')

# ================================================== LAB 2 REBUILD
t=open('lab2-excel-basics.html').read()
head=t[:t.index('<main id="top">')]
tail=t[t.index('</main>'):]
cpblock=t[t.index('<h2 id="checkpoints"'):t.index('<h2 id="submit"')]

QS2=[
 {"q":"Part A \u00b7 After Step 3: how many rows of sales data are in the sheet? (Data rows, not the header.)","t":"num","a":b64(V['n_rows']),"tol":0,
  "h":"Ctrl+End (Cmd+Fn+\u2192 then \u2193 on a Mac) lands on the last row. The header row takes one, so subtract it from the row number you see."},
 {"q":"Part A \u00b7 Your P2 cell after Step 4: total revenue for 2025, in dollars?","t":"num","a":b64(V['tot_rev']),"tol":1,
  "h":"=SUM(K:K) exactly as typed in Step 4. If you got 0, check that you are on the data sheet and that you pressed Enter."},
 {"q":"Part B \u00b7 Same move, new column: how many total units did the co-op sell? (Sum the quantity column.)","t":"num","a":b64(V['tot_qty']),"tol":0,
  "h":"The pattern is =SUM(column:column), and quantity lives in column H. You wrote this formula five minutes ago with a different letter."},
 {"q":"Part B \u00b7 Average revenue per sales line, to the cent?","t":"num","a":b64(V['avg_line']),"tol":0.05,
  "h":"The verb changes, the shape does not: =AVERAGE( ) pointed at the revenue column."},
 {"q":"Part B \u00b7 Use the filter and status-bar method: which store produced the most revenue in 2025?","t":"txt","a":b64('Seattle Flagship'),"tol":0,
  "h":"Filter column C to one store, click column K's header, and read Sum in the status bar at the bottom. Eight stores, eight reads, one clear winner. Clear the filter when done."},
 {"q":"Part B \u00b7 Confirm the year's biggest single sale with =MAX on the revenue column. Dollars?","t":"num","a":b64(V['max_line']),"tol":0,
  "h":"=MAX(K:K). Trivia for the curious: three different stores tie for it."},
]
old=re.search(r'QS=(\[.*?\]);',tail,re.S)
tail=tail[:old.start(1)]+json.dumps(QS2)+tail[old.end(1):]

MAIN2 = f'''<main id="top">
<header class="chaphead">
  <p class="eyebrow">Lab 2 · Week 2</p>
  <h1>Excel Basics: Meeting the Client</h1>
  <div class="meta-row"><span>Lab session · 80 min</span><span class="alt"><a href="chapter1-starbucks.html" style="color:inherit;text-decoration:none">Pairs with Chapter 1 · The Value of Information &#8594;</a></span></div>
</header>

<p class="lede">Meet your client. Cascadia Outfitters is a member-owned gear co-op with eight stores
from Boise to Bellingham, 35 products, and a business model that lives or dies on its members. For
the next month, you are their analyst. This lab is built as a tutorial: <strong>Part A walks you
through every click and keystroke</strong>, and once your hands know the moves,
<strong>Part B hands you the same moves to make alone</strong>. If you have used Excel before, this
will be comfortable; if you have not, you cannot get lost, because nothing here is left for you to
guess.</p>

<div class="callout"><strong>Download</strong>
<p style="font-family:var(--sans);font-size:.9rem"><a href="cascadia-sales-2025.xlsx">cascadia-sales-2025.xlsx</a>,
one sheet, one year of sales. Columns you will use today: <code class="inline">C</code> store,
<code class="inline">H</code> quantity, <code class="inline">K</code> revenue.</p></div>

<div class="callout callout-bridge"><strong>From lecture to lab</strong><p><strong>Lab professor's intro (10 min):</strong>
First, announce the rule for the Excel month, plainly: AI is off for Labs 2 through 5, and here is
why, these four labs put Excel in your hands the way scales put a piano in a musician's, and anything
an AI types for you never becomes yours. It comes back in Week 6. Then run Part A live at half speed,
Steps 1 through 5, narrating every click, with the room following along on their own machines. Say
the lab's rhythm out loud: watch it, do it, own it. Nobody starts Part B until their Checkpoint 2 is
green. Early finishers: the stretch callout at the end seeds next week.</p></div>

{redbox("This week that means typing every formula with your own fingers; the goal is that =SUM comes out of them without thought by Friday.")}

<h2><span class="num">Part A</span>Follow along: five steps, together</h2>

<p>Do these in order, exactly as written. Checkpoints 1 and 2 simply confirm your workbook matches
the walkthrough.</p>

<ol>
<li><strong>Step 1 · Save it properly.</strong> Open the download, then File &#8594; Save As, and name
it <code class="inline">LAB2_Last_First.xlsx</code>. Naming files like an analyst is a habit, not a
nicety; you are about to make fourteen of these this quarter.</li>
<li><strong>Step 2 · Make it readable.</strong> Click the triangle above row 1 and left of column A
to select everything, then double-click any boundary between two column letters. Every column snaps
to fit its contents.</li>
<li><strong>Step 3 · Freeze the header and size up the data.</strong> View tab &#8594; Freeze Panes
&#8594; Freeze Top Row, so the column names stay visible while you scroll. Now press Ctrl+End
(<span class="mac">Mac</span> Cmd+Fn+&#8594; then &#8595;) to jump to the data's far corner and note
the row number. <em>Checkpoint 1.</em></li>
<li><strong>Step 4 · Your first formula.</strong> Press Ctrl+Home to return to the top. Click cell
<code class="inline">P1</code> and type the label <code class="inline">Total revenue</code>. Click
<code class="inline">P2</code>, type <code class="inline">=SUM(K:K)</code> exactly, and press Enter.
The cell shows one number; the formula bar still shows your formula. Read the formula as a sentence:
add up everything in column K. <em>Checkpoint 2.</em></li>
<li><strong>Step 5 · The free answers in the status bar.</strong> Click column K's header letter to
select the whole column, then look at the bar along the bottom of the window: Excel is already
showing you Average, Count, and Sum without being asked. Remember this trick; Part B uses it.</li>
</ol>

<details class="howto"><summary>If a step misbehaves</summary><div class="howto-body">
<ol>
<li><strong>Freeze Panes is grayed out:</strong> you are in a cell-editing state; press Esc first.</li>
<li><strong>=SUM shows 0:</strong> you are probably on a different sheet, or typed a letter other than K. Click the cell and read the formula bar.</li>
<li><strong>#NAME? error:</strong> the function name is misspelled. Delete and retype.</li>
<li><strong>The status bar shows nothing:</strong> right-click the status bar itself and check Sum, Average, and Count.</li>
</ol>
</div></details>

<h2><span class="num">Part B</span>Now you: the same moves, alone</h2>

<p>Everything below uses only Steps 4 and 5's moves with different targets. The hints tell you the
pattern; your fingers do the rest.</p>

<ol>
<li><strong>Total units sold.</strong> One formula, one new column letter. <em>Checkpoint 3.</em></li>
<li><strong>Average revenue per line.</strong> New verb, same shape. <em>Checkpoint 4.</em></li>
<li><strong>The leading store.</strong> Put a filter on (click any cell in the data, Data tab &#8594;
Filter), use column C's dropdown to show one store at a time, and read column K's Sum in the status
bar, the Step 5 trick. Work through the stores until you are sure of the winner, then clear the
filter. <em>Checkpoint 5.</em></li>
<li><strong>The biggest single sale.</strong> Sort by revenue if you like the drama, but confirm it
with a formula: MAX works exactly like SUM. <em>Checkpoint 6.</em></li>
</ol>

<div class="callout"><strong>Why a co-op cares about members (a seed for later)</strong>
<p>Column N marks whether each sale had a member attached. Every "N" is a customer the co-op earned
nothing durable from: no relationship, no dividend, no reason to come back. Nobody is asking you to
compute anything with it today, but scroll past it once and remember it exists. You will meet that
column again, and when you do, it will matter more than revenue.</p></div>

<div class="callout callout-good"><strong>Finished early? One stretch</strong>
<p>Select the whole data range and Insert &#8594; Table (Ctrl+T). Notice the filter arrows appear on
their own and formulas start reading like sentences. Then just explore: filter to your favorite
store, read a week of its sales. Familiarity with a dataset is part of analysis, not a delay before
it.</p></div>

{cpblock}
<h2 id="submit"><span class="num">Canvas</span>What to submit</h2>
<p style="font-family:var(--sans);font-size:.92rem">Your workbook as LAB2_Last_First.xlsx with your
labeled formulas, plus your completion certificate PDF (your reflection is page 2 of it).</p>
</main>'''
open('lab2-excel-basics.html','w').write(head+MAIN2+tail)
print('lab2 rebuilt as tutorial:', len(head+MAIN2+tail))

# ================================================== LAB 3 REBUILD (v2, A/B + reorder)
t=open('lab3-excel-dataprep.html').read()
head=t[:t.index('<main id="top">')]
tail=t[t.index('</main>'):]
cpblock=t[t.index('<h2 id="checkpoints"'):t.index('<h2 id="submit"')]

QS3=[
 {"q":"Part A \u00b7 Step 2's formula, exactly as walked through: how many sales lines came from the Bellingham store?","t":"num","a":b64(V['cnt_bham']),"tol":0,
  "h":"=COUNTIF(C:C,\"Bellingham\"), typed in Step 2. Three parts: where to look, what to match."},
 {"q":"Part A \u00b7 Step 3's formula: total revenue from the Portland Pearl store, in dollars?","t":"num","a":b64(V['rev_pp']),"tol":1,
  "h":"=SUMIF(C:C,\"Portland Pearl\",K:K), from Step 3. Look in C, match the store, add up K."},
 {"q":"Part B \u00b7 Your turn, same COUNTIF shape: how many sales lines are in the Snow category?","t":"num","a":b64(V['cnt_snow']),"tol":0,
  "h":"The Part A shape, pointed at the category column instead of the store column. Category lives in F."},
 {"q":"Part B \u00b7 AVERAGEIF: the average revenue per sales line in the Snow category, to the cent?","t":"num","a":b64(V['avg_snow']),"tol":0.05,
  "h":"=AVERAGEIF(where, what, average-this). Same three parts as SUMIF with a different verb. Snow gear is pricey; expect a big number."},
 {"q":"Part B \u00b7 COUNTIFS (plural): how many sales lines at the Tacoma store were member sales (is_member = Y)?","t":"num","a":b64(V['cnt_tacm']),"tol":0,
  "h":"The S version takes pairs: store column with its name, then the is_member column with \"Y\". Two conditions, one count."},
 {"q":"Part B \u00b7 SUMIFS: revenue from Snow-category sales at the Seattle Flagship, in dollars?","t":"num","a":b64(V['rev_ss']),"tol":1,
  "h":"One quirk: in SUMIFS the column being summed goes first, then the condition pairs. Everything else you already know."},
 {"q":"Part B \u00b7 Put two formulas together: what percent of total revenue came from Portland Pearl, to one decimal?","t":"num","a":b64(V['pp_share']),"tol":0.1,
  "h":"Your Part A SUMIF divided by a plain SUM of the revenue column, times 100. Two formulas you own, one number a manager would ask for."},
]
old=re.search(r'QS=(\[.*?\]);',tail,re.S)
tail=tail[:old.start(1)]+json.dumps(QS3)+tail[old.end(1):]

MAIN3 = f'''<main id="top">
<header class="chaphead">
  <p class="eyebrow">Lab 3 · Week 3</p>
  <h1>Excel Functions: One Question, One Formula</h1>
  <div class="meta-row"><span>Lab session · 80 min</span><span class="alt"><a href="chapter3-dominos.html" style="color:inherit;text-decoration:none">Pairs with Chapter 3 · Business Processes &#8594;</a></span></div>
</header>

<p class="lede">Last week you toured the client's workbook and totaled it. This week you interrogate
it. Every business question here has the same three-part shape: which column to look in, what to look
for, and what to do with the rows that match. Same tutorial rhythm as last week: <strong>Part A walks
two formulas keystroke by keystroke</strong>, then <strong>Part B hands you five questions to answer
alone</strong> with the shapes you just learned. Nothing to clean, nothing hidden, no tricks.</p>

<div class="callout"><strong>Download</strong>
<p style="font-family:var(--sans);font-size:.9rem">Same workbook as last week:
<a href="cascadia-sales-2025.xlsx">cascadia-sales-2025.xlsx</a>. If you kept your Lab 2 file, work
there and add a sheet. Columns for today: <code class="inline">C</code> store,
<code class="inline">F</code> category, <code class="inline">K</code> revenue,
<code class="inline">N</code> is_member.</p></div>

<div class="callout callout-bridge"><strong>From lecture to lab</strong><p><strong>Lab professor's intro (10 min):</strong>
Remind the room the Excel-month AI rule is still on, then write the mantra on the board: one
question, one formula. Run Part A live at half speed, narrating COUNTIF's three parts as you type,
where to look, what to match, and (for SUMIF) what to add. Then say the important sentence: every
Part B question is one of these two shapes wearing different columns. Nobody is being tested on
memory; the hints carry the patterns. Early finishers build the summary block in the callout, which
is literally next week's chart data.</p></div>

{redbox("Reading a business question and choosing the right column is the skill here, and choosing is the one thing that cannot be delegated.")}

<h2><span class="num">Part A</span>Follow along: two formulas, together</h2>

<ol>
<li><strong>Step 1 · Set up an answers area.</strong> Click cell <code class="inline">P1</code> and
type <code class="inline">Bellingham lines</code>. Analysts label first, compute second.</li>
<li><strong>Step 2 · COUNTIF, your first question.</strong> In <code class="inline">P2</code>, type
<code class="inline">=COUNTIF(C:C,"Bellingham")</code> and press Enter. Read it the way Excel does:
COUNTIF is the verb, count; C:C is where to look, the store column; "Bellingham" is what to match,
in quotes because it is text. One number appears. <em>Checkpoint 1.</em></li>
<li><strong>Step 3 · SUMIF, one new argument.</strong> Label <code class="inline">Q1</code> as
<code class="inline">Portland Pearl revenue</code>, and in <code class="inline">Q2</code> type
<code class="inline">=SUMIF(C:C,"Portland Pearl",K:K)</code>. Same sentence with a third clause:
look in C, match the store, <em>add up the matching rows of K</em>. <em>Checkpoint 2.</em></li>
</ol>

<p>That is the entire mechanism. Every remaining function today is one of those two sentences with a
different verb or an extra clause:</p>

<table class="lab">
<thead><tr><th>Function</th><th>The question it answers</th><th>Shape</th></tr></thead>
<tbody>
<tr><td><code class="inline">COUNTIF</code></td><td>How many rows match?</td><td>=COUNTIF(where, what)</td></tr>
<tr><td><code class="inline">SUMIF</code></td><td>Add a column, only for matching rows</td><td>=SUMIF(where, what, add-this)</td></tr>
<tr><td><code class="inline">AVERAGEIF</code></td><td>Average a column, only for matching rows</td><td>=AVERAGEIF(where, what, average-this)</td></tr>
<tr><td><code class="inline">COUNTIFS / SUMIFS</code></td><td>Same, with two or more conditions</td><td>pairs of (where, what); SUMIFS puts add-this first</td></tr>
</tbody>
</table>

<details class="howto"><summary>If a formula misbehaves</summary><div class="howto-body">
<ol>
<li><code class="inline">#NAME?</code>: the function name is misspelled. Retype it.</li>
<li><strong>Unexpected 0:</strong> the text does not match the data exactly. Check spelling and that the quotes are straight ("), not curly.</li>
<li><strong>#VALUE? in SUMIFS:</strong> the sum column probably is not first. The S versions reorder the arguments; the table above shows where things go.</li>
</ol>
</div></details>

<h2><span class="num">Part B</span>Now you: five questions, alone</h2>

<p>Each checkpoint below is a Part A shape pointed at new columns. The hints give you the pattern,
never the finished formula; picking the column is the part that has to be yours.</p>

<ol>
<li><strong>How many Snow-category lines?</strong> Part A's first shape, new column. <em>Checkpoint 3.</em></li>
<li><strong>Average revenue per Snow line.</strong> A verb you have not typed yet, in a shape you have. <em>Checkpoint 4.</em></li>
<li><strong>Member sales at Tacoma.</strong> Two conditions at once; reach for the plural. <em>Checkpoint 5.</em></li>
<li><strong>Snow revenue at the Seattle Flagship.</strong> The plural of SUMIF, with its one quirk. <em>Checkpoint 6.</em></li>
<li><strong>Portland Pearl's share of everything.</strong> Divide, multiply by 100, and you have built your first business metric. <em>Checkpoint 7.</em></li>
</ol>

<div class="callout callout-good"><strong>Finished early? Build the summary block</strong>
<p>In a blank area, list the eight store names down a column. Beside each, a COUNTIF for its lines, a
SUMIF for its revenue, and a COUNTIFS for its member lines, filled down. Eight rows, four columns:
you have just hand-built the table every dashboard is secretly made of. Keep it; next week's lab
turns exactly this block into charts.</p></div>

{cpblock}
<h2 id="submit"><span class="num">Canvas</span>What to submit</h2>
<p style="font-family:var(--sans);font-size:.92rem">Your workbook as LAB3_Last_First.xlsx with your
labeled formulas (and the summary block if you built it), plus your completion certificate PDF (your
reflection is page 2 of it).</p>
</main>'''
open('lab3-excel-dataprep.html','w').write(head+MAIN3+tail)
print('lab3 rebuilt as tutorial:', len(head+MAIN3+tail))

# ================================================== LAB 4 RESTRUCTURE
t=open('lab4-excel-dataviz.html').read()
m=re.search(r'(<h2[^>]*><span class="num">Part 2</span>[^<]*</h2>)(.*?)(<details class="howto")', t, re.S)
assert m, 'L4 part2 anchor'
new_open = '''
<p><strong>The first chart we build together, the second is yours.</strong> Same rhythm as Labs 2
and 3: follow Part A's steps exactly, then repeat the moves alone.</p>

<h3>Follow along: revenue by store, as a sorted bar</h3>
<ol>
<li><strong>Step 1.</strong> Click any single cell inside the data, then Insert &#8594; PivotTable
(the how-to below has every click if this is your first pivot). Put <code class="inline">store</code>
in Rows and <code class="inline">revenue</code> in Values.</li>
<li><strong>Step 2.</strong> Click inside the pivot, then Insert &#8594; Recommended Charts &#8594;
Bar (or Column). A chart appears wired to the pivot.</li>
<li><strong>Step 3.</strong> Sort it: right-click any revenue value in the pivot &#8594; Sort &#8594;
Largest to Smallest. The bars fall into order.</li>
<li><strong>Step 4.</strong> Check the axis starts at zero (it will by default; Part 3 shows you why
that matters), then click the title and replace it with a sentence that states the finding, not the
topic: "Seattle Flagship leads; the gap to last place is wide," not "Revenue by Store."
<em>Checkpoints 1 and 2.</em></li>
</ol>

<h3>Now you: revenue by month, as a line</h3>
<p>Repeat the four steps alone with <code class="inline">month</code> in Rows instead of store, and
choose the chart type yourself; Part 1 told you which shape time takes. Twelve points, time on the
horizontal, title that states what the year did. Look at the shape of the co-op's year before moving
on, because you will need it later. <em>Checkpoints 3 and 4.</em></p>

'''
t = t[:m.start(2)] + new_open + t[m.start(3):]
open('lab4-excel-dataviz.html','w').write(t)
print('lab4 restructured: follow-along + now-you')

# ================================================== LAB 5 FRAMING
t=open('lab5-excel-analysis.html').read()
t=t.replace('<span class="num">Part A</span>Skills: pivots as instruments',
            '<span class="num">Part A</span>Follow along, skills: pivots as instruments')
assert 'Follow along, skills' in t
old_pb = re.search(r'<h2[^>]*><span class="num">Part B</span>The mini project[^<]*</h2>', t)
assert old_pb
t = t.replace(old_pb.group(0), old_pb.group(0) + '''
<p><strong>Everything in Part A was rehearsal. From here, the direction comes from you.</strong> The
memo below is the entire brief, exactly as a board would send it, and choosing what to measure is the
assignment. If the cliff feels too sheer, the guided-path ladder underneath it exists for exactly
that moment, and using it is method, not defeat.</p>''')
open('lab5-excel-analysis.html','w').write(t)
print('lab5 framed: rehearsal → yours')

# insert follow-along steps for L5's first pivot right after Part A h2
t=open('lab5-excel-analysis.html').read()
mA=re.search(r'<h2[^>]*><span class="num">Part A</span>[^<]*</h2>', t)
FOLLOW = '''
<h3>Follow along: the member pivot, click by click</h3>
<ol>
<li><strong>Step 1.</strong> Click any cell in the data, Insert &#8594; PivotTable, new worksheet.</li>
<li><strong>Step 2.</strong> Drag <code class="inline">is_member</code> to Rows and
<code class="inline">revenue</code> to Values. Two rows appear, Y and N, with revenue beside each.
The Y row is <em>Checkpoint 1</em>.</li>
<li><strong>Step 3.</strong> Now measure lines instead of dollars: drag <code class="inline">sale_id</code>
to Values (it lands as Count). Right-click a count value &#8594; Show Values As &#8594; % of Column
Total. The Y row's percentage is <em>Checkpoint 2</em>.</li>
<li><strong>Step 4.</strong> Say what you just built, out loud if you like: the share of the co-op's
business that has a member attached. Keep this pivot; the mini project will make you glad you have
it.</li>
</ol>
'''
t = t[:mA.end()] + FOLLOW + t[mA.end():]
open('lab5-excel-analysis.html','w').write(t)
print('lab5 follow-along inserted')

# ================================================== RED LIGHTS EVERYWHERE
swap_ailight('lab2-excel-basics.html', redbox("This week that means typing every formula with your own fingers; the goal is that =SUM comes out of them without thought by Friday.")) if open('lab2-excel-basics.html').read().count('class="ailight')>1 else print('lab2 red already in main')
swap_ailight('lab4-excel-dataviz.html', redbox("And diagnosing a misleading chart with your own eyes is the skill this lab exists to build: the one you will need in a meeting where no AI is open and a vendor's slide looks a little too convincing."))
swap_ailight('lab5-excel-analysis.html', redbox("The investigation is graded on noticing something wrong in data nobody annotated for you, and a borrowed eye defeats the entire point."))

# ================================================== VERIFY + INDEX SYNC
v=open('verify_facts.py').read()
# lab3 checkpoints 2 and 3 swapped (SUMIF PP now second, Snow count third)
mm=re.search(r"('lab3-excel-dataprep\.html': \[)(.*?)(\],\n)", v, re.S)
items=[x.strip() for x in re.split(r',\n', mm.group(2))]
assert len(items)==7, items
items[1],items[2]=items[2],items[1]
v=v.replace(mm.group(0), mm.group(1)+',\n                   '.join(items)+mm.group(3))
open('verify_facts.py','w').write(v); print('verify_facts reordered for lab3')

t=open('index.html').read()
t=t.replace('<h4>Excel Basics: Meeting the Client</h4><p>The engagement opens. 6 checkpoints.</p>',
            '<h4>Excel Basics: Meeting the Client</h4><p>A follow-along tutorial, then the same moves alone. 6 checkpoints.</p>')
t=t.replace('<h4>Excel Functions: One Question, One Formula</h4><p>COUNTIF, SUMIF, and friends on the clean workbook. 7 checkpoints.</p>',
            '<h4>Excel Functions: One Question, One Formula</h4><p>Two formulas walked keystroke by keystroke, five solo. 7 checkpoints.</p>')
open('index.html','w').write(t); print('index cards updated')
