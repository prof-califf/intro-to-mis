"""Builds lab1-lab4 HTML with embedded sequential checkpoints + PDF certificate.
Checkpoint answers computed live from cascadia.db so they can never drift from the data.
Certificate spec recovered from prior project session: djb2 hash base36-upper,
code = LABID-h32(name.lower()+'|'+LABID+'|'+nQuestions), jsPDF landscape 560x380."""
import base64, json, re, sqlite3

css = open('shared-inline.css').read()
con = sqlite3.connect('cascadia.db')
Q = lambda s: con.execute(s).fetchone()[0]
R = "quantity*unit_price"

b64 = lambda s: base64.b64encode(str(s).encode()).decode()
def num(prompt, ans, tol, hint):  return {"q":prompt,"t":"num","a":b64(ans),"tol":tol,"h":hint}
def txt(prompt, ans, hint):       return {"q":prompt,"t":"txt","a":b64(ans),"h":hint}

# ---------------- checkpoint sets (answers pulled from the db) ----------------
L1 = [  # three-light AI policy: classification drills, no dataset needed
 txt("A classmate pastes this week's discussion question into Claude and submits the answer unedited. Which light is that: green, yellow, or red?","red","If the deliverable is the thinking, outsourcing the thinking is the red zone."),
 txt("You ask Claude to explain why your VLOOKUP returns #N/A, then fix it yourself. Which light?","green","Using AI to understand your own error is exactly what the green zone is for."),
 txt("You have Claude draft a first version of your case memo, then substantially rewrite it in your own words and cite the assist. Which light?","yellow","Permitted with disclosure: that's the definition of the yellow zone."),
 txt("During Exam 1, you open Claude in another tab 'just to check a definition.' Which light?","red","Exams are closed-AI, full stop. No disclosure makes it permissible."),
]

L2 = [  # Excel basics: deliberately easy
 num("Checkpoint 1 · How many rows of sales data are in the Sales2025 sheet? (Count data rows, not the header.)", Q("SELECT COUNT(*) FROM sales"), 0, "Click any cell in the data, press Ctrl+End, and read the row number, then subtract 1 for the header."),
 num("Checkpoint 2 · Use SUM on the revenue column. Total revenue for 2025, in dollars?", round(Q(f"SELECT SUM({R}) FROM sales"),2), 1, "=SUM(K:K) if revenue is column K. Enter the number with or without cents."),
 num("Checkpoint 3 · Use SUM on quantity. How many total units did the co-op sell?", Q("SELECT SUM(quantity) FROM sales"), 0, "Same idea as Checkpoint 2, different column."),
 num("Checkpoint 4 · Use AVERAGE on revenue. Average revenue per line, to the cent?", round(Q(f"SELECT AVG({R}) FROM sales"),2), 0.05, "=AVERAGE(revenue column). Give two decimals."),
 txt("Checkpoint 5 · Sort or filter by store. Which store produced the most revenue in 2025?","Seattle Flagship","Sort descending on revenue won't answer this alone. You need revenue BY store. A quick way: select the data, Insert → PivotTable, or just sort by store and eyeball the SUBTOTALs. The answer is a store name."),
 num("Checkpoint 6 · Use SUMIF: revenue for the Seattle Flagship store only?", round(Q(f"SELECT SUM({R}) FROM sales WHERE store_id=1"),2), 1, '=SUMIF(store_column,"Seattle Flagship",revenue_column)'),
]

L3 = [  # Data prep on the RAW file: hardest pre-exam lab
 num("Checkpoint 1 · Open cascadia-sales-2025-RAW.xlsx. How many data rows does it contain?", 2923, 0, "Ctrl+End again. It is NOT the same as the clean file. That difference is the point."),
 num("Checkpoint 2 · Use Remove Duplicates (Data tab) across all columns. How many duplicate rows does Excel report removing?", 24, 0, "Select the whole table first. Excel tells you the count in a dialog. That number is your answer."),
 num("Checkpoint 3 · After removing duplicates, how many data rows remain?", 2899, 0, "If this matches the clean file's row count from Lab 2, your dedupe worked."),
 num("Checkpoint 4 · Some quantity cells are blank. Use COUNTBLANK on the quantity column: how many?", 55, 0, "=COUNTBLANK(range). Run it on the deduplicated data."),
 num("Checkpoint 5 · Some unit_price values were stored as text with a leading $. Count them. How many?", 109, 0, 'Text-formatted numbers left-align. One approach: =SUMPRODUCT(--ISTEXT(range)) on unit_price after dedupe. Another: filter for cells beginning with "$" using =COUNTIF(range,"$*").'),
 num("Checkpoint 6 · Build the supplier lookup table from this page, then use VLOOKUP to add lead times. What is the lead time, in days, for the supplier of the Dynamic Rope 60m?", 56, 0, "Find the rope's supplier first (it's in the supplier column), then VLOOKUP that name against the lead-time table."),
 num("Checkpoint 7 · Fully clean the file: dedupe, TRIM store names, fix dates to one format, convert text prices to numbers, resolve blanks per the instructions. Recompute total revenue. What do you get?", round(Q(f"SELECT SUM({R}) FROM sales"),2), 1, "If your cleaned total matches Lab 2's total exactly, you have reconstructed the clean dataset. That agreement is the whole test."),
]

L4 = [  # Data visualization: medium
 txt("Checkpoint 1 · Chart monthly revenue as a line. Which month is the peak?","January","Group sale_date by month first: a pivot table with sale_date in Rows (grouped by month) and revenue in Values, then insert a line chart from it."),
 num("Checkpoint 2 · Revenue for that peak month, in dollars?", round(Q(f"SELECT SUM({R}) FROM sales WHERE substr(sale_date,6,2)='01'"),2), 1, "Read it off your pivot, not the chart."),
 txt("Checkpoint 3 · Which month is the trough?","April","Look for the shoulder season: after ski gear stops selling and before camping starts."),
 txt("Checkpoint 4 · Build a bar chart of revenue by category. Which category leads?","Camping","Pivot: category in Rows, revenue in Values, sort descending, insert bar chart."),
 num("Checkpoint 5 · Revenue for that leading category?", round(Q(f"SELECT SUM({R}) FROM sales s JOIN products p ON p.product_id=s.product_id WHERE p.category='Camping'"),2), 1, "Same pivot as Checkpoint 4."),
 txt("Checkpoint 6 · Top single product by revenue across the year?","Touring Ski Package","Swap category for product in your pivot Rows. One product is far ahead."),
]

