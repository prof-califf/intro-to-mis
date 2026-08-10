"""
Cascadia Outfitters — canonical dataset for MIS 320 Labs 2-7.
Member-owned Pacific Northwest outdoor gear co-op, modeled on REI.

DETERMINISTIC: fixed seed, fixed iteration order. Re-running reproduces byte-identical
output, so every student sees identical numbers and checkpoints stay valid.

PLANTED ANOMALY
  Bellingham's member attach rate collapses to ~50%; all other stores sit 89-94%.
  The CAUSE is deliberately absent from the data. Students rediscover it across
  Excel (L3/L4), Tableau (L6), SQL (L7) and process modeling (Week 4 in class).
"""
import csv, json, random, sqlite3, datetime as dt, os

SEED = 320
random.seed(SEED)
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- stores
# (id, name, region, opened, sqft, member_attach_target)
STORES = [
    (1, "Seattle Flagship",  "Puget Sound",   2004, 74000, 0.93),
    (2, "Bellevue",          "Puget Sound",   2011, 41000, 0.91),
    (3, "Tacoma",            "Puget Sound",   2014, 36000, 0.89),
    (4, "Bellingham",        "North Cascades",2019, 38000, 0.50),   # <-- anomaly
    (5, "Spokane",           "Inland",        2009, 33000, 0.90),
    (6, "Portland Pearl",    "Willamette",    2007, 62000, 0.94),
    (7, "Eugene",            "Willamette",    2016, 29000, 0.90),
    (8, "Boise",             "Inland",        2021, 31000, 0.92),
]

# ---------------------------------------------------------------- suppliers
SUPPLIERS = [
    (1, "Olympic Down Works",    "USA",     18),
    (2, "Cascade Textiles",      "USA",     24),
    (3, "Kitsap Forge",          "USA",     30),
    (4, "Nordvik Outdoor",       "Norway",  56),
    (5, "Sanko Technical",       "Japan",   62),
    (6, "Andes Alpaca Co-op",    "Peru",    48),
    (7, "Fraser Valley Rubber",  "Canada",  21),
]

# ---------------------------------------------------------------- products
# (id, name, category, supplier, cost, price, seasonality)
#   seasonality: 'summer' | 'winter' | 'flat'
P = [
    ("Alpine 45L Pack",          "Camping",  1, 78.00, 189.00, "summer"),
    ("Basecamp 65L Pack",        "Camping",  1, 96.00, 229.00, "summer"),
    ("Ridgeline 2P Tent",        "Camping",  2,142.00, 349.00, "summer"),
    ("Ridgeline 3P Tent",        "Camping",  2,168.00, 419.00, "summer"),
    ("Nimbus 20F Sleeping Bag",  "Camping",  1,104.00, 259.00, "summer"),
    ("Nimbus 0F Sleeping Bag",   "Camping",  1,138.00, 339.00, "winter"),
    ("Trailhead Sleeping Pad",   "Camping",  5, 41.00,  99.00, "summer"),
    ("Cascade Camp Stove",       "Camping",  3, 34.00,  84.00, "summer"),
    ("Titanium Cook Set",        "Camping",  5, 47.00, 115.00, "flat"),
    ("Headlamp 400",             "Camping",  5, 16.00,  44.00, "flat"),

    ("Summit Shell Jacket",      "Apparel",  2,121.00, 299.00, "winter"),
    ("Stormbreak Rain Jacket",   "Apparel",  2, 68.00, 169.00, "flat"),
    ("Down Sweater",             "Apparel",  1, 74.00, 185.00, "winter"),
    ("Alpaca Base Layer",        "Apparel",  6, 29.00,  78.00, "winter"),
    ("Merino Hiking Socks",      "Apparel",  6,  8.50,  24.00, "flat"),
    ("Trail Convertible Pant",   "Apparel",  2, 36.00,  89.00, "summer"),
    ("Fleece Quarter-Zip",       "Apparel",  2, 31.00,  79.00, "winter"),
    ("Sun Hoody",                "Apparel",  2, 24.00,  62.00, "summer"),

    ("Approach Shoe",            "Footwear", 7, 52.00, 129.00, "summer"),
    ("Backcountry Boot",         "Footwear", 7, 88.00, 219.00, "winter"),
    ("Trail Runner GTX",         "Footwear", 7, 61.00, 149.00, "summer"),
    ("Insulated Camp Bootie",    "Footwear", 6, 22.00,  59.00, "winter"),

    ("Vertex Climbing Harness",  "Climbing", 3, 43.00, 105.00, "flat"),
    ("Dynamic Rope 60m",         "Climbing", 4, 98.00, 239.00, "flat"),
    ("Belay Device",             "Climbing", 3, 19.00,  49.00, "flat"),
    ("Chalk Bag",                "Climbing", 3,  9.00,  26.00, "flat"),
    ("Quickdraw Set of 6",       "Climbing", 4, 62.00, 155.00, "flat"),

    ("Touring Ski Package",      "Snow",     4,412.00, 949.00, "winter"),
    ("Avalanche Beacon",         "Snow",     4,178.00, 399.00, "winter"),
    ("Snowshoe Kit",             "Snow",     3, 76.00, 179.00, "winter"),
    ("Ski Skins",                "Snow",     4, 84.00, 199.00, "winter"),

    ("Inflatable Kayak",         "Water",    7,289.00, 699.00, "summer"),
    ("Dry Bag 30L",              "Water",    7, 17.00,  42.00, "summer"),
    ("PFD Vest",                 "Water",    3, 38.00,  95.00, "summer"),
    ("Paddle Carbon",            "Water",    5,112.00, 279.00, "summer"),
]
PRODUCTS = [(i + 101, n, c, s, cost, price, seas) for i, (n, c, s, cost, price, seas) in enumerate(P)]

