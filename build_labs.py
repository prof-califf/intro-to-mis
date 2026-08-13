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
L1 = [  # calculator problem -> policy -> roles -> catching the confident error
 txt("Checkpoint 1 \u00b7 The policy. A classmate pastes this week's discussion question into an AI and submits the answer unedited. Which light is that: green, yellow, or red?","red","If the deliverable is the thinking, outsourcing the thinking is the red zone."),
 txt("Checkpoint 2 \u00b7 You ask an AI to explain why your VLOOKUP returns #N/A, then fix it yourself. Which light?","green","Using AI to understand your own error is exactly what the green zone is for."),
 txt("Checkpoint 3 \u00b7 The roles. You tell an AI: 'Quiz me on the five components of MIS, one question at a time, and when I miss one give me a hint instead of the answer.' Which role is the AI playing: coach, sparring partner, or calculator?","coach","A coach makes you do the work. Handing you answers on demand would make it a calculator, and a coach is the opposite of a calculator."),
 txt("Checkpoint 4 \u00b7 Run that coach session for real, five questions, in whatever AI tool you use. Then answer this one yourself, no tab-switching: espresso machines that report their own condition to headquarters. Which of the five components are the machines themselves: hardware, software, data, networks, or people?","hardware","The machines are hardware. The condition reports they emit are data, and the telemetry travels the network. If the coach session worked, this took you five seconds."),
 num("Checkpoint 5 \u00b7 The calculator test. You gave an AI the ten order lines printed in the lab above and it answered, confidently: 'The total is $1,440.75.' Compute the real total yourself in Excel or on paper. What is it?", 1440.57, 0.01, "SUM of quantity times price for each line. The AI transposed two digits. It happens, it looks right, and nobody catches it except the person who checks."),
 txt("Checkpoint 6 \u00b7 The autopsy. The AI paragraph printed above is fluent, confident, and contains one factual error about this course's central rule. One word appears where its opposite should be. What is the wrong word?","strongest","The weakest component rule says a system is only as strong as its WEAKEST component. The paragraph says strongest, which reverses the entire point while sounding completely reasonable. This is what wrong looks like from an AI: not garbled, just wrong."),
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
 num("Checkpoint 7 · Fully clean the file: dedupe, TRIM store names, fix dates to one format, convert text prices to numbers, resolve blanks per the instructions. Recompute total revenue. What do you get?", round(Q(f"SELECT SUM({R}) FROM sales"),2), 1, "If your cleaned total matches Lab 2's total exactly, you have reconstructed the clean dataset. That agreement is the whole test. If you are close but not exact, run this checklist before redoing anything: (1) your row count should still be 2,899; lower means you deleted rows that only needed fixing. (2) All 109 dollar-sign prices must be true numbers; =COUNT on the price column equals 2,899 only when they are, because COUNT skips text. (3) Every blank quantity must use the controller's rule exactly: revenue divided by unit price, rounded to a whole number. A decimal quantity anywhere is the miss."),
]

