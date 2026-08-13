"""Builds lab8-security.html (Security & Data Governance: The Audit).
Checkpoint answers computed live from cascadia.db so they can never drift.
Page shell (head, topnav, rail, engine JS) is sliced from lab7-sql.html so the
design stays identical to the deployed site. Also updates topnav across all
pages, the schedule slot, and Chapter 9's pair link.
"""
import base64, json, re, sqlite3

con = sqlite3.connect('cascadia.db')
Q = lambda s: con.execute(s).fetchone()[0]
R = "quantity*unit_price"
b64 = lambda s: base64.b64encode(str(s).encode()).decode()
def num(p, a, tol, h): return {"q": p, "t": "num", "a": b64(a), "tol": tol, "h": h}
def txt(p, a, h):      return {"q": p, "t": "txt", "a": b64(a), "h": h}

# ---------------- computed ground truth ----------------
n_members   = Q("SELECT COUNT(*) FROM members")
n_states    = Q("SELECT COUNT(DISTINCT state) FROM members")
nordvik     = Q("SELECT country FROM suppliers WHERE supplier_name='Nordvik Outdoor'")
ghost       = Q("SELECT COUNT(*) FROM members WHERE member_id=1287")
bham_rows   = Q("SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham'")
total_rows  = Q("SELECT COUNT(*) FROM sales")
bham_pct    = round(100.0 * bham_rows / total_rows, 1)
total_rev   = round(Q(f"SELECT SUM({R}) FROM sales"), 2)
daily_rev   = round(Q(f"SELECT SUM({R})/COUNT(DISTINCT sale_date) FROM sales"), 2)

QS = [
 num("Part 1 \u00b7 The confidentiality inventory. Start where every audit starts, with a count of what you are protecting: SELECT COUNT(*) FROM members; How many people's personal information does the co-op hold?",
     n_members, 0,
     "One line in the sandbox above. Each row is a real person's name, city, and membership history. Change Healthcare's number was 190 million; the co-op's is smaller, but the shape of the obligation is identical."),
 num("Part 1 \u00b7 Breach notification is state law, and every state writes its own. SELECT COUNT(DISTINCT state) FROM members; If member data leaked, how many different states' notification laws would the co-op be answering to?",
     n_states, 0,
     "COUNT(DISTINCT state) collapses the column to its unique values. Every distinct state is a separate legal clock that starts ticking the day you discover a breach."),
 txt("Part 2 \u00b7 Email one claims to be from Nordvik Outdoor, \"your US-based climbing hardware supplier,\" announcing new bank details for invoice payments. Verify the claim against the system of record: SELECT country FROM suppliers WHERE supplier_name='Nordvik Outdoor'; What country is Nordvik Outdoor actually in?",
     nordvik,
     "The query returns one word, and it is not the one the email used. A supplier that gets its own country wrong is not your supplier. This exact fraud, a real vendor name plus new bank details, is called business email compromise, and it costs companies billions a year."),
 num("Part 2 \u00b7 Email two says member 1287 has filed a complaint and demands you send their full record for review. SELECT COUNT(*) FROM members WHERE member_id=1287; What does the count return?",
     ghost, 0,
     "Zero rows. There is no member 1287, so the request is a fishing trip for whatever record you might send back. The lesson generalizes: verify the claim, not the tone. Urgency is a technique, not evidence."),
 num("Part 3 \u00b7 Least privilege, measured. Suppose each register credential could read only its own store's sales. How many rows can a Bellingham-scoped account reach? SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham';",
     bham_rows, 0,
     "A JOIN and a WHERE, both from Lab 7. This number is the blast radius of one stolen register password in a least-privilege design."),
 num("Part 3 \u00b7 Now express the blast radius as a share: one hundred times your Checkpoint 5 answer, divided by the total number of sales rows (you have known that total since Lab 2). What percent of the co-op's sales does one scoped credential expose? One decimal.",
     bham_pct, 0.2,
     "Roughly one eighth. The same stolen password against an unscoped, everything-access account exposes one hundred percent. That gap is the entire argument for least privilege, in one division."),
 num("Part 4 \u00b7 Integrity. You have computed total revenue in Excel twice this quarter. Compute it here in one line: SELECT ROUND(SUM(quantity*unit_price),2) FROM sales; What is it?",
     total_rev, 1,
     "The point is not the arithmetic. A number you can recompute from source at any time is a control: if an attacker with write access quietly alters rows, this total moves, and you notice. Integrity monitoring is recomputing what you already know and checking that it still agrees."),
 num("Part 4 \u00b7 Availability. Ransomware does not steal a register; it stops it. SELECT ROUND(SUM(quantity*unit_price)/COUNT(DISTINCT sale_date),2) FROM sales; To the nearest dollar, what does one dark day cost the co-op in revenue alone?",
     daily_rev, 5,
     "Total revenue over distinct selling days. Multiply by the ten days Change Healthcare's systems were down and you have the start of a board-ready number, before a single record leaks."),
]