# ---------------------------------------------------------------- members
FIRST = ["Ana","Marcus","Priya","Tomas","Grace","Liam","Yuki","Devon","Rosa","Ibrahim",
         "Skye","Nathan","Mei","Owen","Freya","Caleb","Nadia","Jonas","Elena","Theo",
         "Rani","Silas","Maya","Beckett","Noor","Iris","Emmett","Zara","Hollis","June"]
LAST  = ["Okafor","Lindqvist","Ramirez","Chen","Whitcomb","Torres","Nakamura","Boyd","Delgado","Haddad",
         "Petersen","Moreau","Zhang","Kelleher","Bjornstad","Ruiz","Farrow","Ito","Vargas","Quinn",
         "Salas","Andersen","Pham","Coates","Rahimi","Lund","Barros","Novak","Whitfield","Ames"]
CITIES = [("Seattle","WA"),("Bellevue","WA"),("Tacoma","WA"),("Bellingham","WA"),("Spokane","WA"),
          ("Portland","OR"),("Eugene","OR"),("Boise","ID"),("Olympia","WA"),("Vancouver","WA")]

members = []
for i in range(1, 61):
    city, state = CITIES[(i - 1) % len(CITIES)]
    mtype = "Lifetime" if i % 7 == 0 else "Standard"
    year = 2015 + ((i * 3) % 10)
    month = 1 + ((i * 5) % 12)
    day = 1 + ((i * 11) % 28)
    members.append((i + 1000, FIRST[(i - 1) % 30], LAST[(i * 7 - 1) % 30],
                    city, state, mtype, f"{year}-{month:02d}-{day:02d}"))

# ---------------------------------------------------------------- sales
START = dt.date(2025, 1, 1)
DAYS = 365
TARGET_ROWS = 2899

# store share of volume, roughly proportional to sqft with flagship weighting
weights = {1: 0.21, 2: 0.13, 3: 0.11, 4: 0.11, 5: 0.10, 6: 0.18, 7: 0.08, 8: 0.08}

def season_mult(seas, month):
    if seas == "summer":
        return {1:.35,2:.40,3:.60,4:.95,5:1.35,6:1.75,7:1.95,8:1.85,9:1.30,10:.75,11:.45,12:.35}[month]
    if seas == "winter":
        return {1:1.75,2:1.60,3:1.15,4:.65,5:.35,6:.25,7:.20,8:.25,9:.55,10:1.05,11:1.65,12:1.95}[month]
    return 1.0

store_ids = [s[0] for s in STORES]
store_pick = []
for sid in store_ids:
    store_pick += [sid] * int(round(weights[sid] * 1000))

sales = []
sale_id = 5000
attach = {s[0]: s[5] for s in STORES}

for _ in range(TARGET_ROWS):
    sale_id += 1
    day_offset = random.randrange(DAYS)
    d = START + dt.timedelta(days=day_offset)
    sid = random.choice(store_pick)

    # product chosen with seasonal weighting for that month
    while True:
        prod = random.choice(PRODUCTS)
        if random.random() < season_mult(prod[6], d.month) / 1.95:
            break

    qty = 1 if prod[5] > 200 else random.choice([1, 1, 1, 2, 2, 3])

    # member attach — the planted anomaly lives here
    mid = random.choice(members)[0] if random.random() < attach[sid] else None

    # occasional promotional discount
    unit = prod[5]
    if random.random() < 0.08:
        unit = round(unit * 0.85, 2)

    sales.append((sale_id, d.isoformat(), sid, prod[0], mid, qty, unit))