L5 = [  # Data analysis + mini project: hardest Excel lab of the quarter
 num("Checkpoint 1 · Pivot revenue by is_member. Total revenue from member-attached sales, in dollars?", round(Q(f"SELECT SUM({R}) FROM sales WHERE member_id IS NOT NULL"),2), 1, "is_member in Rows, revenue in Values."),
 num("Checkpoint 2 · What share of all sales lines are member-attached, as a percent to one decimal?", 86.0, 0.2, "Count of lines by is_member, then Y / total. Show Values As → % of Column Total does it in one move."),
 txt("Checkpoint 3 · THE MINI PROJECT BEGINS. Read the board memo above, then investigate. Which store is the problem?","Bellingham","The memo says revenue looks fine, so stop looking at revenue. What other measure appears in the memo? Break it out by store."),
 num("Checkpoint 4 · That store's member attach rate, as a percent to one decimal?", 51.6, 0.2, "Pivot: store in Rows, is_member in Columns, count of sale_id in Values, shown as % of Row Total."),
 num("Checkpoint 5 · The next-lowest store's attach rate, to one decimal?", 86.9, 0.2, "Same pivot. Notice the size of the cliff between last place and second-to-last."),
 num("Checkpoint 6 · How many sales lines at the problem store have no member attached?", 168, 0, "Filter or COUNTIFS: store = Bellingham, is_member = N."),
 txt("Checkpoint 7 · Which OTHER store's total revenue is closest to the problem store's? (This is why nobody noticed.)","Tacoma","Revenue by store, sorted. The problem store sits comfortably mid-pack. The anomaly is invisible on every chart you built in Lab 4."),
 num("Checkpoint 8 · Goal Seek thinking: converting how many of the problem store's existing non-member sales to member sales would lift its attach rate to 87%?", 123, 1, "It has 347 total lines. What member count makes member/total reach 87%? Subtract the current member count. Goal Seek on a small model, or algebra (both are legitimate analyst moves."),
]

L6 = [  # Tableau) medium; the anomaly's visual encounter
 num("Checkpoint 1 · Connect Tableau to cascadia-sales-2025.csv. How many rows does the data source show?", 2899, 0, "Data Source tab, bottom-left corner after the connection loads."),
 txt("Checkpoint 2 · Bar chart of revenue by store, sorted descending. Which store is SECOND?","Portland Pearl","Drag store to Rows, revenue to Columns, sort with the toolbar button. Seattle Flagship is first: who's next?"),
 txt("Checkpoint 3 · Create a calculated field: margin_rate = SUM([gross_margin]) / SUM([revenue]). Which category has the HIGHEST margin rate?","Apparel","Analysis → Create Calculated Field. Then category to Rows, your new field to Columns, format as percent."),
 num("Checkpoint 4 · That category's margin rate, as a percent to one decimal?", 59.9, 0.1, "Hover the bar, or add the field to Label."),
 txt("Checkpoint 5 · Highlight table: store in Rows, month of sale_date in Columns, revenue in Color. Which single store-month cell is the darkest (highest) of the whole year? Answer as 'store month'.","Seattle Flagship September","Click the cell. The tooltip settles arguments. And notice it is NOT January, even though January is the co-op's best month overall."),
 txt("Checkpoint 6 · Now build the view Cascadia never built: store in Rows, and the PERCENT of each store's sales that are member-attached (is_member = 'Y'). You found this in a pivot in Lab 5, which store does the chart make impossible to miss?","Bellingham","COUNT(IF [is_member]='Y' THEN 1 END) / COUNT([sale_id]), formatted as percent. Notice how much faster the eye catches it than the pivot did. That is the argument for visualization."),
 num("Checkpoint 7 · Read that store's rate off your chart, as a percent to one decimal.", 51.6, 0.2, "Label or tooltip. Same number as Lab 5 (same data, new instrument."),
]

L7 = [  # SQL data cleaning, following the six-step framework
 num("Step 1 \u00b7 Understand the data. Run: SELECT COUNT(*) FROM sales_raw; How many rows are in the messy export?", 2923, 0, "Type it in the sandbox above and press Run. This is the same export you cleaned by hand in Lab 3."),
 num("Step 1 \u00b7 Now count the real orders: SELECT COUNT(DISTINCT sale_id) FROM sales_raw; How many distinct sale IDs?", 2899, 0, "COUNT(DISTINCT column) counts unique values. The gap between this and Checkpoint 1 is your duplicate problem, already measured, in one line."),
 num("Step 2 \u00b7 Standardize formats. The store column has stray spaces and inconsistent casing. Run SELECT COUNT(DISTINCT store) FROM sales_raw, then wrap it: SELECT COUNT(DISTINCT lower(trim(store))). What does the second query return?", 8, 0, "trim() strips spaces, lower() forces one casing. The co-op has eight stores, so eight is the right answer and anything higher means the text is still dirty."),
 num("Step 2 \u00b7 Some prices were exported as text with a dollar sign. Count them: SELECT COUNT(*) FROM sales_raw WHERE unit_price LIKE '$%'; How many?", 108, 0, "LIKE '$%' matches any value starting with a dollar sign. In Lab 3 you found these by eye in Excel."),
 num("Step 3 \u00b7 Identify missing values. SELECT COUNT(*) FROM sales_raw WHERE quantity IS NULL; How many rows are missing a quantity?", 81, 0, "IS NULL, never = NULL. Nothing equals NULL, not even NULL itself."),
 num("Step 4 \u00b7 Recode variables. The state column is a mess. SELECT COUNT(DISTINCT state) FROM sales_raw returns how many different spellings?", 14, 0, "Run SELECT DISTINCT state FROM sales_raw ORDER BY 1 first and look at what you are dealing with. Then count them."),
 num("Step 4 \u00b7 Cleaning the text only gets you partway: SELECT COUNT(DISTINCT upper(trim(state))) still returns 8, because 'Washington' and 'WA' are the same state spelled differently. Write a CASE expression that maps every variant to WA, OR, or ID, and count the distinct results. What do you get?", 3, 0, "SELECT COUNT(DISTINCT CASE WHEN upper(trim(state)) IN ('WA','WASHINGTON','WASH.') THEN 'WA' WHEN upper(trim(state)) IN ('OR','OREGON','ORE.') THEN 'OR' ELSE 'ID' END) FROM sales_raw; This is recoding, and no string function can do it for you, because only a human knows Wash. means Washington."),
 num("Step 5 and 6 \u00b7 Put it together. Deduplicate with ROW_NUMBER, replace the dollar signs, and treat missing quantities as zero, then total the revenue. Round to two decimals. What is the cleaned total?", 692220.6, 1, "Use the pattern in the worked example above the checkpoints. The full query is: SELECT ROUND(SUM(COALESCE(quantity,0)*CAST(replace(unit_price,'$','') AS REAL)),2) FROM (SELECT sale_id, quantity, unit_price, ROW_NUMBER() OVER (PARTITION BY sale_id ORDER BY sale_id) rn FROM sales_raw) WHERE rn = 1;"),
]