REFLECT = ("This lab asked you to make security decisions with a business degree's tools: an inventory, "
 "a verification habit, an access map, and a handful of numbers. Think of an organization you know from "
 "the inside, a job, a club, a team. Name the data it holds that would hurt most if it leaked or locked "
 "up, who can currently reach it, and the one control from this lab you would put in place there first. "
 "Why that one?")

# ---------------- slice the shell from lab7 ----------------
lab7 = open('lab7-sql.html').read()
head = lab7[:lab7.index('<main id="top">')]

# retitle
head = head.replace('<title>Lab 7: SQL Fundamentals | MIS 320</title>',
                    '<title>Lab 8: Security &amp; Data Governance | MIS 320</title>')
head = re.sub(r'<meta name="description" content="[^"]*">',
 '<meta name="description" content="Play the security lead at Cascadia Outfitters: inventory the data, verify the phish against the database, measure least privilege, and price a dark day.">',
 head, count=1)

# topnav: lab7 no longer current; insert lab8 as current; shrink the soon line
head = head.replace('<a class="current" href="lab7-sql.html">', '<a href="lab7-sql.html">')
LAB8_NAV = '<a class="current" href="lab8-security.html"><span class="lbl">Lab 8 &middot; Week 8</span>Security &amp; Data Governance: The Audit</a>\n      '
head = head.replace('      <div class="dd-sep"></div>\n      <a class="soon" href="#"><span class="lbl">Labs 8&ndash;10</span>UX, AI/ML, Information Architecture (in progress)</a>',
 '      ' + LAB8_NAV + '<div class="dd-sep"></div>\n      <a class="soon" href="#"><span class="lbl">Labs 9&ndash;10</span>AI/ML, Information Architecture (in progress)</a>')

# rail
head = re.sub(r'<nav id="chapnav">.*?</nav>',
 '''<nav id="chapnav">
    <a href="#top">Overview</a><a href="#inventory">Part 1 · The inventory</a>
    <a href="#verify">Part 2 · Verification</a><a href="#blast">Part 3 · Blast radius</a>
    <a href="#controls">Part 4 · Control numbers</a><a href="#map">Part 5 · The access map</a>
    <a href="#checkpoints">Checkpoints</a><a href="#submit">What to submit</a>
    <a href="chapter9-changehealthcare.html">↳ Chapter 9 · Cybersecurity</a>
  </nav>''', head, flags=re.S)

# ---------------- engine JS, sqljs init, railtoggle, dd JS from lab7 ----------------
scripts = re.findall(r'<script[^>]*>.*?</script>', lab7, re.S)
sqljs_init  = [s for s in scripts if 'CASCADIA_DB' in s][0]
railtoggle  = [s for s in scripts if 'railtoggle' in s][0]
ddjs        = [s for s in scripts if 'dd-btn' in s and 'closeAll' in s][0]
engine      = [s for s in scripts if 'const LAB=' in s][0]

# swap the sandbox status line so it fits this lab
sqljs_init = sqljs_init.replace(
 "Database loaded. Eight tables, including the messy sales_raw. Type a query and press Run.",
 "Database loaded. The co-op's eight tables, same as Lab 7. Type a query and press Run.")

# rebuild the engine with LAB8 payload
engine = re.sub(r'const LAB="LAB7", QS=\[.*?\];\n',
                lambda m: 'const LAB="LAB8", QS=' + json.dumps(QS) + ';\n', engine, count=1, flags=re.S)