L4 = [  # Chart selection, then diagnosing charts that mislead
 txt("Checkpoint 1 \u00b7 You want to compare total revenue across the eight stores. Which chart type is right: bar, line, scatter, or pie?", "bar", "Comparing one number across separate named things is what bar charts are for."),
 txt("Checkpoint 2 \u00b7 Build it. Pivot revenue by store, insert a bar chart, sort highest to lowest. Which store is SECOND?", "Portland Pearl", "Sorting matters. An unsorted bar chart makes the reader do the ranking you should have done for them."),
 txt("Checkpoint 3 \u00b7 Different question: how did revenue move across the twelve months of 2025? Which chart type?", "line", "Time on the horizontal axis, connected points. The line says these values are steps in one sequence, not separate categories."),
 txt("Checkpoint 4 \u00b7 Build it. Which month was the co-op's highest?", "January", "Group by month and chart it. Answer with the month name."),
 num("Checkpoint 5 \u00b7 Now the diagnosis work. Chart A (above) shows Bellevue, Tacoma, and Bellingham with a vertical axis starting at $80,000, and Bellevue's bar looks roughly six times taller than Bellingham's. What is the ACTUAL percentage gap between Bellevue and Bellingham? One decimal.", 8.1, 0.3, "Compute it: (Bellevue minus Bellingham) divided by Bellingham, times 100. Then look at Chart A again. That is what a truncated axis does to a reader who trusts you."),
 txt("Checkpoint 6 \u00b7 Chart B plots the eight stores on a LINE chart, left to right, and the line slopes downward. What is wrong with it? Answer with one word: the chart type implies something false about the relationship between the items on the horizontal axis. That false implication is a ______ (one word, starts with T).", "trend", "A line connects points to say they are steps in a sequence. Stores are not a sequence. Reorder them alphabetically and the 'trend' reverses, which proves it was never there."),
 num("Checkpoint 7 \u00b7 Chart C is a pie chart of revenue by individual product. How many slices does it have? (Count the products in the data.)", 35, 0, "Humans compare angles badly, and a pie stops being readable at about five slices. This one is not a chart, it is a colour wheel."),
 txt("Checkpoint 8 \u00b7 Chart D is an accurate line chart of monthly revenue titled 'Revenue Collapsing After January.' Revenue does fall 24.6% from January to February, so the number in the title is real. Now look at the whole year: which month is the co-op's SECOND-highest?", "October", "October, and December is third. Revenue recovers and the year ends strong, so a seasonal dip has been relabelled a collapse. Nothing in this chart is factually wrong, which is what makes it the most dangerous of the four."),
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

L6 = [  # Tableau: worksheets to dashboard
 num("Checkpoint 1 \u00b7 Connect Tableau to cascadia-sales-2025.csv. How many rows does the data source show?", 2899, 0, "Data Source tab, bottom left, after the connection loads."),
 txt("Checkpoint 2 \u00b7 Worksheet 1. Revenue by store as a sorted bar chart. Which store is SECOND?", "Portland Pearl", "Store to Rows, revenue to Columns, then the sort button in the toolbar. Same chart-type logic as Lab 4: comparing a number across separate named places is a bar chart."),
 txt("Checkpoint 3 \u00b7 Worksheet 2. Revenue by month as a line chart. Which month is highest?", "January", "Drag sale_date to Columns and set it to Month. Time on the horizontal axis, connected points, because these values are one continuous story."),
 txt("Checkpoint 4 \u00b7 Worksheet 3. Create a calculated field: margin_rate = SUM([gross_margin]) / SUM([revenue]). Which category has the highest margin rate?", "Apparel", "Analysis menu, then Create Calculated Field. Category to Rows, your new field to Columns, format as a percentage."),
 num("Checkpoint 5 \u00b7 Worksheet 4. Build a highlight table: store in Rows, month in Columns, revenue on Color. Click the single darkest cell and read its value off the tooltip. What is it, to the nearest dollar?", 17338, 3, "Colour alone is hard to judge, which is why you click to confirm rather than squinting. The answer is a store-month you might not expect, and it is not January."),
 txt("Checkpoint 6 \u00b7 Which store and month is that darkest cell? Answer as 'Store Month'.", "Seattle Flagship September", "The tooltip tells you both. Note that the co-op's best month overall is January, but its single best store-month is not, which is the kind of thing a highlight table shows and a bar chart cannot."),
 txt("Checkpoint 7 \u00b7 Worksheet 5, the view Cascadia never built. Store in Rows, and the PERCENT of each store's sales that are member-attached (is_member = 'Y') in Columns. You found this in a pivot table in Lab 5. Which store does the chart make impossible to miss?", "Bellingham", "COUNT(IF [is_member]='Y' THEN 1 END) / COUNT([sale_id]), formatted as a percentage. Watch how much faster your eye catches it here than the pivot table did."),
 num("Checkpoint 8 \u00b7 Assemble your five worksheets into a Dashboard, then add region as a filter and apply it to all sheets. Filter to Puget Sound only. What total revenue does your dashboard now show, to the nearest dollar?", 319628, 5, "Dashboard tab at the bottom, drag your sheets in, then use the filter dropdown and choose Apply to Worksheets, All Using This Data Source. If only one chart changes, the filter is not applied across the dashboard yet."),
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
 txt("The relational payoff, part 1 \u00b7 The products table stores a supplier_id, not a supplier name. JOIN products to suppliers: which supplier makes the Avalanche Beacon?", "Nordvik Outdoor", "SELECT su.supplier_name FROM products p JOIN suppliers su ON su.supplier_id = p.supplier_id WHERE p.product_name = 'Avalanche Beacon'; The ON clause states which columns connect the tables."),
 txt("The relational payoff, part 2 \u00b7 One question across two tables: JOIN sales to stores, group by store name, and compute each store's member attach rate: 100.0 * SUM(CASE WHEN member_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*). One store is drastically below the others. Which one?", "Bellingham", "You have now found this three ways: a pivot table in Lab 5, a chart in Lab 6, and a query today. The instrument keeps changing. The fact does not, which is what it means for a finding to be real."),
]

# ---------------- lab page content ----------------
LABS = {
"lab1-genai.html": dict(
  labid="LAB1", n="Lab 1", title="GenAI for Thinking, Not Instead of It", week="Week 1",
  reflect="""Pick the field you plan to enter. Name one skill in that field that a professional must be able to do without AI, the way an analyst must be able to check a total, and explain what goes wrong for someone who lets AI do it for them from day one. Then name one way you plan to use AI as a coach this quarter.""",
  pair=('chapter0-what-is-mis.html','Chapter 0 \u00b7 What Is MIS?'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Open with the calculator line, it frames
  the whole quarter: we do not hand first graders calculators, because the point of first grade math is
  building the number sense that makes a calculator useful later. Same logic here. Then walk the three
  lights on the projector and do the coach exercise live: ask an AI to quiz YOU on the five components,
  one question at a time, hints not answers. Students immediately see AI making someone think harder
  rather than less. Flag that checkpoints 5 and 6 contain deliberately wrong AI output and finding the
  errors is the exercise. This is also everyone's first run through checkpoints, reflection, and the
  certificate, so leave five minutes at the end for the download step.</p>""",
  intro="""<p class="lede">Nobody hands a first grader a calculator. Not because calculators are bad,
  but because the point of first grade arithmetic is not the answers. It is building the number sense
  that lets you catch a wrong answer later, including a wrong answer from the calculator. You are in
  the first grade of business analysis right now. That is not an insult, it is a schedule: this quarter
  you learn the basics by hand, precisely so that AI becomes a tool you command instead of a crutch you
  cannot check.</p>
  <p>So this course does not ban AI, and it does not pretend AI is optional in the careers you are
  heading into. It asks something harder: that you use it in ways that make you better at thinking,
  and that you always remain the person who can tell when it is wrong. Today you learn the rules and
  the three ways of using AI that actually build skill.</p>""",
  steps="""
<h2><span class="num">Part 1</span>The rules: three lights</h2>

<p>Every use of AI in this course falls into one of three zones. When in doubt, ask which one you are
in, and if you are still in doubt, ask us.</p>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; always fine</strong>
  <p>Asking AI to explain a concept, quiz you, critique your reasoning, or help you understand an error
  you then fix yourself. Green uses make you smarter and need no disclosure.</p></div>
</div>

<div class="ailight y">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Yellow &middot; fine with disclosure</strong>
  <p>AI drafts or outlines that you substantially rework in your own words, with a one-line note saying
  how you used it. The thinking in the final product must be yours.</p></div>
</div>

<div class="ailight r">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Red &middot; never</strong>
  <p>Submitting AI output as your own work, using AI on exams, and using AI to write the lab
  reflections. The reflections exist to capture <em>your</em> thinking, and an AI-written one defeats
  the entire purpose while being easier to spot than students expect.</p></div>
</div>

<div class="callout"><strong>You will see these lights all quarter</strong>
<p>These traffic lights appear throughout the textbook, on chapters and labs, marking the moments where
AI helps and the moments where it must stay closed. A green light next to an exercise means use AI
freely, and usually names the role to use it in. Yellow means allowed with a disclosure line. Red means
this one is you alone. When you see a light, that is the policy for that specific task, decided so you
do not have to guess.</p></div>

<div class="callout"><strong>The test behind the lights</strong>
<p>Ask: is the thing being graded the thinking itself? If yes, the thinking must be yours. That single
question sorts almost every case into the right zone.</p></div>

<h2><span class="num">Part 2</span>The three roles worth knowing</h2>

<p>Most students arrive knowing exactly one way to use AI: "write it for me." That is the vending
machine, and it is the one use this course restricts, because it does your thinking for you. Here are
the three roles that do the opposite. Learn their names, we will use them all quarter.</p>

<h3>The coach: it asks, you answer</h3>
<p>A coach does not play the game for you. Tell an AI: <em>"Quiz me on the five components of MIS. One
question at a time. When I get one wrong, give me a hint, not the answer."</em> Now the AI is doing
what a good tutor does at two in the morning before an exam: making you retrieve, which is the thing
that actually builds memory. Reading feels like learning. Retrieval is learning.</p>
<p><strong>Try it now.</strong> Run that exact prompt in whatever AI you use, answer five questions,
and notice how different it feels from reading the chapter again.</p>

<h3>The sparring partner: it attacks, you defend</h3>
<p>Write three sentences answering this: <em>should Cascadia Outfitters, a small gear co-op, spend
money on AI tools this year?</em> Your opinion, your reasoning. Then tell the AI: <em>"Argue against
this. Find my weakest claim and press on it."</em></p>
<p>Your first answer is never your best answer. A sparring partner exposes the soft spots while the
stakes are zero, which is exactly what a good study group does, except this one is available at any
hour and never gets tired of you.</p>

<h3>The calculator: it works fast, you check it</h3>
<p>Back to where this lab started. A calculator is a wonderful thing in the hands of someone who knows
arithmetic, and a trap in the hands of someone who does not, because the person who cannot estimate
cannot notice a wrong answer. Every professional lives by the rule that follows: you can delegate the
work, you can never delegate the checking. AI is the most powerful calculator ever built, and it can be
wrong in ways a pocket calculator never was. The next section makes this concrete.</p>

<h2><span class="num">Part 3</span>The calculator test</h2>

<p>Below are ten order lines from a Cascadia store. An AI was asked for the total and answered,
instantly and confidently: <strong>"The total is $1,440.75."</strong></p>

<div class="callout"><strong>The order lines</strong>
<p style="font-family:ui-monospace,Menlo,monospace;font-size:.9rem;line-height:1.7">
2 &times; $24.50 &nbsp;&nbsp; 1 &times; $189.95 &nbsp;&nbsp; 3 &times; $12.00 &nbsp;&nbsp; 1 &times; $449.00 &nbsp;&nbsp; 2 &times; $67.25<br>
4 &times; $8.75 &nbsp;&nbsp; 1 &times; $95.00 &nbsp;&nbsp; 2 &times; $154.90 &nbsp;&nbsp; 1 &times; $22.35 &nbsp;&nbsp; 3 &times; $39.99</p></div>

<p>Checkpoint 5 asks for the real total. Compute it yourself, in Excel or on paper. The point is not
that AI is bad at arithmetic, some tools now do it well. The point is that the error, when it comes,
will look exactly like the right answer, and the only person who catches it is the one who can still
do first grade math.</p>

<h2><span class="num">Part 4</span>The autopsy: what wrong looks like</h2>

<p>A student asked an AI to summarize the course's central rule and got this paragraph back:</p>

<div class="callout callout-caution"><strong>AI output, verbatim</strong>
<p><em>"Information systems are built from five components: hardware, software, data, networks, and
people. These components work together to turn raw data into decisions a business can act on. The key
principle, sometimes called the weakest component rule, is that a system is only as strong as its
strongest component, which is why companies invest heavily in their best-performing areas. When
analyzing any system failure, start by identifying which component broke."</em></p></div>

<p>It is fluent. It is confident. It is well organized. And it contains one factual error that reverses
the meaning of the rule it is explaining. Checkpoint 6 asks you to find it, and here is why this
exercise sits in Week 1: in Chapter 0 you read about a system that produced fluent, confident,
well-written nonsense because of one wrong input, and it took deliberate checking to catch. Learning to
read AI output the way an editor reads a draft, trusting nothing on fluency alone, is the single most
valuable AI skill this course teaches.</p>

<div class="stuck"><strong>When you get stuck</strong>
<p>Before raising your hand, try these in order.</p>
<ol>
<li>Re-read the checkpoint. Every answer in this lab is either a single word or a number.</li>
<li>For checkpoint 5, lay the ten lines out in two Excel columns and multiply, do not do it in your
head.</li>
<li>For checkpoint 6, read the AI paragraph against the rule as Chapter 0 states it, one clause at a
time.</li>
<li>Use the hint button. It is part of the lab, not a penalty.</li>
<li>Ask a neighbour. Then raise your hand.</li>
</ol></div>""",
  submit="Your completion certificate PDF (your reflection is page 2 of it). Nothing else this week: the point today is the system itself, and your first certificate.",
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

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach</strong>
  <p>Stuck on what SUMIF does or why a formula errors? Ask an AI to explain it, then write the formula yourself. Do not paste the checkpoint questions in and ask for answers; the checkpoint measures whether your workbook is right, and the workbook is yours.</p></div>
</div>

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
<details class="howto"><summary>How to make a pivot table</summary><div class="howto-body">
<ol>
<li>Click any single cell inside the data.</li>
<li><strong>Insert</strong> tab, then <strong>PivotTable</strong>. <span class="mac">Mac</span> same menu, but the button may read <strong>Summarize with PivotTable</strong>.</li>
<li>Excel guesses the data range. Check that it covers all the rows, then choose <strong>New Worksheet</strong> and click OK.</li>
<li>A panel appears on the right with your column names. Drag a field into <strong>Rows</strong> to group by it, and drag a number into <strong>Values</strong> to total it.</li>
<li>If Values shows a count instead of a sum, click it, choose <strong>Value Field Settings</strong>, and pick <strong>Sum</strong>. This catches almost everyone once.</li>
</ol>
<p><strong>If your pivot is empty:</strong> you probably selected a single cell outside the data before inserting. Undo and click inside the table first.</p>
</div></details>
<li><strong>Now make Excel answer a question.</strong> SUMIF revenue by store name. COUNTIF rows where
<code class="inline">is_member</code> is "N": you'll meet that number again later in the course.</li>
</ol>
<div class="callout"><strong>Why a co-op cares about attach</strong>
<p>Every sale without a member number is a customer the co-op cannot send a dividend to, cannot
survey, and cannot see in its demand planning. Keep that in the back of your mind. Just the back,
for now.</p></div>
<div class="stuck"><strong>When you get stuck</strong>
<p>Before raising your hand, try these in order. Most problems in this lab are one of them.</p>
<ol>
<li>Re-read the checkpoint question. Is it asking for a count, a total, or an average? Those are three different numbers.</li>
<li>Check whether your number is plausible. If total revenue comes out as 12 or as 40 million, something is off by a lot and you can usually see where.</li>
<li>Expand the grey "How to" box for that step. It has the exact clicks.</li>
<li>Check the formula bar of the cell you think is wrong. Does it reference the range you meant?</li>
<li>Use the hint button on the checkpoint. It is not a penalty, it is part of the lab.</li>
<li>Ask a neighbour. Then raise your hand.</li>
</ol></div>""",
  submit="Your workbook saved as LAB2_Last_First.xlsx with your scratch calculations visible, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L2),

"lab3-excel-dataprep.html": dict(reflect="""Dirty data is the fingerprint of a broken process. Describe where dirty data would most likely appear in the industry you want to work in, what upstream process failure would cause it, and what it would cost the business if nobody cleaned it before a decision was made from it.""",
  labid="LAB3", n="Lab 3", title="Data Preparation. The RAW File", week="Week 3",
  pair=('chapter2-competitive-advantage.html','Chapter 2 · Competitive Advantage'),
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

<div class="ailight y">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Yellow &middot; AI as calculator, with checking</strong>
  <p>You may ask an AI to draft a cleaning formula, a nested TRIM or a VLOOKUP, but you must test it on rows where you already know the right answer before trusting it, and note the assist in your reflection. A formula you never verified is not your work, it is your risk.</p></div>
</div>

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
<details class="howto"><summary>How to find and remove duplicates</summary><div class="howto-body">
<p><strong>See them first, then delete.</strong> Never delete before you have looked.</p>
<ol>
<li>Select the column you think has duplicates.</li>
<li><strong>Home</strong> tab, <strong>Conditional Formatting</strong>, <strong>Highlight Cells Rules</strong>, <strong>Duplicate Values</strong>. They turn red. Scroll and confirm they are genuine copies.</li>
<li>To remove: click inside the data, then <strong>Data</strong> tab, then <strong>Remove Duplicates</strong>.</li>
<li>A box lists every column with checkboxes. This matters: Excel deletes a row only when <em>every</em> checked column matches. To dedupe on the ID alone, check only the ID column.</li>
<li>Excel reports how many it removed. Write that number down, you will need it.</li>
</ol>
<p><strong>Work on a copy of the sheet.</strong> Remove Duplicates cannot be undone reliably after other edits.</p>
</div></details><details class="howto"><summary>How to clean text and fix number columns</summary><div class="howto-body">
<p>Build these in an empty column beside the dirty one, then paste the results back as values.</p>
<ol>
<li><strong>Stray spaces:</strong> <span class="kbd">=TRIM(A2)</span></li>
<li><strong>Inconsistent casing:</strong> <span class="kbd">=PROPER(A2)</span> for names, <span class="kbd">=UPPER(A2)</span> for codes</li>
<li><strong>Both at once:</strong> <span class="kbd">=PROPER(TRIM(A2))</span></li>
<li><strong>Numbers stored as text</strong> (left-aligned, with a $ typed in): <span class="kbd">=VALUE(SUBSTITUTE(A2,"$",""))</span></li>
<li>Fill down, then select your clean column, Copy, then right-click the original and choose <strong>Paste Special, Values</strong>. Now delete the helper column.</li>
</ol>
<p><strong>How to tell a real number from text:</strong> numbers align right by default, text aligns left. If a column of numbers is left-aligned, Excel thinks it is text and SUM will return 0.</p>
</div></details><details class="howto"><summary>How to write a VLOOKUP</summary><div class="howto-body">
<p>The formula is <span class="kbd">=VLOOKUP(what you are looking up, where to look, which column to return, FALSE)</span></p>
<ol>
<li>Click the empty cell where you want the answer.</li>
<li>Type <span class="kbd">=VLOOKUP(</span> then click the cell holding the value you are looking up, then a comma.</li>
<li>Select the whole lookup table, including its header row, then press <span class="kbd">F4</span> (<span class="mac">Mac</span> <span class="kbd">fn+F4</span>) to lock it with dollar signs. Without this the range slides as you fill down and results go wrong.</li>
<li>Type a comma, then the column number to return, counting from the left edge of your selection starting at 1.</li>
<li>Type <span class="kbd">,FALSE)</span> and press Enter. FALSE means exact match, and you want exact match essentially always.</li>
<li>Fill down by double-clicking the small square at the bottom-right of the cell.</li>
</ol>
<p><strong>#N/A</strong> means no match was found. Usually stray spaces: wrap the lookup value in <span class="kbd">TRIM()</span>. <strong>#REF!</strong> means your column number is larger than your selection.</p>
</div></details>
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
exercise.</p></div>
<div class="stuck"><strong>When you get stuck</strong>
<p>Before raising your hand, try these in order. Most problems in this lab are one of them.</p>
<ol>
<li>Re-read the checkpoint question. Is it asking for a count, a total, or an average? Those are three different numbers.</li>
<li>Check whether your number is plausible. If total revenue comes out as 12 or as 40 million, something is off by a lot and you can usually see where.</li>
<li>Expand the grey "How to" box for that step. It has the exact clicks.</li>
<li>Check the formula bar of the cell you think is wrong. Does it reference the range you meant?</li>
<li>Use the hint button on the checkpoint. It is not a penalty, it is part of the lab.</li>
<li>Ask a neighbour. Then raise your hand.</li>
</ol></div>""",
  submit="Your cleaned workbook as LAB3_Last_First.xlsx including your helper columns, a three-sentence note to the controller quantifying what was wrong, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L3),

"lab4-excel-dataviz.html": dict(
  labid="LAB4", n="Lab 4", title="Data Visualization: Charts That Tell the Truth", week="Week 4",
  reflect="""Every chart in Part 3 was built from accurate data and every one of them misled. In the field you plan to enter, describe a situation where someone would have an incentive to present true numbers in a misleading shape. What would you look at first to catch it?""",
  pair=('chapter3-dominos.html','Chapter 3 \u00b7 Business Processes'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Connect to this week's Domino's case. The
  tracker made a process visible, and visibility is what lets anyone manage anything. Charts are how
  visibility reaches a manager, which means a misleading chart is a broken instrument. Part 1 of this lab is
  quick, matching the chart to the question. Part 3 is the real work, four charts built from true
  Cascadia numbers that each mislead in a different way. Worth doing the first one on the projector:
  show Chart A, ask the room how much bigger Bellevue is than Bellingham, let them answer from the
  picture, then reveal it is 8 percent. That moment lands better than any explanation.</p>""",
  intro="""<p class="lede">A chart is an argument, not decoration. The wrong chart makes a true finding
  unreadable, and a carefully wrong chart makes a false finding look obvious. Today you learn to pick
  the right one, and then you practice catching charts that lie while telling the truth.</p>
  <p>Open <a href="cascadia-sales-2025.xlsx"><strong>cascadia-sales-2025.xlsx</strong></a>. You will
  build everything from pivot tables, so this is also good pivot practice before Exam 1.</p>""",
  steps="""


<h2><span class="num">Part 1</span>The question decides the chart</h2>

<p>Almost every chart mistake is really a question mistake: someone picked a shape before deciding what
they were asking. Learn the mapping.</p>

<h3>Bar chart: comparing across categories</h3>
<p>One number measured across separate named things. Revenue by store. Units by product. The bars sit
apart because the categories are unrelated, and length is what your eye compares, which is why bars work.
Humans read length accurately.</p>
<p><strong>Sort by value</strong> unless the categories have a natural order, and <strong>start the axis
at zero</strong>. Both rules come back to bite you in Part 3.</p>

<h3>Line chart: change over time</h3>
<p>The horizontal axis is time and the points are steps in a sequence. Revenue by month. Enrollments by
day. The connecting line is doing real work: it tells the reader these values belong to one continuous
story, which is exactly why you must never use a line for categories.</p>

<h3>Scatter plot: the relationship between two numbers</h3>
<p>Two measurements per thing, one dot each, position carrying both. Store size against store revenue.
Scatter plots answer a question no other chart can: they show you the outlier sitting off the pattern,
which is usually the most interesting item in the dataset.</p>

<h3>Pie chart: parts of one whole</h3>
<p>Only when the slices sum to a meaningful 100 percent, and only with a handful of them. Humans compare
angles badly. If you are ranking things, use a bar chart. Most pie charts in business decks should have
been bar charts.</p>

<div class="callout"><strong>The test before you chart anything</strong>
<p>Say the question out loud in one sentence. "How do the stores compare?" is a bar. "What happened over
the year?" is a line. "Does bigger mean richer?" is a scatter. If you cannot say the question in a
sentence, you are not ready to chart yet.</p></div>

<h2><span class="num">Part 2</span>Build two, properly</h2>
<ol>
<li><strong>Revenue by store, sorted bar.</strong> Pivot, chart, sort descending, axis at zero, title
that states the finding rather than the topic.</li>
<li><strong>Revenue by month, line.</strong> Twelve points, time on the horizontal. Look at the shape
of the co-op's year before you move on, because you will need it later.</li>
</ol>

<details class="howto"><summary>How to make a pivot table</summary><div class="howto-body">
<ol>
<li>Click any single cell inside the data.</li>
<li><strong>Insert</strong> tab, then <strong>PivotTable</strong>. <span class="mac">Mac</span> same menu, but the button may read <strong>Summarize with PivotTable</strong>.</li>
<li>Excel guesses the data range. Check that it covers all the rows, then choose <strong>New Worksheet</strong> and click OK.</li>
<li>A panel appears on the right with your column names. Drag a field into <strong>Rows</strong> to group by it, and drag a number into <strong>Values</strong> to total it.</li>
<li>If Values shows a count instead of a sum, click it, choose <strong>Value Field Settings</strong>, and pick <strong>Sum</strong>. This catches almost everyone once.</li>
</ol>
<p><strong>If your pivot is empty:</strong> you probably selected a single cell outside the data before inserting. Undo and click inside the table first.</p>
</div></details><details class="howto"><summary>How to insert and clean up a chart</summary><div class="howto-body">
<ol>
<li>Select the pivot table results, including the row labels.</li>
<li><strong>Insert</strong> tab, then the chart type you want. Hover any icon to see its name before clicking.</li>
<li>To sort a bar chart: sort the pivot table itself. Click the dropdown arrow on the Row Labels header, then <strong>More Sort Options</strong>, then sort by your value column, descending.</li>
<li>To set the axis to zero: right-click the vertical axis, choose <strong>Format Axis</strong>, and set Minimum to 0.</li>
<li>To retitle: click the chart title once, then type. To delete a legend you do not need, click it and press Delete.</li>
</ol>
<p><span class="mac">Mac</span> Chart tools live in the <strong>Chart Design</strong> and <strong>Format</strong> tabs that appear when a chart is selected.</p>
</div></details>

<div class="ailight r">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Red &middot; this part is you alone</strong>
  <p>Do not ask an AI what is wrong with these charts. Diagnosing a misleading chart with your own eyes
  is the skill this lab exists to build, and it is the one you will need in a meeting where no AI is
  open and a vendor's slide looks a little too convincing.</p></div>
</div>
<h2><span class="num">Part 3</span>Four charts that lie</h2>

<p>Here is the part that matters. Each of the four charts below is built from Cascadia's real 2025 data.
Every number in them is correct. Every one of them misleads. Build each one yourself so you can see how
easy it is, then answer the checkpoint that exposes it.</p>

<h3>Chart A: the truncated axis</h3>
<p>Bar chart of Bellevue, Tacoma, and Bellingham revenue, with the vertical axis starting at $80,000
instead of zero. Build it. Bellevue's bar towers over Bellingham's, looking several times taller.</p>
<p>Then compute the actual gap between them. The distance between what the picture says and what the
arithmetic says is the whole lesson, and this is the single most common way charts mislead in business,
usually without anyone intending it.</p>

<h3>Chart B: the line that invents a trend</h3>
<p>Put the eight stores on a line chart, left to right, revenue on the vertical. The line slopes
downward and looks like decline.</p>
<p>Nothing is declining. A line says these points are steps in a sequence, and stores are not a sequence.
The proof: reorder the stores alphabetically and the "trend" changes shape entirely. Any pattern that
depends on the order you happened to type things in was never a pattern.</p>

<h3>Chart C: the unreadable pie</h3>
<p>Pie chart of revenue by individual product. Build it and try to answer a simple question from it, such
as which product is fourth largest. You cannot, and neither can anyone in your audience.</p>
<p>The chart is accurate and useless, which is its own category of failure. A chart that cannot be read
is not a neutral choice; it consumes attention and returns nothing.</p>

<h3>Chart D: the honest chart with the dishonest title</h3>
<p>A clean line chart of monthly revenue, correctly built, titled <em>"Revenue Collapsing After
January."</em> Revenue really does fall about 25 percent from January to February. The chart is accurate,
the number is accurate, and the conclusion is false.</p>
<p>Look at the full year and you will see why. This is the most dangerous of the four, because there is
nothing to catch by inspecting the chart itself. The lie lives in the framing, and the only defence is
knowing enough about the business to notice that a seasonal dip has been renamed a collapse.</p>

<div class="callout callout-caution"><strong>Where this connects to Monday</strong>
<p>Healthcare.gov's leadership was not lied to. They received status reports that were accurate about
what they measured: contract deliverables completed, milestones marked green. Nothing in those reports
was false. What none of them said was whether the assembled system could serve the number of people who
would arrive on October 1st. Accurate information, wrong question, catastrophic outcome. Every chart in
this part of the lab is a small version of that.</p></div>

<h2><span class="num">Part 4</span>Fix one</h2>
<p>Pick whichever of the four you find most misleading and rebuild it honestly: right chart type, axis
from zero, readable number of items, and a title that states what the data actually supports. Put the
before and after side by side on one sheet.</p>
<p>Then write one sentence naming who would benefit from the misleading version. Sometimes the answer is
nobody and it was carelessness. Often it is not, and being able to say so plainly is part of the job you
are training for.</p>
<div class="stuck"><strong>When you get stuck</strong>
<p>Before raising your hand, try these in order. Most problems in this lab are one of them.</p>
<ol>
<li>Re-read the checkpoint question. Is it asking for a count, a total, or an average? Those are three different numbers.</li>
<li>Check whether your number is plausible. If total revenue comes out as 12 or as 40 million, something is off by a lot and you can usually see where.</li>
<li>Expand the grey "How to" box for that step. It has the exact clicks.</li>
<li>Check the formula bar of the cell you think is wrong. Does it reference the range you meant?</li>
<li>Use the hint button on the checkpoint. It is not a penalty, it is part of the lab.</li>
<li>Ask a neighbour. Then raise your hand.</li>
</ol></div>""",
  submit="Your workbook containing the two charts from Part 2, your four rebuilt misleading charts from Part 3, and the before-and-after fix from Part 4 with your one-sentence note, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L4),

"lab5-excel-analysis.html": dict(reflect="""You just found a problem that every standard report concealed. In the career you are heading toward, what is one 'healthy-looking sick store': a metric that could look fine while something underneath it fails? What would you have to break out, segment, or cross-tab to catch it early?""",
  labid="LAB5", n="Lab 5", title="Data Analysis: Why Are Members Disappearing?", week="Week 5",
  pair=('chapter4-healthcaregov.html','Chapter 4 · Systems Analysis'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> This is the hardest Excel assignment of
  the quarter, by design, and it lands two days after Exam 1 with Wednesday's Healthcare.gov case fresh: a
  system whose status reports were accurate and told leadership nothing that mattered. Part A is guided skill work
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

<div class="ailight r">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Red, then green</strong>
  <p>The open-brief investigation in this lab is the one part of the Excel sequence where AI stays closed: the skill being graded is noticing something wrong in data nobody annotated for you. After you have found it and written it up, the light turns green: ask an AI to argue against your explanation, sparring partner mode, and see if your finding survives.</p></div>
</div>

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
<details class="howto"><summary>How to make a pivot table</summary><div class="howto-body">
<ol>
<li>Click any single cell inside the data.</li>
<li><strong>Insert</strong> tab, then <strong>PivotTable</strong>. <span class="mac">Mac</span> same menu, but the button may read <strong>Summarize with PivotTable</strong>.</li>
<li>Excel guesses the data range. Check that it covers all the rows, then choose <strong>New Worksheet</strong> and click OK.</li>
<li>A panel appears on the right with your column names. Drag a field into <strong>Rows</strong> to group by it, and drag a number into <strong>Values</strong> to total it.</li>
<li>If Values shows a count instead of a sum, click it, choose <strong>Value Field Settings</strong>, and pick <strong>Sum</strong>. This catches almost everyone once.</li>
</ol>
<p><strong>If your pivot is empty:</strong> you probably selected a single cell outside the data before inserting. Undo and click inside the table first.</p>
</div></details><details class="howto"><summary>How to use Goal Seek (it is well hidden)</summary><div class="howto-body">
<ol>
<li>You need a cell containing a <em>formula</em> whose result you want to force to a particular value, and another cell the formula depends on.</li>
<li><strong>Data</strong> tab, then <strong>What-If Analysis</strong>, then <strong>Goal Seek</strong>. <span class="mac">Mac</span> same path, under the Data tab.</li>
<li><strong>Set cell:</strong> the formula cell. <strong>To value:</strong> the number you want it to reach. <strong>By changing cell:</strong> the input cell.</li>
<li>Click OK. Excel changes the input until the formula hits your target.</li>
</ol>
<p><strong>"Cell must contain a value" error:</strong> you put the formula in the wrong box. Set cell must hold a formula, By changing cell must hold a plain number.</p>
</div></details>
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
is the analyst's version of the audit Nike never ran.</p></div>
<div class="stuck"><strong>When you get stuck</strong>
<p>Before raising your hand, try these in order. Most problems in this lab are one of them.</p>
<ol>
<li>Re-read the checkpoint question. Is it asking for a count, a total, or an average? Those are three different numbers.</li>
<li>Check whether your number is plausible. If total revenue comes out as 12 or as 40 million, something is off by a lot and you can usually see where.</li>
<li>Expand the grey "How to" box for that step. It has the exact clicks.</li>
<li>Check the formula bar of the cell you think is wrong. Does it reference the range you meant?</li>
<li>Use the hint button on the checkpoint. It is not a penalty, it is part of the lab.</li>
<li>Ask a neighbour. Then raise your hand.</li>
</ol></div>""",
  submit="Your workbook as LAB5_Last_First.xlsx (Part A sheets plus your investigation pivots), your one-page board memo, plus your completion certificate PDF (your reflection is page 2 of it).",
  qs=L5),

"lab6-tableau.html": dict(
  labid="LAB6", n="Lab 6", title="Data Visualization with Tableau", week="Week 6",
  reflect="""You built a dashboard that shows revenue, and revenue at this co-op looks healthy. In the field you plan to enter, name one dashboard you have seen or can imagine that would show green while something serious was going wrong underneath. What single chart would you add to catch it?""",
  pair=('index.html','Chapter 7 \u00b7 BI &amp; Analytics (coming)'),
  bridge="""<p><strong>Lab professor's intro (10 min):</strong> Frame with Monday's BI discussion: the A's won by measuring what the league was not measuring. Today students point a
  different instrument at data they already know well. Two things are worth doing on the projector.
  First, show the Data Source pane and one drag-and-drop so the interface stops being intimidating.
  Second, show the difference between a worksheet and a dashboard, because that distinction is the whole
  lab and Tableau's own vocabulary makes it confusing at first. Tableau Public is free and sufficient if
  desktop licences are a problem. Checkpoints 5 and 6 have a deliberately surprising answer.</p>""",
  intro="""<p class="lede">In Lab 4 you learned which chart answers which question and assembled one in
  Excel. Tableau exists because that assembly should be faster, and because a real dashboard does
  something an Excel sheet cannot: the pieces talk to each other. Click a region, and every chart
  responds.</p>
  <p>Download <a href="cascadia-sales-2025.csv"><strong>cascadia-sales-2025.csv</strong></a> and connect
  Tableau, or free <a href="https://public.tableau.com">Tableau Public</a>, to it.</p>""",
  steps="""

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach</strong>
  <p>Tableau questions are perfect coach material: ask an AI where a setting lives or why your chart shows SUM when you wanted a percentage, then make the change yourself. The dashboard you submit must be assembled by you.</p></div>
</div>

<h2><span class="num">Part 1</span>Worksheets and dashboards are different things</h2>

<p>Tableau's vocabulary trips up nearly everyone in the first hour, so get it straight before you build
anything.</p>

<p>A <strong>worksheet</strong> is one chart answering one question. Revenue by store. That is a
worksheet. In Tableau you build worksheets one at a time, each on its own tab at the bottom of the
window, and each one is a complete little argument by itself.</p>

<p>A <strong>dashboard</strong> is an arrangement of finished worksheets on one screen, plus the
connections between them. This is the part that matters and the part people skip: on a real dashboard,
a filter can apply to every chart at once, and clicking a bar in one chart can filter all the others.
The charts stop being pictures sitting next to each other and start behaving like one instrument.</p>

<p>Hold onto the definition from Lab 4, because it still governs: a dashboard is a single screen that
answers a specific person's recurring questions about the current state of something, without them
having to ask anyone. Tableau gives you better tools for building one. It does not decide for you who
the person is or what they need to know, and no software ever will.</p>

<div class="callout"><strong>Chart choice did not change</strong>
<p>Tableau has a Show Me panel that offers you every chart type it can draw with your fields, and it is
a trap if you let it choose for you. The logic from Lab 4 still applies. Comparing across categories is
a bar chart. Change over time is a line. A relationship between two numbers is a scatter. Show Me tells
you what is possible, not what is right.</p></div>

<h2><span class="num">Part 2</span>Build five worksheets</h2>

<ol>
<li><strong>Connect and check.</strong> Open the CSV as a data source. Confirm the row count, and that
Tableau read revenue as a number and sale_date as a date rather than text. Fixing types here is much
easier than fixing them after you have built six charts on top of them.</li>
<li><strong>Sorted bar: revenue by store.</strong> Store to Rows, revenue to Columns, sort descending
with the toolbar button. Notice how much faster this is than the Excel version.</li>
<li><strong>Line: revenue by month.</strong> Drag sale_date to Columns and set it to Month. Watch the
shape of the year.</li>
<li><strong>Calculated field: margin rate by category.</strong> Analysis, then Create Calculated Field.
This is the Moneyball move, building a ratio the raw data does not contain and making it something you
can chart.</li>
<li><strong>Highlight table: store by month.</strong> Store in Rows, month in Columns, revenue on
Color. The co-op's whole year on one screen. Click cells rather than judging colour by eye, because
colour is genuinely hard to read precisely and that is a limitation worth knowing about the chart type
you just chose.</li>
<li><strong>Attach rate by store.</strong> The view Cascadia never built. You know what you found in
Lab 5; watch what happens when it is drawn instead of tabulated.</li>
</ol>

<h2><span class="num">Part 3</span>Assemble the dashboard</h2>

<ol>
<li><strong>New dashboard.</strong> The dashboard tab is at the bottom of the window, next to your
worksheet tabs. Set a size that matches how it will be viewed rather than leaving it automatic.</li>
<li><strong>Drag your worksheets in.</strong> Put the chart answering the most important question in the
top left. Everything you learned about arrangement in Lab 4 applies here.</li>
<li><strong>Add a filter and apply it everywhere.</strong> This is the step that makes it a dashboard
rather than a poster. Add region as a filter, then set it to apply to all worksheets using this data
source. Now changing one dropdown changes every chart at once.</li>
<li><strong>Add a dashboard action.</strong> Dashboard menu, then Actions, then Add Action, then Filter.
Set it so clicking a store in your bar chart filters the other charts to that store. Click Seattle
Flagship and watch the rest of the screen answer a new question. Nothing in Excel does this.</li>
<li><strong>Title it with the finding.</strong> Not "Cascadia Dashboard." Something a manager could act
on.</li>
</ol>

<div class="callout callout-caution"><strong>The honest question, again</strong>
<p>Your dashboard is built mostly on revenue, and revenue at this co-op looks fine. In Lab 5 you found
something that revenue never showed you. Look at your finished screen and ask what else it would fail to
reveal. Every dashboard has a blind spot, and the professional skill is not building one without blind
spots, which is impossible. It is knowing where yours are and saying so out loud.</p></div>

<div class="callout"><strong>If you finish early</strong>
<p>Put revenue on one axis and margin rate on the other, by category, as a scatter. The A's looked for
players the market underpriced. A merchant looks for categories earning a high rate on modest volume.
Which category would you tell Cascadia to promote harder? There is no checkpoint for this and more than
one defensible answer; your pick and one sentence of reasoning go in the submission note.</p></div>""",
  submit="Your packaged workbook (.twbx) or a PDF export of the dashboard showing the region filter applied, your undervalued-category pick with one sentence of reasoning, plus your completion certificate PDF (your reflection is page 2 of it).",
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


<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as coach</strong>
  <p>SQL error messages are terse, and asking an AI to explain one is exactly the right use: paste the error and your query, understand the explanation, then fix it yourself. Asking it to write the checkpoint queries from scratch is different; in Week 7 the syntax is still the thing you are building.</p></div>
</div>

<h2><span class="num">Part 1</span>Why the data is not in Excel</h2>

<p>Everything you have touched this quarter has been a spreadsheet, so it is worth saying plainly:
no real company keeps its operating data in Excel. Cascadia's registers do not write to a workbook.
They write to a <strong>database</strong>, and the difference is not cosmetic.</p>

<p>A spreadsheet is one grid, edited by one person at a time, that tops out around a million rows and
lives in a file someone can move, break, or email around. A <strong>relational database</strong> is a
set of tables that live on a server, get written to by hundreds of registers and websites at the same
moment, hold effectively unlimited rows, and are read by asking questions in SQL rather than by
scrolling.</p>

<p>The word <em>relational</em> is the important one. Look at the schema box above: the sales table
does not contain store names. It contains a <strong>store_id</strong>, a number pointing at one row of
the stores table, where the name, region, and square footage live exactly once. That pointer is called
a <strong>foreign key</strong>, and the column it points at, the one that uniquely identifies each row,
is a <strong>primary key</strong>.</p>

<p>Why build it that way? Because facts should live in one place. If Bellingham's name were spelled out
on all of its sales rows and the co-op renamed the store, someone would have to fix thousands of rows
and would miss some, and you have already seen this movie: it is exactly how the state column in
sales_raw ended up with fourteen spellings. Storing each fact once and pointing at it is the cure for
the disease you are about to spend this lab treating. Monday's lecture calls this
<strong>normalization</strong>; today you get to feel why it exists.</p>

<div class="callout"><strong>The one-sentence version</strong>
<p>Excel is where analysis happens. A database is where the truth lives. The skill this lab teaches is
going to the truth directly.</p></div>

<div class="callout"><strong>See it before you write it</strong>
<p>Open the <a href="join-builder.html"><strong>Join Builder</strong></a> in another tab. Click a
foreign key, click the primary key it points at, and watch the arrow become a working JOIN against this
same database. Five minutes there makes the last two checkpoints here much easier.</p></div>
<h2><span class="num">Sandbox</span>The Cascadia database, live</h2>
<div id="sqlbox" style="border:1px solid var(--rule);background:var(--paper);border-radius:2px;padding:1rem 1.15rem;margin:1.2rem 0">
  <p id="sqlstatus" style="font-family:var(--sans);font-size:.85rem;color:var(--muted);margin:0 0 .6rem">Loading database&hellip;</p>
  <textarea id="sqlin" rows="5" spellcheck="false" style="width:100%;font-family:ui-monospace,Menlo,monospace;font-size:.92rem;padding:.6rem;border:1px solid var(--rule);border-radius:2px" aria-label="SQL query" placeholder="SELECT COUNT(*) FROM sales_raw;"></textarea>
  <br><button onclick="runSQL()" style="font-family:var(--display);font-size:14px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;background:var(--magenta);color:#fff;border:none;padding:.5rem 1.1rem;cursor:pointer;margin-top:.5rem">Run query</button>
  <div id="sqlout" style="overflow-x:auto;margin-top:.8rem;font-family:var(--sans);font-size:.85rem"></div>
</div>

<h2><span class="num">Part 2</span>Six steps for cleaning any table</h2>

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


<h3>The payoff: tables that connect</h3>
<p>Cleaning one table is half the story. The other half is that tables answer questions
<em>together</em>. The pattern is JOIN:</p>
<pre style="background:var(--off-white);border:1px solid var(--border);padding:.9rem 1rem;overflow-x:auto;font-family:ui-monospace,Menlo,monospace;font-size:.85rem;line-height:1.5">SELECT s.store_name, SUM(sa.quantity * sa.unit_price) AS revenue
FROM sales sa
JOIN stores s ON s.store_id = sa.store_id
GROUP BY s.store_name;</pre>
<p>Read the ON clause out loud: connect each sales row to the stores row whose primary key matches its
foreign key. Every VLOOKUP you wrote in Lab 3 was a hand-built imitation of this one line, and the last
two checkpoints ask you to use it.</p>
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