sales.sort(key=lambda r: (r[1], r[0]))
sales = [(i + 5001, *r[1:]) for i, r in enumerate(sales)]

# ---------------------------------------------------------------- inventory
inventory = []
for sid in store_ids:
    for p in PRODUCTS:
        rp = 8 if p[5] < 100 else 4
        qoh = random.randrange(0, 40)
        inventory.append((sid, p[0], qoh, rp))

# ---------------------------------------------------------------- used gear
CONDITIONS = ["Like New", "Good", "Fair"]
used = []
for i in range(220):
    p = random.choice(PRODUCTS)
    sid = random.choice(store_ids)
    cond = CONDITIONS[i % 3]
    mult = {"Like New": 0.62, "Good": 0.45, "Fair": 0.30}[cond]
    listed = round(p[5] * mult, 2)
    ld = START + dt.timedelta(days=random.randrange(DAYS))
    sold = None
    if random.random() < 0.63:
        sold = (ld + dt.timedelta(days=random.randrange(3, 70))).isoformat()
        if sold > "2025-12-31":
            sold = None
    used.append((i + 9001, p[0], sid, cond, listed, ld.isoformat(), sold))

# ---------------------------------------------------------------- write sqlite
db = os.path.join(OUT, "cascadia.db")
if os.path.exists(db):
    os.remove(db)
con = sqlite3.connect(db)
con.executescript("""
CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT, region TEXT,
  opened_year INTEGER, square_feet INTEGER);
CREATE TABLE suppliers(supplier_id INTEGER PRIMARY KEY, supplier_name TEXT, country TEXT,
  lead_time_days INTEGER);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT,
  supplier_id INTEGER, unit_cost REAL, list_price REAL,
  FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id));
CREATE TABLE members(member_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT,
  city TEXT, state TEXT, member_type TEXT, join_date TEXT);
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, sale_date TEXT, store_id INTEGER,
  product_id INTEGER, member_id INTEGER, quantity INTEGER, unit_price REAL,
  FOREIGN KEY(store_id) REFERENCES stores(store_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id),
  FOREIGN KEY(member_id) REFERENCES members(member_id));
CREATE TABLE inventory(store_id INTEGER, product_id INTEGER, quantity_on_hand INTEGER,
  reorder_point INTEGER, PRIMARY KEY(store_id, product_id));
CREATE TABLE used_gear(item_id INTEGER PRIMARY KEY, product_id INTEGER, store_id INTEGER,
  condition TEXT, listed_price REAL, date_listed TEXT, date_sold TEXT);
""")
con.executemany("INSERT INTO stores VALUES(?,?,?,?,?)", [(a,b,c,d,e) for a,b,c,d,e,_ in STORES])
con.executemany("INSERT INTO suppliers VALUES(?,?,?,?)", SUPPLIERS)
con.executemany("INSERT INTO products VALUES(?,?,?,?,?,?)",
                [(i,n,c,s,cost,price) for i,n,c,s,cost,price,_ in PRODUCTS])
con.executemany("INSERT INTO members VALUES(?,?,?,?,?,?,?)", members)
con.executemany("INSERT INTO sales VALUES(?,?,?,?,?,?,?)", sales)
con.executemany("INSERT INTO inventory VALUES(?,?,?,?)", inventory)
con.executemany("INSERT INTO used_gear VALUES(?,?,?,?,?,?,?)", used)
con.commit()

# ---------------------------------------------------------------- flat CSV (joined export)
smap = {s[0]: s for s in STORES}
pmap = {p[0]: p for p in PRODUCTS}
supmap = {s[0]: s for s in SUPPLIERS}

rows = []
for sid_, date, st, pid, mid, qty, unit in sales:
    p = pmap[pid]; s = smap[st]
    rev = round(qty * unit, 2)
    cost = round(qty * p[4], 2)
    rows.append({
        "sale_id": sid_, "sale_date": date, "store": s[1], "region": s[2],
        "product": p[1], "category": p[2], "supplier": supmap[p[3]][1],
        "quantity": qty, "unit_price": f"{unit:.2f}", "unit_cost": f"{p[4]:.2f}",
        "revenue": f"{rev:.2f}", "gross_margin": f"{rev - cost:.2f}",
        "member_id": mid if mid else "", "is_member": "Y" if mid else "N",
    })

with open(os.path.join(OUT, "cascadia-sales-2025.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

print(json.dumps({"sales": len(sales), "products": len(PRODUCTS), "members": len(members),
                  "inventory": len(inventory), "used_gear": len(used)}, indent=None))
