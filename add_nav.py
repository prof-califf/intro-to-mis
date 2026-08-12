"""Injects the global dropdown navigation into every chapter and lab page.
Idempotent: running twice does not duplicate the nav.
Run after any chapter reassembly or lab rebuild."""
import re, glob, os

CHAPTERS = [
    ("chapter0-what-is-mis.html",            "Chapter 0 &middot; Week 1", "What Is MIS? &mdash; Spotify Wrapped"),
    ("chapter1-starbucks.html",              "Chapter 1 &middot; Week 2", "The Value of Information &mdash; Starbucks"),
    ("chapter2-competitive-advantage.html",  "Chapter 2 &middot; Week 2", "Technology &amp; Competitive Advantage &mdash; Zara"),
    ("chapter3-dominos.html",                "Chapter 3 &middot; Week 3", "Business Processes &mdash; Domino's"),
    ("chapter4-healthcaregov.html",          "Chapter 4 &middot; Week 4", "Systems Analysis &amp; the SDLC &mdash; Healthcare.gov"),
    ("chapter6-nike-sap.html",               "Chapter 6 &middot; Week 5", "Enterprise Systems &mdash; Nike/SAP"),
    (None,                                   "Chapters 5, 7&ndash;12",    "Databases, BI, AI/ML, Security, Cloud, IoT"),
]

LABS = [
    ("lab1-genai.html",           "Lab 1 &middot; Week 1", "GenAI for Thinking"),
    ("lab2-excel-basics.html",    "Lab 2 &middot; Week 2", "Excel Basics: Meeting the Client"),
    ("lab3-excel-dataprep.html",  "Lab 3 &middot; Week 3", "Data Preparation: The RAW File"),
    ("lab4-excel-dataviz.html",   "Lab 4 &middot; Week 4", "Data Visualization: Charts That Tell the Truth"),
    ("lab5-excel-analysis.html",  "Lab 5 &middot; Week 5", "Data Analysis &amp; Mini Project"),
    ("lab6-tableau.html",         "Lab 6 &middot; Week 6", "Tableau: Worksheets to a Dashboard"),
    ("lab7-sql.html",             "Lab 7 &middot; Week 7", "SQL Fundamentals"),
    (None,                        "Labs 8&ndash;10",      "UX, AI/ML, Information Architecture"),
]

DATA = [
    ("cascadia-sales-2025.xlsx",     "Workbook", "Cascadia sales, clean (.xlsx)"),
    ("cascadia-sales-2025-RAW.xlsx", "Workbook", "Cascadia sales, RAW for Lab 3 (.xlsx)"),
    ("cascadia-sales-2025.csv",      "Data",     "Flat CSV for Tableau"),
    ("cascadia.db",                  "Database", "SQLite database for the SQL lab"),
]


def menu(items, current):
    out = []
    for href, label, title in items:
        if href is None:
            out.append('<div class="dd-sep"></div>')
            out.append(f'<a class="soon" href="#"><span class="lbl">{label}</span>{title} (in progress)</a>')
        else:
            cls = ' class="current"' if href == current else ''
            out.append(f'<a{cls} href="{href}"><span class="lbl">{label}</span>{title}</a>')
    return "\n      ".join(out)


def nav_html(current):
    return f'''<nav class="topnav">
  <div class="topnav-in">
    <a class="topnav-brand" href="index.html">MIS 320 &middot; Intro to Information Systems</a>
    <a class="dd-btn" href="schedule.html" style="text-decoration:none">Schedule</a>
    <div class="dd">
      <button class="dd-btn" aria-expanded="false" aria-haspopup="true" data-dd="ddc">Chapters<span class="caret">&#9660;</span></button>
      <div class="dd-menu" id="ddc">
      {menu(CHAPTERS, current)}
      </div>
    </div>
    <div class="dd">
      <button class="dd-btn" aria-expanded="false" aria-haspopup="true" data-dd="ddl">Labs<span class="caret">&#9660;</span></button>
      <div class="dd-menu" id="ddl">
      {menu(LABS, current)}
      </div>
    </div>
    <div class="dd">
      <button class="dd-btn" aria-expanded="false" aria-haspopup="true" data-dd="ddd">Data<span class="caret">&#9660;</span></button>
      <div class="dd-menu" id="ddd">
      {menu(DATA, current)}
      </div>
    </div>
  </div>
</nav>
'''

NAV_JS = '''<script>
(function(){
  var btns=[].slice.call(document.querySelectorAll('.dd-btn'));
  function closeAll(except){
    btns.forEach(function(b){
      var m=document.getElementById(b.getAttribute('data-dd'));
      if(m&&m!==except){m.classList.remove('open');b.setAttribute('aria-expanded','false');}
    });
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(e){
      e.stopPropagation();
      var m=document.getElementById(b.getAttribute('data-dd'));
      var open=m.classList.contains('open');
      closeAll();
      if(!open){m.classList.add('open');b.setAttribute('aria-expanded','true');}
    });
  });
  document.addEventListener('click',function(){closeAll();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll();});
  document.querySelectorAll('.dd-menu').forEach(function(m){
    m.addEventListener('click',function(e){e.stopPropagation();});
  });
})();
</script>
'''


def inject(path):
    s = open(path).read()
    name = os.path.basename(path)
    if 'class="topnav"' in s:                      # replace existing nav (idempotent)
        s = re.sub(r'<nav class="topnav">.*?</nav>\n?', '', s, flags=re.S)
    if '<!--NAVJS-->' not in s:
        s = s.replace('</body>', '<!--NAVJS-->\n' + NAV_JS + '</body>')
    else:
        s = re.sub(r'<!--NAVJS-->\n<script>\n\(function\(\)\{\n  var btns.*?</script>\n', '<!--NAVJS-->\n' + NAV_JS, s, flags=re.S)
    s = s.replace('<body>', '<body>\n' + nav_html(name), 1)
    open(path, 'w').write(s)
    return name


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'))
    done = []
    for f in sorted(glob.glob('chapter*.html') + glob.glob('lab*.html') + glob.glob('schedule.html') + glob.glob('join-builder.html')):
        done.append(inject(f))
    print(f"nav injected into {len(done)} pages")
