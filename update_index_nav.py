"""Normalizes the Chapters/Labs dropdowns on every page to the current schedule,
adds the missing Chapter 5 / 9 / 10 cards and the Lab 8 card to the index,
and fixes stale week numbers and checkpoint counts on the landing page."""
import re, glob

DDC = '''
      <a href="chapter0-what-is-mis.html"><span class="lbl">Chapter 0 &middot; Week 1</span>What Is MIS? &mdash; Spotify Wrapped</a>
      <a href="chapter1-starbucks.html"><span class="lbl">Chapter 1 &middot; Week 2</span>The Value of Information &mdash; Starbucks</a>
      <a href="chapter2-competitive-advantage.html"><span class="lbl">Chapter 2 &middot; Week 3</span>Technology &amp; Competitive Advantage &mdash; Zara</a>
      <a href="chapter3-dominos.html"><span class="lbl">Chapter 3 &middot; Week 4</span>Business Processes &mdash; Domino's</a>
      <a href="chapter4-healthcaregov.html"><span class="lbl">Chapter 4 &middot; Week 5</span>Systems Analysis &amp; the SDLC &mdash; Healthcare.gov</a>
      <a href="chapter5-walmart.html"><span class="lbl">Chapter 5 &middot; Week 7</span>What Data Is: Databases &mdash; Walmart</a>
      <a href="chapter6-nike-sap.html"><span class="lbl">Chapter 6 &middot; Week 7</span>Enterprise Systems &mdash; Nike/SAP</a>
      <a href="chapter9-changehealthcare.html"><span class="lbl">Chapter 9 &middot; Week 8</span>Cybersecurity &mdash; Change Healthcare</a>
      <a href="chapter10-equifax.html"><span class="lbl">Chapter 10 &middot; Week 8</span>IT Governance &mdash; Equifax</a>
      <div class="dd-sep"></div>
      <a class="soon" href="#"><span class="lbl">Chapters 7&ndash;8, 11&ndash;12</span>BI, AI/ML, Cloud, IoT (in progress)</a>
      '''

DDL = '''
      <a href="lab1-genai.html"><span class="lbl">Lab 1 &middot; Week 1</span>GenAI for Thinking</a>
      <a href="lab2-excel-basics.html"><span class="lbl">Lab 2 &middot; Week 2</span>Excel Basics: Meeting the Client</a>
      <a href="lab3-excel-dataprep.html"><span class="lbl">Lab 3 &middot; Week 3</span>Data Preparation: The RAW File</a>
      <a href="lab4-excel-dataviz.html"><span class="lbl">Lab 4 &middot; Week 4</span>Data Visualization: Charts That Tell the Truth</a>
      <a href="lab5-excel-analysis.html"><span class="lbl">Lab 5 &middot; Week 5</span>Data Analysis &amp; Mini Project</a>
      <a href="lab6-tableau.html"><span class="lbl">Lab 6 &middot; Week 6</span>Tableau: Worksheets to a Dashboard</a>
      <a href="lab7-sql.html"><span class="lbl">Lab 7 &middot; Week 7</span>SQL Fundamentals</a>
      <a href="lab8-security.html"><span class="lbl">Lab 8 &middot; Week 8</span>Security &amp; Data Governance: The Audit</a>
      <div class="dd-sep"></div>
      <a class="soon" href="#"><span class="lbl">Labs 9&ndash;10</span>AI/ML, Information Architecture (in progress)</a>
      '''

for fn in glob.glob('*.html'):
    t = open(fn).read(); orig = t
    t = re.sub(r'(<div class="dd-menu" id="ddc">).*?(</div>\s*</div>)', lambda m: m.group(1)+DDC+m.group(2), t, count=1, flags=re.S)
    t = re.sub(r'(<div class="dd-menu" id="ddl">).*?(</div>\s*</div>)', lambda m: m.group(1)+DDL+m.group(2), t, count=1, flags=re.S)
    # mark this page current in its own menu
    t = t.replace(f'<a href="{fn}">', f'<a class="current" href="{fn}">')
    if t != orig:
        open(fn, 'w').write(t); print('nav normalized:', fn)

# ---------------- index body ----------------
t = open('index.html').read()

# stale week numbers on chapter cards
for old, new in [('Chapter 2 · Week 2 · Competitive advantage', 'Chapter 2 · Week 3 · Competitive advantage'),
                 ('Chapter 3 · Week 3 · Business processes',    'Chapter 3 · Week 4 · Business processes'),
                 ('Chapter 4 · Week 4 · Systems analysis',      'Chapter 4 · Week 5 · Systems analysis'),
                 ('Chapter 6 · Week 5 · Enterprise systems',    'Chapter 6 · Week 7 · Enterprise systems')]:
    assert old in t, old
    t = t.replace(old, new)

CH5_CARD = '''  <div class="chapter-card">
      <div class="chapter-header"><div><div class="chapter-num">Chapter 5 · Week 7 · Databases</div>
        <div class="chapter-title">What Data Is: Databases, and the Company That Built Itself on One</div>
        <div class="chapter-company">Walmart · Retail Link · one receipt at a time</div></div>
        <div class="chapter-links"><a class="btn btn-solid" href="chapter5-walmart.html">Read Case →</a><a class="btn btn-outline" href="lab7-sql.html">Lab 7</a></div></div>
      <div class="chapter-body">
        <div><h5>Concepts</h5><ul><li>Records, fields, formats</li><li>Why one big grid breaks</li><li>The relational model</li><li>Normalization</li></ul></div>
        <div><h5>Business topics</h5><ul><li>A company built on a database</li><li>From records to answers</li><li>The other side: what the basket reveals</li></ul></div>
        <div><h5>In the lab</h5><ul><li>Query the real co-op database</li><li>JOINs across seven tables</li><li>The finding, re-found in SQL</li></ul></div>
      </div>
    </div>
'''