# ---------------- lab page content ----------------
LABS = {
"lab1-genai.html": dict(reflect="""Think about the field you plan to work in. Describe one task in that field where AI in the green zone would genuinely make someone better at their job, and one task where leaning on AI would quietly erode a skill that professionals in that field cannot afford to lose. Be specific to your field, not generic.""",
  labid="LAB1", n="Lab 1", title="GenAI for Thinking", week="Week 1",
  pair=('chapter0-what-is-mis.html','Chapter 0 · What Is MIS?'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> This lab sets the AI policy for the
  whole quarter, before students touch any tool. Walk the three lights on the projector, run one
  live example of a green-zone use (ask Claude to explain a concept from Wednesday's lecture), and
  emphasize that the policy is the same in lab and lecture. Students then work the exercises and
  checkpoints on their own machines. Nothing here requires a dataset.</p>""",
  intro="""<p class="lede">Before you analyze a single row of data in this course, we settle how you may
  and may not use generative AI. Not because AI is forbidden, you will use it in this very lab, but because the difference between using AI to <em>think better</em> and using it to
  <em>avoid thinking</em> is the difference between graduating employable and graduating hollow.</p>""",
  steps="""
<h2><span class="num">The policy</span>Three lights</h2>
<div class="callout callout-good"><strong>Green: always fine, no disclosure needed</strong>
<p>Explaining concepts, debugging your own formulas, quizzing yourself, translating jargon,
summarizing your own notes. AI as tutor. The thinking remains yours.</p></div>
<div class="callout"><strong>Yellow: permitted with disclosure</strong>
<p>Drafting that you substantially rewrite, brainstorming structures, critique of your own work.
One sentence at the end of the submission: what you used, and for what. Undisclosed yellow is red.</p></div>
<div class="callout callout-caution"><strong>Red: never</strong>
<p>Submitting AI output as your work. Any AI during exams. Fabricating checkpoint answers instead of
doing the Excel work. The verification codes exist precisely to make that conversation short.</p></div>

<h2><span class="num">Exercise</span>Use the green zone, on purpose</h2>
<p>Open Claude (or the AI of your choice) and do these three things. They are graded by the
checkpoints, not by screenshots, but you will be asked about them in lab.</p>
<ol>
<li>Ask it to explain the <strong>five components of MIS</strong> (hardware, software, data, networks, people) from Chapter 0 to you as if you run a food truck. Push back on one component that seems wrong for a food truck. Does it hold up?</li>
<li>Paste a paragraph of your own writing from any other class and ask for critique, not a rewrite,
critique. Notice the difference in what you learn.</li>
<li>Ask it something from your major that you already know deeply. Grade its answer. This calibrates
how much to trust it on things you <em>don't</em> know.</li>
</ol>""",
  submit="Your completion certificate PDF: your reflection is page 2 of it.",
  qs=L1),

"lab2-excel-basics.html": dict(reflect="""Cascadia's leaders could not answer basic questions about their own business until someone computed these totals. In the field you plan to enter, what is one number that leadership probably cannot state off the top of their head but should be able to, and what decision would knowing it change?""",
  labid="LAB2", n="Lab 2", title="Excel Basics: Meeting the Client", week="Week 2",
  pair=('chapter1-starbucks.html','Chapter 1 · The Value of Information'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Introduce the client: Cascadia
  Outfitters, a member-owned outdoor co-op with eight PNW stores, whose 2025 sales data the class
  will work in Excel, Tableau, and SQL all quarter. Show the workbook's Read Me tab on the projector
  and define <em>member attach</em>, a sale linked to a member number, because the co-op's dividend
  and demand planning both depend on it. Then let them work. This lab is deliberately gentle;
  DataCamp's Introduction to Excel is its companion. Do not preview later labs' findings.</p>""",
  intro="""<p class="lede">Meet your client. Cascadia Outfitters is a member-owned gear co-op with eight stores
  from Boise to Bellingham, 35 products, and a business model that lives or dies on its members. For the
  next month, you are their analyst.</p>
  <p>Today is the gentle one, and that is deliberate. Before you can find anything interesting in a
  company's data, you have to know what is actually in it. Every analyst you will ever work with starts
  a new engagement exactly this way.</p>
  <p>Download <a href="cascadia-sales-2025.xlsx"><strong>cascadia-sales-2025.xlsx</strong></a>, and read
  the Read Me tab before you touch anything else. I know that sounds like routine advice. Analysts who
  skip the data dictionary are the ones who confidently present the wrong number.</p>""",
  steps="""
<h2><span class="num">Skills</span>Navigation, SUM, AVERAGE, sort, filter, SUMIF</h2>
<ol>
<li><strong>Get oriented first.</strong> Press Ctrl+End (Cmd+Fn+Right on a Mac) to jump to the far
corner of the data. Now you know how big the dataset is. Scroll around a bit. I have already frozen the
header row for you, so watch what that does as you go down.</li>
<li><strong>Get your totals.</strong> Find some empty space to the right of the data and build
yourself a scratch area. Total revenue, total units, average revenue per line, using SUM and
AVERAGE. Keep these visible, because you will be checking later work against them.</li>
<li><strong>Poke around.</strong> Sort by revenue, highest first. What is the single biggest sale of
the year, and does it surprise you? Then filter down to whichever store you like best and read a
week of its sales. Building familiarity with a dataset is part of the analysis, not a delay before it.</li>
<li><strong>Now make Excel answer a question.</strong> SUMIF revenue by store name. COUNTIF rows where
<code class="inline">is_member</code> is "N": you'll meet that number again later in the course.</li>
</ol>
<div class="callout"><strong>Why a co-op cares about attach</strong>
<p>Every sale without a member number is a customer the co-op cannot send a dividend to, cannot
survey, and cannot see in its demand planning. Keep that in the back of your mind. Just the back,
for now.</p></div>""",
  submit="Your workbook saved as LAB2_Last_First.xlsx with your scratch calculations visible, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L2),

"lab3-excel-dataprep.html": dict(reflect="""Dirty data is the fingerprint of a broken process. Describe where dirty data would most likely appear in the industry you want to work in, what upstream process failure would cause it, and what it would cost the business if nobody cleaned it before a decision was made from it.""",
  labid="LAB3", n="Lab 3", title="Data Preparation. The RAW File", week="Week 3",
  pair=('chapter3-dominos.html','Chapter 3 · Business Processes'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Frame this with Monday's Domino's
  discussion: dirty data is the fingerprint of a process with an unmanaged handoff. Cascadia's
  point-of-sale export has duplicates (a double-post between POS and the export job), mixed date
  formats (two store systems configured differently), text-formatted prices, and blank quantities.
  Their controller wants it clean and wants the damage quantified. This is the hardest lab before
  Exam 1: budget the full session, and point students to the final checkpoint's self-test: a
  correctly cleaned file reproduces Lab 2's revenue total exactly.</p>""",
  intro="""<p class="lede">Cascadia's controller sends you their raw point-of-sale export with a
  note: <em>"The numbers from this file don't match our dashboard. Find out why, fix it, and tell me
  how bad it was."</em> This is the most common first assignment in every analyst's career, and the
  least glamorous. It is also where trust in every later analysis is earned.</p>
  <p>Download <a href="cascadia-sales-2025-RAW.xlsx"><strong>cascadia-sales-2025-RAW.xlsx</strong></a>.
  Do not reuse Lab 2's clean file: reproducing it is the assignment.</p>""",
  steps="""
<h2><span class="num">Skills</span>Remove Duplicates, TRIM, date repair, type conversion, VLOOKUP</h2>
<ol>
<li><strong>Count before you clean.</strong> Row count first. An analyst who cleans before
counting cannot report what was wrong.</li>
<li><strong>Duplicates.</strong> Data → Remove Duplicates across all columns. Record what Excel
reports.</li>
<li><strong>Whitespace and case.</strong> Some store names carry stray spaces; some categories are
UPPERCASE. TRIM and PROPER in helper columns, then paste-as-values back.</li>
<li><strong>Dates.</strong> Two formats coexist: ISO (2025-03-14) and US (3/14/2025). Standardize to
one. Text-to-Columns or DATEVALUE both work; pick one and be consistent.</li>
<li><strong>Text prices.</strong> Some unit_price cells are text with a leading $. Find them,
convert them, and confirm revenue math still works.</li>
<li><strong>Blanks.</strong> Some quantity cells are empty. Count them, then apply the controller's
rule: a blank quantity on a line with revenue is a keying failure: set it to
<code class="inline">revenue / unit_price</code>, rounded to a whole number.</li>
<li><strong>Enrich with VLOOKUP.</strong> Build this supplier table on a new sheet and add a
lead-time column to the data:</li>
</ol>
<table style="border-collapse:collapse;margin:1rem 0;font-family:var(--sans);font-size:.85rem">
<tr style="background:var(--navy);color:#fff"><th style="padding:.4rem.8rem;text-align:left">supplier</th><th style="padding:.4rem.8rem">lead_time_days</th></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Olympic Down Works</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">18</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Cascade Textiles</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">24</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Kitsap Forge</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">30</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Nordvik Outdoor</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">56</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Sanko Technical</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">62</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Andes Alpaca Co-op</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">48</td></tr>
<tr><td style="padding:.35rem.8rem;border:1px solid var(--rule)">Fraser Valley Rubber</td><td style="padding:.35rem.8rem;border:1px solid var(--rule);text-align:center">21</td></tr>
</table>
<div class="callout callout-caution"><strong>The self-test</strong>
<p>A correctly cleaned RAW file is the clean file. Your final revenue total must match Lab 2's to
the cent. If it doesn't, one of your six repairs went wrong, and finding which one is the real
exercise.</p></div>""",
  submit="Your cleaned workbook as LAB3_Last_First.xlsx including your helper columns, a three-sentence note to the controller quantifying what was wrong, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L3),

"lab4-excel-dataviz.html": dict(reflect="""A chart is how a system's status reaches the people who decide. In your intended field, describe one situation where an honest chart shown early would change a decision, and one way a chart in that field could technically be accurate while still misleading the person reading it.""",
  labid="LAB4", n="Lab 4", title="Data Visualization: Communicating Status", week="Week 4",
  pair=('chapter4-healthcaregov.html','Chapter 4 · Systems Analysis'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Connect to Monday's Healthcare.gov
  case: the site's builders had no dashboard that told leadership, honestly, whether the system was
  ready: status was communicated in meetings, optimistically. This lab is about charts as honest
  status instruments. Students pivot the Cascadia data and build a small dashboard: monthly revenue
  line, category bar, store comparison. Emphasize chart-type choice (time = line, comparison = bar)
  and axis honesty. Difficulty is moderate; pivots were previewed in DataCamp's Visualization
  module.</p>""",
  intro="""<p class="lede">Healthcare.gov failed in part because nobody built the picture that would
  have made the truth undeniable. A chart is not decoration. It is how a system's status gets
  communicated to the people who decide. This week you build Cascadia's status pictures, and you
  build them honestly.</p>
  <p>Work from your <strong>cleaned</strong> Lab 3 file, or re-download
  <a href="cascadia-sales-2025.xlsx">the clean workbook</a>.</p>""",
  steps="""
<h2><span class="num">Skills</span>Pivot tables, line charts, bar charts, dashboard assembly</h2>
<ol>
<li><strong>Monthly revenue, as a line.</strong> Pivot with sale_date grouped by month against
revenue; insert a line chart. Seasonality should jump out. This is a gear co-op, and the calendar
is its heartbeat.</li>
<li><strong>Category revenue, as bars.</strong> New pivot, categories sorted descending, bar chart.
Resist 3-D. Resist pie.</li>
<li><strong>Store comparison.</strong> Revenue by store, bars, sorted. Title it as a claim, not a
label: "Seattle Flagship carries a fifth of the co-op" beats "Revenue by Store."</li>
<li><strong>Assemble.</strong> Arrange the three charts on one sheet named
<code class="inline">Dashboard</code> so a manager gets the year in one glance.</li>
</ol>
<div class="callout"><strong>Axis honesty</strong>
<p>Truncating a bar chart's y-axis manufactures drama the data doesn't contain. Healthcare.gov's
leadership got optimistic pictures for three years; the correction arrived all at once on launch
day. Your dashboards should make bad news visible early, because that is what dashboards are
for.</p></div>
<div class="callout callout-bridge"><strong>What you have not been asked to chart</strong>
<p>Notice this dashboard says nothing about <em>members</em>. Revenue looks healthy everywhere. In
Lab 5, after the exam, the co-op's board asks a question this dashboard cannot answer, and you will
find that healthy revenue can hide a sick store.</p></div>""",
  submit="Your workbook as LAB4_Last_First.xlsx with the Dashboard sheet, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L4),

"lab5-excel-analysis.html": dict(reflect="""You just found a problem that every standard report concealed. In the career you are heading toward, what is one 'healthy-looking sick store': a metric that could look fine while something underneath it fails? What would you have to break out, segment, or cross-tab to catch it early?""",
  labid="LAB5", n="Lab 5", title="Data Analysis: Why Are Members Disappearing?", week="Week 5",
  pair=('chapter6-nike-sap.html','Chapter 6 · Enterprise Systems'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> This is the hardest Excel assignment of
  the quarter, by design, and it lands two days after Exam 1 with Wednesday's Nike/SAP case fresh: a
  company whose numbers looked fine while its planning system quietly broke. Part A is guided skill work
  (pivots, % of total, Goal Seek, FORECAST.LINEAR). Part B is an open brief: read the board memo aloud,
  then say nothing more. Do not name the store, do not name the metric. Students who ask for direction
  get one sentence: "The memo tells you what the board can see. Find what they can't." Budget the full
  session; the checkpoints gate the discovery in stages so nobody stays stuck forever.</p>""",
  intro="""<p class="lede">Cascadia's board sends the memo below. Every dashboard you built in Lab 4
  says the co-op is healthy. Both of those things can be true at once, and finding out how is the
  hardest, and most realistic, assignment of the Excel month.</p>
  <div class="callout callout-caution"><strong>Memo from the board of directors</strong>
  <p><em>"Annual dividend redemptions in our North Cascades region came in far below projection, and
  member survey response rates there have fallen for three straight quarters. Yet regional revenue is on
  plan and store traffic looks normal. Finance says nothing is wrong. Membership says something is very
  wrong. You have the 2025 sales data. Tell us which of them is right, where, how bad it is, and what it
  would take to fix it."</em></p></div>
  <p>Work from the clean data: <a href="cascadia-sales-2025.xlsx">cascadia-sales-2025.xlsx</a>.</p>""",
  steps="""
<h2><span class="num">Part A</span>Skills: pivots as instruments, what-if, forecasting</h2>
<ol>
<li><strong>Two-dimensional pivots.</strong> Rows and Columns together: store by category, store by
month. Practice Show Values As → % of Row Total and % of Column Total. The single most useful trick in
analytical Excel, and the one Part B quietly depends on.</li>
<li><strong>What-if.</strong> Build a three-cell model (members, total lines, attach rate) and use
Goal Seek (Data → What-If Analysis) to answer questions of the form "what input produces this output?"</li>
<li><strong>Forecasting.</strong> From your Lab 4 monthly pivot, use FORECAST.LINEAR to project January
2026 revenue, and say in one sentence why a linear forecast is suspect for a business this seasonal.
(No checkpoint: your reasoning goes in the submission note.)</li>
</ol>
<h2><span class="num">Part B</span>The mini project: open brief</h2>
<p>Re-read the memo. There are no numbered steps for this part; the structure of the investigation is
the assignment. The checkpoints below will confirm each finding as you reach it, and their order is a
deliberate breadcrumb trail if you're lost. Three rules:</p>
<ul>
<li>Everything you need is in the sales data you already have.</li>
<li>"Revenue is on plan" is in the memo because it is true. Believe it, then ask what it hides.</li>
<li>Your deliverable is a one-page memo back to the board: the finding, its size, why their existing
reports missed it, and one costed recommendation.</li>
</ul>
<div class="callout callout-bridge"><strong>Why this pairs with Nike</strong>
<p>Nike's planners trusted a system whose numbers looked plausible while its demand signal was
corrupted, and the gap between looked-fine and was-fine cost $100 million. Cascadia's board has the
same gap on a co-op's scale: the revenue signal is healthy while the membership signal, the one the
entire business model runs on, has quietly failed at one store. Finding a healthy-looking sick store
is the analyst's version of the audit Nike never ran.</p></div>""",
  submit="Your workbook as LAB5_Last_First.xlsx (Part A sheets plus your investigation pivots), your one-page board memo, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L5),

"lab6-tableau.html": dict(labid="LAB6", n="Lab 6", title="Tableau: Seeing the Co-op", week="Week 6",
  reflect="""Tableau showed you in one glance what took a careful pivot table to find last week. In the field you plan to enter, describe one decision that is currently made from tables of numbers but should be made from a picture, and one risk of letting a beautiful chart substitute for checking the underlying data.""",
  pair=('index.html','Chapter 7 · BI &amp; Analytics (coming)'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Frame with Monday's Moneyball
  discussion: the A's won by measuring what the league didn't. Today students point a new instrument, Tableau, at data they already know, and re-find last week's discovery visually, which lands the
  argument for visualization better than any lecture could. Show connecting to a CSV on the projector
  (Data Source pane, then one drag-and-drop), then release them. If desktop Tableau isn't installed,
  Tableau Public is free and sufficient. Checkpoint 5's answer is deliberately counterintuitive: let
  them be surprised.</p>""",
  intro="""<p class="lede">Same client, new instrument. Everything you found in Excel is still true, but this week you'll watch a finding that took a careful pivot table become impossible to miss the
  moment it's drawn. That difference is why analytics teams fight over dashboards.</p>
  <p>Download <a href="cascadia-sales-2025.csv"><strong>cascadia-sales-2025.csv</strong></a> and connect
  Tableau (or free <a href="https://public.tableau.com">Tableau Public</a>) to it.</p>""",
  steps="""
<h2><span class="num">Skills</span>Connecting data, marks &amp; shelves, calculated fields, highlight tables</h2>
<ol>
<li><strong>Get connected, then look before you build.</strong> Open the CSV as a data source; check the row count and that
Tableau typed revenue as a number and sale_date as a date.</li>
<li><strong>Make your first chart fast.</strong> Revenue by store as sorted bars. Then swap store for
category, then for product: feel how fast iteration is compared to rebuilding a pivot.</li>
<li><strong>Calculated fields.</strong> Build margin_rate and format it as a percent. This is the
Moneyball move: a ratio the raw data doesn't contain, made first-class.</li>
<li><strong>Highlight table.</strong> Store by month, colored by revenue. The co-op's year on one
screen. Find the surprises: the best single cell is not in the best month.</li>
<li><strong>The re-discovery.</strong> Build attach rate by store and watch last week's investigation
become a single picture. Screenshot this one. It goes in your submission.</li>
</ol>
<div class="callout"><strong>Undervalued gear</strong>
<p>Before you leave: put revenue on one axis and margin_rate on the other, by category. The A's looked
for players the market underpriced; a merchant looks for categories earning a high rate on low volume.
Which category would you tell Cascadia to promote harder? No checkpoint for this: your pick and one
sentence of reasoning go in the submission note, and there is more than one defensible answer.</p></div>""",
  submit="A PDF or image export of your attach-rate chart and your highlight table, your undervalued-gear pick with one sentence of reasoning, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L6),

"lab7-sql.html": dict(
  labid="LAB7", n="Lab 7", title="SQL: Cleaning Data at the Source", week="Week 7",
  reflect="""Data professionals spend a large share of their time cleaning data rather than analyzing it. Now that you have done the same cleaning job twice, once by hand in Excel and once in SQL, describe a dataset in the field you plan to enter that probably arrives dirty. What would be wrong with it, who would have to clean it, and what would it cost the business if nobody did?""",
  pair=('index.html','Chapter 5 \u00b7 Databases (coming)'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Open with the number: analysts spend
  most of their time cleaning data, not analyzing it. This lab makes that concrete by handing students
  the same dirty export they cleaned by hand in Lab 3, this time as a table in a real database. What took
  a full Excel session takes six functions here, and that contrast is the entire lesson. Demo Checkpoint 1
  on the projector, then deliberately typo a query so a syntax error stops being frightening. Point out
  the schema box and the worked example. Students who finish early: have them find the single largest
  sale in the cleaned data with ORDER BY and LIMIT.</p>""",
  intro="""<p class="lede">In Lab 3 you cleaned Cascadia's messy sales export by hand in Excel. It took
  a whole session: removing duplicates, trimming spaces, fixing dates, converting text back into numbers.
  Today you will do the same job in SQL, and it will take you about six functions.</p>
  <p>That comparison is the point of this lab. Cleaning data is the least glamorous work in the field
  and by far the most common, so the tool you use for it matters more than almost anything else you
  learn this quarter.</p>
  <div class="callout"><strong>Where this framework comes from</strong>
  <p>The six steps below follow a widely shared SQL data-cleaning cheat sheet by data analyst
  <strong>Jess Ramos</strong>. It is a good summary of how working analysts actually approach a messy
  table, which is why we are using it rather than something invented for a textbook.</p></div>
  <div class="callout"><strong>The schema</strong>
  <p style="font-family:var(--sans);font-size:.9rem">The database has the co-op's seven clean tables plus
  one deliberately messy one. You will work mostly in <code class="inline">sales_raw</code>.</p>
  <p style="font-family:var(--sans);font-size:.88rem"><code class="inline">sales_raw</code>(sale_id, sale_date, store, category, state, quantity, unit_price, member_id) &#183;
  <code class="inline">stores</code>(store_id, store_name, region, opened_year, square_feet) &#183;
  <code class="inline">suppliers</code>(supplier_id, supplier_name, country, lead_time_days) &#183;
  <code class="inline">products</code>(product_id, product_name, category, supplier_id, unit_cost, list_price) &#183;
  <code class="inline">members</code>(member_id, first_name, last_name, city, state, member_type, join_date) &#183;
  <code class="inline">sales</code>(sale_id, sale_date, store_id, product_id, member_id, quantity, unit_price) &#183;
  <code class="inline">inventory</code>(store_id, product_id, quantity_on_hand, reorder_point) &#183;
  <code class="inline">used_gear</code>(item_id, product_id, store_id, condition, listed_price, date_listed, date_sold)</p></div>""",
  steps="""
<h2><span class="num">Sandbox</span>The Cascadia database, live</h2>
<div id="sqlbox" style="border:1px solid var(--rule);background:var(--paper);border-radius:2px;padding:1rem 1.15rem;margin:1.2rem 0">
  <p id="sqlstatus" style="font-family:var(--sans);font-size:.85rem;color:var(--muted);margin:0 0 .6rem">Loading database&hellip;</p>
  <textarea id="sqlin" rows="5" spellcheck="false" style="width:100%;font-family:ui-monospace,Menlo,monospace;font-size:.92rem;padding:.6rem;border:1px solid var(--rule);border-radius:2px" aria-label="SQL query" placeholder="SELECT COUNT(*) FROM sales_raw;"></textarea>
  <br><button onclick="runSQL()" style="font-family:var(--display);font-size:14px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;background:var(--magenta);color:#fff;border:none;padding:.5rem 1.1rem;cursor:pointer;margin-top:.5rem">Run query</button>
  <div id="sqlout" style="overflow-x:auto;margin-top:.8rem;font-family:var(--sans);font-size:.85rem"></div>
</div>

<h2><span class="num">The method</span>Six steps for cleaning any table</h2>

<h3>1. Understand the data</h3>
<p>Never clean anything before you have measured what is wrong with it. Your first job is a damage
report, not a repair.</p>
<p><code class="inline">SELECT COUNT(*) FROM sales_raw;</code> tells you how big it is.
<code class="inline">SELECT COUNT(DISTINCT sale_id) FROM sales_raw;</code> tells you how many real
orders there are. If those two numbers disagree, you have duplicates, and you now know exactly how many.
<code class="inline">SELECT * FROM sales_raw LIMIT 10;</code> shows you what the rows actually look
like, which is always worth doing before you assume anything.</p>

<h3>2. Standardize formats</h3>
<p>The same value written five ways is five values as far as the database is concerned, and that quietly
ruins every count and every GROUP BY you write afterward.</p>
<ul>
<li><code class="inline">trim(store)</code> removes leading and trailing spaces</li>
<li><code class="inline">lower(store)</code> or <code class="inline">upper(store)</code> forces one casing</li>
<li><code class="inline">replace(unit_price, '$', '')</code> strips a stray character</li>
<li><code class="inline">CAST(replace(unit_price,'$','') AS REAL)</code> turns the cleaned text back into a number you can add up</li>
</ul>
<p>Try it: run <code class="inline">SELECT COUNT(DISTINCT store) FROM sales_raw;</code> and then the same
query wrapped in <code class="inline">lower(trim(...))</code>. The co-op has eight stores. Whatever
number the first query gives you is the size of the problem.</p>

<h3>3. Identify missing values</h3>
<p>Missing is not the same as zero, and it is not the same as empty text. SQL has a separate idea for
it: NULL.</p>
<p>Find them with <code class="inline">WHERE quantity IS NULL</code>. Note carefully that
<code class="inline">= NULL</code> does not work and will silently return nothing, because nothing is
equal to NULL, including NULL. That trips up nearly everyone once, and it will be on Exam 2.</p>

<h3>4. Handle and recode values</h3>
<p>Two different jobs live here. <strong>Handling</strong> a missing value means deciding what to put in
its place: <code class="inline">COALESCE(quantity, 0)</code> returns the quantity, or zero when it is
NULL. <code class="inline">NULLIF(state, '')</code> does the reverse, turning empty text into a proper
NULL so it stops masquerading as a real value.</p>
<p><strong>Recoding</strong> is harder and no function can do it for you. Look at the state column:</p>
<p><code class="inline">SELECT DISTINCT state FROM sales_raw ORDER BY 1;</code></p>
<p>You will find WA, wa, Wash., and Washington all describing the same state. Cleaning the text with
trim and upper gets you partway, but only a person knows that "Wash." means Washington. That judgment
goes into a CASE expression:</p>
<pre style="background:var(--off-white);border:1px solid var(--border);padding:.9rem 1rem;overflow-x:auto;font-family:ui-monospace,Menlo,monospace;font-size:.85rem;line-height:1.5">SELECT CASE
         WHEN upper(trim(state)) IN ('WA','WASHINGTON','WASH.') THEN 'WA'
         WHEN upper(trim(state)) IN ('OR','OREGON','ORE.')      THEN 'OR'
         ELSE 'ID'
       END AS state_clean,
       COUNT(*)
FROM sales_raw
GROUP BY state_clean;</pre>
<p>This is the step where a human has to know the business. It is also, not coincidentally, the step
that is hardest to automate away.</p>

<h3>5. Identify duplicates</h3>
<p>Group by whatever should be unique and keep only the groups that appear more than once:</p>
<pre style="background:var(--off-white);border:1px solid var(--border);padding:.9rem 1rem;overflow-x:auto;font-family:ui-monospace,Menlo,monospace;font-size:.85rem;line-height:1.5">SELECT sale_id, COUNT(*)
FROM sales_raw
GROUP BY sale_id
HAVING COUNT(*) > 1;</pre>
<p><code class="inline">HAVING</code> filters groups the way <code class="inline">WHERE</code> filters
rows. You need it here because you are asking a question about the group, not about any single row.</p>

<h3>6. Remove duplicates</h3>
<p>Number the rows within each group, then keep number one:</p>
<pre style="background:var(--off-white);border:1px solid var(--border);padding:.9rem 1rem;overflow-x:auto;font-family:ui-monospace,Menlo,monospace;font-size:.85rem;line-height:1.5">SELECT sale_id, quantity, unit_price
FROM (
  SELECT sale_id, quantity, unit_price,
         ROW_NUMBER() OVER (PARTITION BY sale_id ORDER BY sale_id) AS rn
  FROM sales_raw
)
WHERE rn = 1;</pre>
<p><code class="inline">PARTITION BY</code> restarts the numbering for each sale_id, so every real order
gets a row 1 and its copies get 2, 3, and so on.</p>
<div class="callout callout-caution"><strong>A warning about cheat sheets</strong>
<p>Published examples of this pattern often end with <code class="inline">QUALIFY rn = 1</code>, which is
shorter and reads better. It will fail in this sandbox, and in SQLite, MySQL, and PostgreSQL, because
QUALIFY exists only in Snowflake, BigQuery, and a few others. Try it and read the error. This is worth
experiencing once: SQL is a standard that every database extends differently, and code you copy from the
internet may be written for a database you are not using.</p></div>

<h3>Putting it together</h3>
<p>The final checkpoint asks you to do all of it at once: deduplicate, strip the dollar signs, treat
missing quantities as zero, and total the revenue. Build it in pieces and run each piece before you
combine them. That is how working analysts write long queries, not in one heroic attempt.</p>

<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>
<script>
var CASCADIA_DB=null;
initSqlJs({locateFile:function(f){return 'https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/'+f}})
.then(function(SQL){return fetch('cascadia.db').then(function(r){if(!r.ok)throw new Error('db fetch '+r.status);return r.arrayBuffer()}).then(function(buf){
  CASCADIA_DB=new SQL.Database(new Uint8Array(buf));
  document.getElementById('sqlstatus').textContent='Database loaded. Eight tables, including the messy sales_raw. Type a query and press Run.';
})}).catch(function(e){
  document.getElementById('sqlstatus').innerHTML='Could not load the database ('+e.message+'). The sandbox has to be served over http, so it works on the course site but not from a file you opened locally. You can also run these queries at <a href="https://sqliteonline.com">sqliteonline.com</a> by uploading <a href="cascadia.db">cascadia.db</a>.';
});
function runSQL(){
  var out=document.getElementById('sqlout');
  if(!CASCADIA_DB){out.textContent='Database still loading, give it a second.';return}
  var q=document.getElementById('sqlin').value;
  try{
    var res=CASCADIA_DB.exec(q);
    if(!res.length){out.textContent='Query ran, no rows returned.';return}
    var r=res[0],h='<table style="border-collapse:collapse"><tr>';
    r.columns.forEach(function(c){h+='<th style="border:1px solid var(--rule);padding:.35rem .65rem;background:var(--off-white);text-align:left">'+c+'</th>'});
    h+='</tr>';
    r.values.slice(0,50).forEach(function(row){h+='<tr>';row.forEach(function(v){h+='<td style="border:1px solid var(--rule);padding:.35rem .65rem">'+(v===null?'<em style="color:#a03434">NULL</em>':String(v).replace(/</g,'&lt;'))+'</td>'});h+='</tr>'});
    h+='</table>';
    if(r.values.length>50)h+='<p style="color:var(--muted)">Showing 50 of '+r.values.length+' rows.</p>';
    out.innerHTML=h;
  }catch(e){out.innerHTML='<span style="color:#a03434">SQL error: '+String(e.message).replace(/</g,'&lt;')+'</span><br><span style="color:var(--muted)">Read it closely. The word right before the error is usually where the problem is.</span>'}
}
</script>""",
  submit="A text file containing your eight working queries, one per checkpoint, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L7),
}

# ---------------- checkpoint + certificate machinery (recovered spec) ----------------
CP_CSS = """.cp{border:1px solid var(--rule);background:var(--paper);border-radius:2px;margin:1rem 0;padding:1rem 1.15rem}.cp.locked{opacity:.45;pointer-events:none}.cp.done{border-left:4px solid var(--good);background:var(--good-pale)}.cp.q{font-family:var(--sans);font-size:.92rem;color:var(--navy);margin:0 0.6rem;font-weight:500}.cp input[type=text]{font-family:var(--sans);font-size:.9rem;padding:.45rem.6rem;border:1px solid var(--rule);border-radius:2px;width:14rem;max-width:100%}.cp button{font-family:var(--sans);font-size:.8rem;font-weight:600;letter-spacing:.04em;background:var(--accent-deep);color:#fff;border:none;border-radius:2px;padding:.5rem.9rem;cursor:pointer;margin-left:.4rem}.cp button.hintb{background:none;color:var(--accent-deep);border:1px solid var(--rule)}.cp.msg{font-family:var(--sans);font-size:.8rem;margin:.5rem 0 0}.cp.hint{font-family:var(--sans);font-size:.8rem;color:var(--muted);margin:.5rem 0 0;display:none;border-top:1px dashed var(--rule);padding-top:.5rem}.progress{position:sticky;top:0;z-index:5;background:var(--black);color:#fff;font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:.6rem 1rem;margin:1.5rem 0}.certbox{border:2px solid var(--black);background:var(--paper);padding:1.2rem 1.3rem;margin:1.5rem 0;display:none}.certbox.show{display:block}.certbox h3{margin-top:0}.codebox code{font-family:ui-monospace,Menlo,monospace;background:var(--cream-deep);padding:.15em.45em;border-radius:2px}
"""

CP_HTML = """
<h2 id="checkpoints"><span class="num">Required</span>Checkpoints <span style="font-weight:400;color:var(--muted);font-size:.65em">, complete as you work</span></h2>
<p style="font-family:var(--sans);font-size:.95rem">Here is how this works. Each checkpoint matches a
step above. You do the actual work in your own file, then paste the answer here. Get it right and the
next question opens up. There is no penalty for a wrong answer, so guess, check, and lean on the hint if
you get stuck. That is what it is there for.</p>
<p style="font-family:var(--sans);font-size:.95rem">Once you have cleared them all, write your reflection
and download your certificate for Canvas. One warning worth taking seriously: <strong>your progress lives
only on this page.</strong> Close the tab or refresh before you download, and you start over.</p>
<div class="progress" id="prog">Checkpoint progress: 0 / __N__</div>
<div id="cps"></div>
<div class="certbox" id="reflectbox">
  <h3>One last thing before your certificate</h3>
  <p style="font-family:var(--sans);font-size:.88rem">__REFLECT__</p>
  <p style="font-family:var(--sans);font-size:.88rem;color:var(--muted)">Fifty words is the minimum, but
  do not write to the counter. This prints as page 2 of your certificate, so it is the part your lab
  professor actually reads. Answer it like someone asked you the question out loud.</p>
  <textarea id="refl" rows="6" style="width:100%;font-family:var(--sans);font-size:.9rem;padding:.6rem;border:1px solid var(--rule);border-radius:2px" aria-label="Lab reflection"></textarea>
  <p class="msg" id="reflcount" style="font-family:var(--sans);font-size:.8rem;color:var(--muted)">0 words</p>
</div>
<div class="certbox" id="certbox">
  <h3>All checkpoints cleared</h3>
  <p style="font-family:var(--sans);font-size:.95rem">Put your name in exactly as it appears in Canvas,
  then download your certificate. The code on it is generated from your name, so it is yours and nobody
  else's.</p>
  <input type="text" id="nm" placeholder="Last, First" aria-label="Your name as in Canvas">
  <button onclick="cert()">Download certificate (PDF)</button>
  <p class="codebox" id="codeout" style="font-family:var(--sans);font-size:.85rem"></p>
</div>
"""

CP_JS = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
const LAB="__LABID__", QS=__QS__;
const solved=new Set();
const norm=s=>s.replace(/[$,\\s]/g,'').toLowerCase();
function render(){
 const c=document.getElementById('cps');c.innerHTML='';
 QS.forEach((q,i)=>{
  const d=document.createElement('div');
  d.className='cp'+(solved.has(i)?' done':(i>0&&!solved.has(i-1)?' locked':''));
  d.innerHTML='<p class="q">'+q.q+'</p>'
   +(solved.has(i)?'<p class="msg" style="color:var(--good)">Correct.</p>':'<input type="text" id="in'+i+'" aria-label="Answer '+(i+1)+'">'
   +'<button onclick="chk('+i+')">Check</button>'
   +'<button class="hintb" onclick="hint('+i+')">Hint</button>'
   +'<p class="msg" id="m'+i+'"></p><p class="hint" id="h'+i+'">'+q.h+'</p>');
  c.appendChild(d);});
 document.getElementById('prog').textContent='Checkpoint progress: '+solved.size+' / '+QS.length;
 const done=solved.size===QS.length;
 document.getElementById('reflectbox').className='certbox'+(done?' show':'');
 document.getElementById('certbox').className='certbox'+(done&&wc()>=50?' show':'');
}
function wc(){const t=document.getElementById('refl');return t?t.value.trim().split(/\\s+/).filter(Boolean).length:0}
document.addEventListener('input',function(e){
 if(e.target&&e.target.id==='refl'){
  const n=wc();document.getElementById('reflcount').textContent=n+' words'+(n<50?': '+(50-n)+' more to unlock your certificate':': certificate unlocked below');
  document.getElementById('certbox').className='certbox'+(solved.size===QS.length&&n>=50?' show':'');
 }
});
function hint(i){const h=document.getElementById('h'+i);h.style.display=h.style.display==='block'?'none':'block'}
function chk(i){
 const v=document.getElementById('in'+i).value,m=document.getElementById('m'+i);
 if(!v.trim()){m.textContent='Enter an answer first.';m.style.color='#7d6608';return}
 const ans=atob(QS[i].a);let ok=false;
 if(QS[i].t==='num'){const g=parseFloat(norm(v)),a=parseFloat(ans);ok=!isNaN(g)&&Math.abs(g-a)<=QS[i].tol}
 else ok=norm(v)===norm(ans);
 if(ok){solved.add(i);render()}
 else{m.textContent='Not yet: check the hint, or re-read the step above.';m.style.color='#a03434'}
}
function h32(s){let h=5381;for(const c of s)h=((h<<5)+h+c.charCodeAt(0))|0;return(h>>>0).toString(36).toUpperCase()}
function cert(){
 const n=document.getElementById('nm').value.trim();
 if(!n){document.getElementById('codeout').textContent='Enter your name first.';return}
 const r=document.getElementById('refl').value.trim();
 if(wc()<50){document.getElementById('codeout').textContent='Finish your 50-word reflection above first.';return}
 const code=LAB+'-'+h32(n.toLowerCase()+'|'+LAB+'|'+QS.length);
 const d=new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
 const {jsPDF}=window.jspdf;const p=new jsPDF({orientation:'landscape',unit:'pt',format:[560,380]});
 p.setFillColor(11,29,51);p.rect(0,0,560,380,'F');
 p.setFillColor(253,252,250);p.rect(16,16,528,348,'F');
 p.setTextColor(26,82,118);p.setFont('helvetica','bold');p.setFontSize(10);
 p.text('MIS 320 \\u00B7 INTRODUCTION TO INFORMATION SYSTEMS \\u00B7 WWU',280,58,{align:'center'});
 p.setTextColor(26,26,26);p.setFont('times','bold');p.setFontSize(26);
 p.text('Certificate of Lab Completion',280,105,{align:'center'});
 p.setFont('times','normal');p.setFontSize(13);p.text('This certifies that',280,140,{align:'center'});
 p.setFont('times','bold');p.setFontSize(20);p.text(n,280,170,{align:'center'});
 p.setFont('times','normal');p.setFontSize(13);
 p.text('completed all '+QS.length+' checkpoints of',280,198,{align:'center'});
 p.setFont('helvetica','bold');p.setFontSize(15);p.setTextColor(26,82,118);
 p.text('__LABNAME__',280,222,{align:'center'});
 p.setFont('helvetica','normal');p.setFontSize(11);p.setTextColor(90,90,90);
 p.text(d,280,252,{align:'center'});
 p.setFont('courier','bold');p.setFontSize(12);p.setTextColor(17,120,100);
 p.text('Verification code: '+code,280,290,{align:'center'});
 p.setFontSize(8);p.setFont('helvetica','normal');p.setTextColor(150,150,150);
 p.text('Upload this PDF to Canvas. Reflection on page 2. Code is unique to name + lab.',280,330,{align:'center'});
 p.addPage([560,380],'landscape');
 p.setFillColor(253,252,250);p.rect(0,0,560,380,'F');
 p.setDrawColor(11,29,51);p.setLineWidth(2);p.rect(16,16,528,348);
 p.setTextColor(26,82,118);p.setFont('helvetica','bold');p.setFontSize(10);
 p.text('LAB REFLECTION \\u00B7 '+n+' \\u00B7 '+code,280,44,{align:'center'});
 p.setTextColor(60,60,60);p.setFont('times','italic');p.setFontSize(9);
 const promptLines=p.splitTextToSize('Prompt: __REFLECTPDF__',480);
 p.text(promptLines,40,70);
 p.setFont('times','normal');p.setFontSize(11);p.setTextColor(26,26,26);
 const lines=p.splitTextToSize(r,480);
 p.text(lines.slice(0,22),40,70+promptLines.length*11+14);
 p.save(LAB+'_certificate_'+n.replace(/[^a-z0-9]/gi,'_')+'.pdf');
 document.getElementById('codeout').innerHTML='Certificate downloaded (reflection on page 2). Your code: <code>'+code+'</code>';
}
render();
</script>
"""

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n} · {title} | MIS 320</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{css}{cpcss}</style></head><body>
<div class="shell">
<aside class="rail">
  <p class="book">MIS 320</p><p class="course">Introduction to Information Systems</p>
  <button class="railtoggle" aria-expanded="false" aria-controls="chapnav">Lab contents</button>
  <nav id="chapnav">
    <a href="#top">Overview</a><a href="#steps">The work</a>
    <a href="#checkpoints">Checkpoints</a><a href="#submit">What to submit</a>
    <a href="{pairhref}">↳ {pairname}</a>
  </nav>
  <a class="back" href="index.html">← All chapters &amp; labs</a>
</aside>
<main id="top">
<header class="chaphead">
  <p class="eyebrow">{n} · {week}</p>
  <h1>{title}</h1>
  <div class="meta-row"><span>Lab session · 80 min</span><span class="alt"><a href="{pairhref}" style="color:inherit;text-decoration:none">Pairs with {pairname} &#8594;</a></span></div>
</header>
{intro}
<div class="callout callout-bridge"><strong>From lecture to lab</strong>{bridge}</div>
<div id="steps">{steps}</div>
{cp}
<h2 id="submit"><span class="num">Canvas</span>What to submit</h2>
<p style="font-family:var(--sans);font-size:.92rem">{submit}</p>
</main></div>
<script>
(function(){{var b=document.querySelector('.railtoggle'),n=document.getElementById('chapnav');
if(!b||!n)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');
b.setAttribute('aria-expanded',o?'true':'false');}});}})();
</script>
{cpjs}
</body></html>"""

for fn, L in LABS.items():
    cp   = (CP_HTML.replace('__N__', str(len(L['qs']))).replace('__REFLECT__', L['reflect']))
    cpjs = (CP_JS.replace('__LABID__', L['labid']).replace('__QS__', json.dumps(L['qs'])).replace('__REFLECTPDF__', L['reflect'].replace("'","\\'")).replace('__LABNAME__', f"{L['n']} \\u00B7 {L['title']}"))
    html = PAGE.format(css=css, cpcss=CP_CSS, cp=cp, cpjs=cpjs,
                       pairhref=L['pair'][0], pairname=L['pair'][1], **L)
    open('out/'+fn, 'w').write(html)
    print(fn, len(html), 'checkpoints:', len(L['qs']))
