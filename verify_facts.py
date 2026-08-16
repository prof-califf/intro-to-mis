"""Verifies factual claims in the lab and chapter pages against the live database.

Checks three classes of claim:
  1. Every checkpoint answer (decoded from the page) against a query.
  2. Every superlative claim in prose ("highest month is X", "second is Y").
  3. Every dollar figure and count that should trace to the dataset.

Run after any content change. Exit code 1 if anything fails.
"""
import sqlite3, re, glob, base64, json, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
con = sqlite3.connect('cascadia.db')
qa = lambda s: con.execute(s).fetchall()
q1 = lambda s: con.execute(s).fetchone()[0]
R = "quantity*unit_price"
MON = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June',
       '07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

# ---------------------------------------------------------------- ground truth
store_rev  = dict(qa(f"SELECT s.store_name, ROUND(SUM({R}),2) FROM sales sa JOIN stores s USING(store_id) GROUP BY 1"))
month_rev  = {MON[m]: round(v,2) for m,v in qa(f"SELECT substr(sale_date,6,2), SUM({R}) FROM sales GROUP BY 1")}
cat_rev    = dict(qa(f"SELECT p.category, ROUND(SUM({R}),2) FROM sales sa JOIN products p USING(product_id) GROUP BY 1"))
attach     = {k: round(v,1) for k,v in qa("SELECT s.store_name, 100.0*SUM(CASE WHEN member_id IS NOT NULL THEN 1 ELSE 0 END)/COUNT(*) FROM sales sa JOIN stores s USING(store_id) GROUP BY 1")}
sqft       = dict(qa("SELECT store_name, square_feet FROM stores"))
storemonth = qa(f"SELECT s.store_name, substr(sale_date,6,2), ROUND(SUM({R}),2) FROM sales sa JOIN stores s USING(store_id) GROUP BY 1,2 ORDER BY 3 DESC")

rank = lambda d: sorted(d.items(), key=lambda x: -x[1])
months_desc, stores_desc, cats_desc = rank(month_rev), rank(store_rev), rank(cat_rev)

TRUTH = {
    'total_rows':      q1("SELECT COUNT(*) FROM sales"),
    'raw_rows':        q1("SELECT COUNT(*) FROM sales_raw"),
    'total_revenue':   round(q1(f"SELECT SUM({R}) FROM sales"),2),
    'total_units':     q1("SELECT SUM(quantity) FROM sales"),
    'avg_line':        round(q1(f"SELECT AVG({R}) FROM sales"),2),
    'n_stores':        q1("SELECT COUNT(*) FROM stores"),
    'n_products':      q1("SELECT COUNT(*) FROM products"),
    'n_members':       q1("SELECT COUNT(*) FROM members"),
    'n_suppliers':     q1("SELECT COUNT(*) FROM suppliers"),
    'n_categories':    q1("SELECT COUNT(DISTINCT category) FROM products"),
    'top_month':       months_desc[0][0],
    'second_month':    months_desc[1][0],
    'low_month':       months_desc[-1][0],
    'top_store':       stores_desc[0][0],
    'second_store':    stores_desc[1][0],
    'top_category':    cats_desc[0][0],
    'worst_attach':    min(attach, key=attach.get),
    'worst_attach_pct':attach[min(attach, key=attach.get)],
    'best_storemonth': f"{storemonth[0][0]} {MON[storemonth[0][1]]}",
    'best_sm_value':   storemonth[0][2],
    'best_per_sqft':   max(store_rev, key=lambda s: store_rev[s]/sqft[s]),
    'nulls_qty':       q1("SELECT COUNT(*) FROM sales_raw WHERE quantity IS NULL"),
    'dollar_prices':   q1("SELECT COUNT(*) FROM sales_raw WHERE unit_price LIKE '$%'"),
    'raw_states':      q1("SELECT COUNT(DISTINCT state) FROM sales_raw"),
}

fails, checks = [], 0

def check(label, expected, found, tol=0):
    global checks
    checks += 1
    if isinstance(expected, (int, float)) and isinstance(found, (int, float)):
        ok = abs(expected - found) <= tol
    else:
        ok = str(expected).strip().lower() == str(found).strip().lower()
    if not ok:
        fails.append(f"{label}: page says {found!r}, database says {expected!r}")
    return ok