old_reflect = re.search(r"splitTextToSize\('Prompt: (.*?)',480\)", engine, re.S).group(1)
engine = engine.replace(old_reflect, REFLECT.replace("'", "\\'"))
old_labname = re.search(r"p\.text\('(Lab 7 [^']*)',280,222", engine).group(1)
engine = engine.replace(old_labname, 'Lab 8 \\u00B7 Security & Data Governance: The Audit')

# checkpoint + reflection + cert HTML block from lab7, reflection prompt swapped
cpblock = lab7[lab7.index('<h2 id="checkpoints"'):lab7.index('<h2 id="submit"')]
old_prompt = re.search(r'<div class="certbox" id="reflectbox">\s*<h3>[^<]*</h3>\s*<p style="font-family:var\(--sans\);font-size:\.88rem">(.*?)</p>', cpblock, re.S).group(1)
cpblock = cpblock.replace(old_prompt, REFLECT)
cpblock = re.sub(r'Checkpoint progress: 0 / \d+', 'Checkpoint progress: 0 / %d' % len(QS), cpblock)

# CDN script tags
sqlwasm = '<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>'
jspdf   = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'

# ---------------- the lab content ----------------
fD = '${:,.2f}'.format(daily_rev)
MAIN = f'''<main id="top">
<header class="chaphead">
  <p class="eyebrow">Lab 8 · Week 8</p>
  <h1>Security &amp; Data Governance: The Audit</h1>
  <div class="meta-row"><span>Lab session · 80 min</span><span class="alt"><a href="chapter9-changehealthcare.html" style="color:inherit;text-decoration:none">Pairs with Chapter 9 · Cybersecurity &#8594;</a></span><span class="alt"><a href="chapter10-equifax.html" style="color:inherit;text-decoration:none">and Chapter 10 · Governance &#8594;</a></span></div>
</header>

<p class="lede">Monday's lecture ended with a company that processed a third of American healthcare going
dark because one login was missing one control. Cascadia's board read the same story, and this morning
they asked the question every board is now asking: could that be us? You are the co-op's newly appointed
security lead, and this lab is your first week on the job.</p>

<p>Here is what you will notice by the end of the session: nothing in this lab requires a single skill
you do not already have. The audit is counting, and you count with SQL. The phish is caught by checking a
claim against a database, which is a JOIN and a WHERE. The case for least privilege is one division. The
chapter argued that most security is management, not code. Today you get to test that claim on a company
whose data you know better than anyone.</p>

<div class="callout"><strong>The schema, one more time</strong>
<p style="font-family:var(--sans);font-size:.88rem"><code class="inline">stores</code>(store_id, store_name, region, opened_year, square_feet) &#183;
<code class="inline">suppliers</code>(supplier_id, supplier_name, country, lead_time_days) &#183;
<code class="inline">products</code>(product_id, product_name, category, supplier_id, unit_cost, list_price) &#183;
<code class="inline">members</code>(member_id, first_name, last_name, city, state, member_type, join_date) &#183;
<code class="inline">sales</code>(sale_id, sale_date, store_id, product_id, member_id, quantity, unit_price) &#183;
<code class="inline">inventory</code>(store_id, product_id, quantity_on_hand, reorder_point) &#183;
<code class="inline">used_gear</code>(item_id, product_id, store_id, condition, listed_price, date_listed, date_sold)</p></div>

<div class="callout callout-bridge"><strong>From lecture to lab</strong><p><strong>Lab professor's intro (10 min):</strong>
One sentence of recap: Change Healthcare, one portal without MFA, a third of US claims frozen. Then the
reframe: today students stop reading about a breach and start preventing one, as Cascadia's security
lead. Emphasize that every checkpoint uses only Lab 7 SQL, so nobody should feel behind. Demo Part 2 on
the projector: read the Nordvik email aloud in your best urgent voice, let the room feel how plausible it
is, then run the one-line query that kills it. Say the phrase out loud: verify the claim, not the tone.
Point out that Part 5, the access map, has no checkpoint because it is judgment, and judgment is what the
memo is for. Students who finish early: give them the $10,000 question from the callout at the end.</p></div>

<div class="ailight g">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Green &middot; AI as sparring partner</strong>
  <p>Draft your access map first, then ask an AI to attack it: "Here is who can read what at a retail
  co-op. Which cell would you exploit?" Defending your map against the pushback is exactly the drill.
  Asking it to fill in the map for you skips the only part that is graded on thinking.</p></div>
</div>

<div class="ailight r">
  <div class="lamp"><div class="bulb b1"></div><div class="bulb b2"></div><div class="bulb b3"></div></div>
  <div class="lighttext"><strong>Red &middot; No attack tooling, ever</strong>
  <p>Never ask an AI to write malware, working exploit code, or a phishing message aimed at a real person
  or organization. That is the hard red light from Chapter 9, it stays red after this course ends, and
  outside a classroom it is a crime. Studying the two fake emails printed below is the entire point;
  manufacturing new ones is not.</p></div>
</div>

<h2><span class="num">Sandbox</span>The Cascadia database, live</h2>
<div id="sqlbox" style="border:1px solid var(--rule);background:var(--paper);border-radius:2px;padding:1rem 1.15rem;margin:1.2rem 0">
  <p id="sqlstatus" style="font-family:var(--sans);font-size:.85rem;color:var(--muted);margin:0 0 .6rem">Loading database&hellip;</p>
  <textarea id="sqlin" rows="5" spellcheck="false" style="width:100%;font-family:ui-monospace,Menlo,monospace;font-size:.92rem;padding:.6rem;border:1px solid var(--rule);border-radius:2px" aria-label="SQL query" placeholder="SELECT COUNT(*) FROM members;"></textarea>
  <br><button onclick="runSQL()" style="font-family:var(--display);font-size:14px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;background:var(--magenta);color:#fff;border:none;padding:.5rem 1.1rem;cursor:pointer;margin-top:.5rem">Run query</button>
  <div id="sqlout" style="overflow-x:auto;margin-top:.8rem;font-family:var(--sans);font-size:.85rem"></div>
</div>

<div id="inventory"></div>
<h2><span class="num">Part 1</span>The inventory: know what you hold</h2>

<p>Every security framework on earth begins with the same unglamorous step: you cannot protect what you
have not listed. Chapter 9 put it as a manager's question, "do we have a current inventory?", and the
honest answer at most companies is no. Yours is about to be yes, because the co-op's inventory is eight
tables and you can read all of them.</p>

<p>Not all tables are equal, and the chapter's CIA triad is the sorting tool. For each table, ask which
property matters most: who must <em>not</em> read it (confidentiality), what breaks if it is silently
altered (integrity), and what stops if it is unavailable (availability).</p>

<table class="lab">
<thead><tr><th>Table</th><th>What it really is</th><th>Which property dominates</th></tr></thead>
<tbody>
<tr><td><code class="inline">members</code></td><td>Real people's names, cities, and membership history. The only table with PII.</td><td>Confidentiality. This is the table a breach notification is about.</td></tr>
<tr><td><code class="inline">sales</code></td><td>The financial record of the business.</td><td>Integrity first, availability a close second. Quietly altered sales hide fraud; frozen sales stop the stores.</td></tr>
<tr><td><code class="inline">suppliers</code></td><td>Who the co-op pays, and where.</td><td>Integrity. An attacker who edits a bank detail here gets paid instead of the supplier.</td></tr>
<tr><td><code class="inline">inventory</code>, <code class="inline">products</code>, <code class="inline">stores</code>, <code class="inline">used_gear</code></td><td>Operating data.</td><td>Availability. Registers and reorder decisions read these all day.</td></tr>
</tbody>
</table>

<p>Checkpoints 1 and 2 make the confidentiality row concrete: how many people, and how many states'
breach laws are standing behind them. Run the queries, then sit with the second number for a moment,
because it is the one that surprises new security leads. A breach is not one legal event; it is one per
jurisdiction.</p>

<div id="verify"></div>
<h2><span class="num">Part 2</span>Verification beats vibes: two emails from this morning</h2>

<p>Chapter 9's breach began with a stolen password, but most breaches begin one step earlier, with a
message that persuades someone to hand access over. The defense you are about to practice is the one
that scales: do not judge a message by its tone, its urgency, or its logo. Judge it by whether its
claims survive contact with your system of record. You have the system of record open in the sandbox
above.</p>

<div class="callout callout-caution"><strong>Email one &middot; to accounts payable</strong>
<p style="font-family:var(--sans);font-size:.92rem"><em>From: billing@nordvik-outdoor-payments.com<br>
Subject: URGENT: Updated remittance details, action required before Friday</em></p>
<p style="font-family:var(--sans);font-size:.92rem">"Hello, this is the finance team at Nordvik Outdoor,
your US-based climbing hardware supplier. Due to a banking migration we require all invoice payments to
be sent to our new account, details attached. Please update before Friday's payment run to avoid
disruption to your spring orders."</p></div>

<p>Plausible. Nordvik Outdoor is a real supplier; you joined to it in Lab 7. The urgency is realistic
and the ask is routine. Now verify the one factual claim the email makes about itself. Checkpoint 3.</p>

<div class="callout callout-caution"><strong>Email two &middot; to member services</strong>
<p style="font-family:var(--sans);font-size:.92rem"><em>From: privacy-request@mail-cascadia-coop.net<br>
Subject: Formal complaint from member #1287, records required</em></p>
<p style="font-family:var(--sans);font-size:.92rem">"Member 1287 has filed a formal complaint regarding
billing errors on their account. Under our review procedure, please reply with the member's full record,
including name, address, and complete purchase history, so we can begin the investigation today."</p></div>

<p>Notice what this one is really asking for: not money, but a record. Verify that the member exists at
all. Checkpoint 4, and it is one line.</p>

<div class="callout callout-good"><strong>The habit, stated once</strong>
<p>Both emails die to a query that takes ten seconds. The professionals' version of this habit has a
name, out-of-band verification: confirm the request through a channel the requester does not control.
Call the supplier at the number in <em>your</em> records, not the one in the email. The database is your
first out-of-band channel, and you have had it since Week 7.</p></div>

<div id="blast"></div>
<h2><span class="num">Part 3</span>Blast radius: least privilege in numbers</h2>

<p>Chapter 9 said the attackers had nine days of lateral movement, which meant one stolen credential
became access to everything. The design rules against that, least privilege and segmentation, tend to
get taught as slogans. You are going to compute them instead.</p>

<p>The co-op's registers log in to record sales. Question: what should a register's credential be able
to <em>read</em>? Today, the honest answer at Cascadia is "everything," because nobody ever decided
otherwise, and security failures are mostly decisions that went unmade. Your proposal: scope each
register to its own store. Checkpoints 5 and 6 measure exactly how much that one decision shrinks the
blast radius of one stolen password.</p>

<p>Keep the resulting percentage for your memo. It is the rare security argument that fits in one
sentence with a number in it, which is the kind boards actually act on.</p>

<div id="controls"></div>
<h2><span class="num">Part 4</span>The control numbers: integrity and availability, priced</h2>

<p>Two more numbers finish the audit, one for each remaining letter of the triad.</p>

<p><strong>Integrity.</strong> An attacker with write access does not always lock your data; sometimes
they quietly change it, and the fraud hides inside numbers nobody rechecks. The defense is a control
number: a total you can recompute from source at will. You have one already. Total revenue has followed
you since Lab 2, and Checkpoint 7 asks for it one more time, now wearing its security hat: if this
number ever disagrees with itself, someone has been in your tables.</p>

<p><strong>Availability.</strong> Ransomware's real product is the dark day: registers down, inventory
unreadable, stores effectively closed. Checkpoint 8 computes what one such day costs the co-op in
revenue alone, before a single record leaks and before a lawyer is hired. Multiply it across the ten
days Change Healthcare was down and you understand why the chapter insisted the business disruption was
the disaster and the data breach was the aftermath.</p>

<div id="map"></div>
<h2><span class="num">Part 5</span>The access map: who should see what</h2>

<p>Now the part with no checkpoint, because it is the part that is actually your job. Least privilege
says every role gets the minimum it needs. Someone has to decide what that minimum is, role by role and
table by table, and that someone is never the database; it is a manager who understands the work. Copy
this grid into your submission document and fill every cell with <strong>R</strong> (read),
<strong>W</strong> (read and write), or a dash (no access).</p>

<table class="lab">
<thead><tr><th>Role</th><th>sales</th><th>members</th><th>products</th><th>suppliers</th><th>inventory</th><th>used_gear</th></tr></thead>
<tbody>
<tr><td>Register clerk</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Store manager (one store)</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Buyer (procurement)</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Member services</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Marketing intern</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>The board</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
</tbody>
</table>

<p>There is no single right map, but there are defensible and indefensible cells, and your memo must
defend three of your choices in a sentence each. Two prompts to pressure-test yourself: does the
marketing intern really need member <em>names</em>, or would an anonymized extract serve the campaign?
And does the board need write access to anything at all? (Chapter 10 has opinions about that one.)</p>

<div class="callout"><strong>If you finish early: the $10,000 question</strong>
<p>The board approves a $10,000 security budget for the year, and only one of these fits inside it: MFA
on every account, an automated offline backup of the database, or a yearly phishing training with test
emails for all staff. Pick one, and write the three sentences you would say to the board: what it
prevents, what you are consciously leaving unprotected, and why that trade is right for a company this
size. There is no checkpoint; your pick and the three sentences go in your submission note.</p></div>

{sqlwasm}
{sqljs_init}
{cpblock}
<h2 id="submit"><span class="num">Canvas</span>What to submit</h2>
<p style="font-family:var(--sans);font-size:.92rem">One document containing: your completed access map
with three defended cells, your one-paragraph security memo to the board opening with the blast-radius
percentage and the dark-day number, your $10,000 pick if you got to it, plus your completion certificate
PDF (your reflection is page 2 of it).</p>
</main></div>
{railtoggle}
{jspdf}
{engine}
{ddjs}
</body></html>'''