CH9_CARD = '''  <div class="chapter-card">
      <div class="chapter-header"><div><div class="chapter-num">Chapter 9 · Week 8 · Cybersecurity</div>
        <div class="chapter-title">The Password That Stopped American Healthcare</div>
        <div class="chapter-company">Change Healthcare / UnitedHealth Group, 2024</div></div>
        <div class="chapter-links"><a class="btn btn-solid" href="chapter9-changehealthcare.html">Read Case →</a><a class="btn btn-outline" href="lab8-security.html">Lab 8</a></div></div>
      <div class="chapter-body">
        <div><h5>Concepts</h5><ul><li>The CIA triad</li><li>Ransomware &amp; RaaS</li><li>MFA &amp; the kill chain</li><li>Least privilege · concentration risk</li></ul></div>
        <div><h5>Business topics</h5><ul><li>A third of US claims, frozen</li><li>$22M paid, leaked anyway</li><li>Business continuity</li><li>Security careers without code</li></ul></div>
        <div><h5>In the lab</h5><ul><li>Play the security lead</li><li>Verify the phish with a query</li><li>Price a dark day</li></ul></div>
      </div>
    </div>
'''

CH10_CARD = '''  <div class="chapter-card">
      <div class="chapter-header"><div><div class="chapter-num">Chapter 10 · Week 8 · IT Governance</div>
        <div class="chapter-title">When Everyone Was Responsible and No One Was</div>
        <div class="chapter-company">Equifax, 2017</div></div>
        <div class="chapter-links"><a class="btn btn-solid" href="chapter10-equifax.html">Read Case →</a><a class="btn btn-outline" href="lab8-security.html">Lab 8</a></div></div>
      <div class="chapter-body">
        <div><h5>Concepts</h5><ul><li>Governance vs. management</li><li>Responsibility vs. accountability</li><li>Frameworks: COBIT, NIST</li><li>Compliance is not security</li></ul></div>
        <div><h5>Business topics</h5><ul><li>A patch nobody applied</li><li>The product was people</li><li>Data about people who never agreed</li></ul></div>
        <div><h5>In the lab</h5><ul><li>Feeds Lab 8's access map</li><li>The memo to the board</li></ul></div>
      </div>
    </div>
'''

# Ch5 before the Ch6 card, Ch9 + Ch10 after it
ch6_start = t.index('<div class="chapter-card">\n      <div class="chapter-header"><div><div class="chapter-num">Chapter 6')
# the card opener includes two leading spaces in source; back up to them
ch6_start = t.rindex('  <div class="chapter-card">', 0, ch6_start + 10)
t = t[:ch6_start] + CH5_CARD + t[ch6_start:]
ch6_end = t.index('</div>\n    </div>\n', t.index('Chapter 6 · Week 7')) + len('</div>\n    </div>\n')
# that lands after chapter-body close + card close of ch6
t = t[:ch6_end] + CH9_CARD + CH10_CARD + t[ch6_end:]

# lab strip: real Lab 8 card + labs 9-10 soon; fix stale titles and checkpoint counts
t = t.replace('<div class="lab-card"><div class="lab-num">Labs 8–10</div><h4>UX · AI/ML · Information Architecture</h4><p class="soon">In progress: UX and IA await the lab professor\'s input.</p></div>',
 '''<a class="lab-card" href="lab8-security.html"><div class="lab-num">Lab 8 · Week 8</div><h4>Security &amp; Data Governance: The Audit</h4><p>Play the security lead: audit the data, kill the phish with a query. 8 checkpoints.</p></a>
      <div class="lab-card"><div class="lab-num">Labs 9–10</div><h4>AI/ML · Information Architecture</h4><p class="soon">In progress: IA awaits the lab professor's input.</p></div>''')
t = t.replace('The three-light policy, set before anything else. 4 checkpoints.', 'The three-light policy, set before anything else. 6 checkpoints.')
t = t.replace('<h4>Data Visualization: Communicating Status</h4><p>Honest dashboards, paired with Healthcare.gov. 6 checkpoints.</p>',
              '<h4>Data Visualization: Charts That Tell the Truth</h4><p>Build honest charts, then diagnose misleading ones. 8 checkpoints.</p>')
t = t.replace('<h4>Tableau: Seeing the Co-op</h4><p>The finding, re-found visually. 7 checkpoints.</p>',
              '<h4>Data Visualization with Tableau</h4><p>The finding, re-found visually. 8 checkpoints.</p>')
t = t.replace('<h4>SQL: Asking Directly</h4><p>Live in-browser sandbox on the real database. 7 checkpoints.</p>',
              '<h4>SQL: Cleaning Data at the Source</h4><p>Live in-browser sandbox on the real database. 10 checkpoints.</p>')
t = t.replace('Ten labs across the quarter; seven are live.', 'Ten labs across the quarter; eight are live.')

open('index.html', 'w').write(t)
print('index cards + lab strip updated')