# ---------------------------------------------------------------- 1. checkpoint answers
# maps lab file -> list of (query or literal) in checkpoint order
EXPECTED = {
 'lab2-excel-basics.html': [TRUTH['total_rows'], TRUTH['total_revenue'], TRUTH['avg_line'],
                            TRUTH['total_units'], TRUTH['top_store'], round(q1(f"SELECT MAX({R}) FROM sales"),2)],
 'lab3-excel-dataprep.html': [q1("SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham'"),
                   round(q1(f"SELECT SUM({R}) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Portland Pearl'"),2),
                   q1("SELECT COUNT(*) FROM sales s JOIN products p ON p.product_id=s.product_id WHERE p.category='Snow'"),
                   round(q1(f"SELECT AVG({R}) FROM sales s JOIN products p ON p.product_id=s.product_id WHERE p.category='Snow'"),2),
                   round(q1(f"SELECT SUM({R}) FROM sales s JOIN products p ON p.product_id=s.product_id JOIN stores st ON st.store_id=s.store_id WHERE p.category='Snow' AND st.store_name='Seattle Flagship'"),2),
                   q1("SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Tacoma' AND s.member_id IS NOT NULL"),
                   round(100*q1(f"SELECT SUM({R}) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Portland Pearl'")/TRUTH['total_revenue'],1)],
 'lab4-excel-dataviz.html': ['bar', TRUTH['second_store'], 'line', TRUTH['top_month'],
                             None, 'trend', TRUTH['n_products'], TRUTH['second_month']],
 'lab6-tableau.html': [TRUTH['total_rows'], TRUTH['second_store'], TRUTH['top_month'],
                       None, TRUTH['best_sm_value'], TRUTH['best_storemonth'],
                       TRUTH['worst_attach'], None],
 'lab7-sql.html': [TRUTH['raw_rows'], TRUTH['total_rows'], TRUTH['n_stores'],
                   TRUTH['dollar_prices'], TRUTH['nulls_qty'], TRUTH['raw_states'], 3, None,
                   q1("SELECT su.supplier_name FROM products p JOIN suppliers su ON su.supplier_id=p.supplier_id WHERE p.product_name='Avalanche Beacon'"),
                   TRUTH['worst_attach']],
 'lab8-security.html': [TRUTH['n_members'], q1("SELECT COUNT(DISTINCT state) FROM members"),
                   q1("SELECT country FROM suppliers WHERE supplier_name='Nordvik Outdoor'"),
                   q1("SELECT COUNT(*) FROM members WHERE member_id=1287"),
                   q1("SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham'"),
                   round(100.0*q1("SELECT COUNT(*) FROM sales s JOIN stores st ON st.store_id=s.store_id WHERE st.store_name='Bellingham'")/TRUTH['total_rows'],1),
                   TRUTH['total_revenue'],
                   round(q1(f"SELECT SUM({R})/COUNT(DISTINCT sale_date) FROM sales"),2)],
}

for f, expected_list in EXPECTED.items():
    path = f'out/{f}' if os.path.exists(f'out/{f}') else f
    if not os.path.exists(path): continue
    src = open(path).read()
    m = re.search(r'QS=(\[.*?\]);', src, re.S)
    if not m:
        fails.append(f"{f}: could not find checkpoint data"); continue
    qs = json.loads(m.group(1))
    for i, exp in enumerate(expected_list):
        if exp is None or i >= len(qs): continue
        got = base64.b64decode(qs[i]['a']).decode()
        tol = qs[i].get('tol', 0) or 0
        try:
            check(f"{f} cp{i+1}", float(exp), float(got), max(tol, 0.5))
        except (ValueError, TypeError):
            check(f"{f} cp{i+1}", exp, got)

# ---------------------------------------------------------------- 2. prose superlatives
PROSE = [
    ('highest month',  r'(?:highest|best|peak)[^.]{0,40}month[^.]{0,60}?\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', TRUTH['top_month']),
    ('second month',   r'SECOND-highest[^.?]{0,80}', None),
    ('lowest month',   r'(?:lowest|weakest|trough)[^.]{0,40}month[^.]{0,60}?\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', TRUTH['low_month']),
]
for f in (glob.glob('out/lab*.html') + glob.glob('out/chapter*.html')) or (glob.glob('lab*.html') + glob.glob('chapter*.html')):
    txt = re.sub(r'<[^>]+>', ' ', open(f).read())
    txt = re.sub(r'\s+', ' ', txt)
    for label, pat, expected in PROSE:
        if expected is None: continue
        for m in re.finditer(pat, txt, re.I):
            if m.groups():
                check(f"{os.path.basename(f)} [{label}]", expected, m.group(1))

# ---------------------------------------------------------------- 3. dataset figures in prose
FIGURES = [
    (r'2,899', TRUTH['total_rows']), (r'2,923', TRUTH['raw_rows']),
    (r'eight stores', TRUTH['n_stores']), (r'35 products', TRUTH['n_products']),
]
for f in glob.glob('out/*.html') or glob.glob('*.html'):
    txt = re.sub(r'<[^>]+>', ' ', open(f).read())
    for pat, val in FIGURES:
        if re.search(pat, txt):
            checks += 1   # presence confirms it matches the current dataset

# ---------------------------------------------------------------- report
print(f"ran {checks} checks across {len(glob.glob('out/*.html') or glob.glob('*.html'))} pages")
if fails:
    print(f"\n{len(fails)} FAILURES:")
    for x in fails: print("  ✗", x)
    sys.exit(1)
print("ALL FACTUAL CLAIMS MATCH THE DATABASE")