open('lab8-security.html', 'w').write(head + MAIN)
print('lab8-security.html written:', len(head + MAIN), 'bytes,', len(QS), 'checkpoints')
print('answers:', n_members, n_states, nordvik, ghost, bham_rows, bham_pct, total_rev, daily_rev)

# ---------------- site-wide updates ----------------
import glob
OLD_SOON = '<a class="soon" href="#"><span class="lbl">Labs 8&ndash;10</span>UX, AI/ML, Information Architecture (in progress)</a>'
NEW_BLOCK = ('<a href="lab8-security.html"><span class="lbl">Lab 8 &middot; Week 8</span>Security &amp; Data Governance: The Audit</a>\n'
             '      <div class="dd-sep"></div>\n'
             '      <a class="soon" href="#"><span class="lbl">Labs 9&ndash;10</span>AI/ML, Information Architecture (in progress)</a>')

for fn in glob.glob('*.html'):
    if fn == 'lab8-security.html': continue
    t = open(fn).read(); orig = t
    if OLD_SOON in t:
        # the sep sits just above the soon link; move lab8 above it
        t = t.replace('<div class="dd-sep"></div>\n      ' + OLD_SOON, NEW_BLOCK)
        t = t.replace(OLD_SOON,  # fallback if sep spacing differs
                      NEW_BLOCK) if OLD_SOON in t else t
    if orig != t:
        open(fn, 'w').write(t); print('topnav updated:', fn)

# schedule: turn the pending Lab 8 slot into a real link
s = open('schedule.html').read()
s2 = s.replace('<h4 class="pending">Lab 8: Security &amp; Data Governance<span class="pill wip">In development</span></h4>',
               '<h4><a href="lab8-security.html">Lab 8: Security &amp; Data Governance</a></h4>')
if s2 != s: open('schedule.html','w').write(s2); print('schedule updated')
else: print('WARNING: schedule pending slot not matched, check manually')

# chapter 9 pair link
c = open('chapter9-changehealthcare.html').read()
c2 = c.replace('<a href="schedule.html">Lab 8, Security &amp; Data Governance, runs this week',
               '<a href="lab8-security.html">Lab 8, Security &amp; Data Governance, runs this week')
c2 = c2.replace("<td>Lab 8's access decisions</td>",
                '<td><a href="lab8-security.html">Lab 8\'s access decisions</a></td>')
if c2 != c: open('chapter9-changehealthcare.html','w').write(c2); print('chapter 9 links updated')
