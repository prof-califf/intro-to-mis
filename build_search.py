"""Build the site search index (search-index.js) for search.html.

Run from the repo folder after changing any chapter, lab, or reference page:
    python3 build_search.py

It also gives every h3 heading (and every glossary term) an id, so search
results can link straight to the right spot. Running it twice is safe.
"""
import json
import re
import glob
from bs4 import BeautifulSoup, NavigableString

PAGES = (
    sorted(glob.glob('chapter*.html'), key=lambda f: int(re.search(r'\d+', f).group()))
    + [f for f in sorted(glob.glob('lab*.html'), key=lambda f: int(re.search(r'\d+', f).group()))
       if '-hidden' not in f]
    + ['sql-bootcamp.html', 'python-bootcamp.html', 'tableau-bootcamp.html', 'glossary.html', 'syllabus.html', 'schedule.html', 'preface.html', 'resume.html']
)
SKIP_CLASSES = {'srcbox', 'printbox', 'toc', 'pn', 'skiplink', 'tocbtn'}


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60]


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def add_ids(path):
    """Give h3 headings and glossary terms stable ids. Edits the file in place
    with plain string replacement so nothing else in the page changes."""
    raw = open(path, encoding='utf-8').read()
    out, used = raw, set(re.findall(r'id="([^"]+)"', raw))

    def give(tag_re, prefix):
        nonlocal out
        def sub(m):
            attrs, inner = m.group(1), m.group(2)
            if 'id=' in attrs:
                return m.group(0)
            text = clean(re.sub(r'<[^>]+>', ' ', inner))
            num = re.match(r'(\d+(?:\.\d+)*)', text)
            base = prefix + (num.group(1).replace('.', '-') if num else slug(text))
            new, k = base, 2
            while new in used:
                new, k = f'{base}-{k}', k + 1
            used.add(new)
            return m.group(0).replace(m.group(1), attrs + f' id="{new}"', 1) if attrs else \
                m.group(0).replace(f'<{m.group(0)[1:3]}>', f'<{m.group(0)[1:3]} id="{new}">', 1)
        out = re.sub(tag_re, sub, out, flags=re.S)

    give(r'<h3((?:\s[^>]*)?)>(.*?)</h3>', 's')
    if path == 'glossary.html':
        give(r'<dt((?:\s[^>]*)?)>(.*?)</dt>', 'g-')
    if out != raw:
        open(path, 'w', encoding='utf-8').write(out)


def page_title(soup):
    h1 = soup.find('h1')
    t = clean(h1.get_text(' ')) if h1 else ''
    return t or clean(soup.title.get_text()).split('|')[0].strip()


def index_page(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    main = soup.find('main') or soup.body
    for bad in main.find_all(['script', 'style', 'nav', 'svg', 'canvas', 'button', 'sup']):
        bad.decompose()
    for bad in main.find_all(class_=lambda c: c and SKIP_CLASSES & set(c.split() if isinstance(c, str) else c)):
        bad.decompose()
    for blk in main.find_all(['p', 'li', 'div', 'td', 'th', 'dd', 'dt', 'h2', 'h3', 'h4', 'br', 'figcaption', 'span']):
        if blk.name == 'span' and 'lbl' not in (blk.get('class') or []):
            continue
        blk.append(' ')
    title = page_title(soup)
    entries, cur = [], {'a': '', 's': title, 't': []}

    def flush():
        text = clean(''.join(cur['t']))
        if len(text) > 30:
            entries.append({'u': path + ('#' + cur['a'] if cur['a'] else ''), 's': cur['s'], 'x': text})

    for el in main.descendants:
        if getattr(el, 'name', None) in ('h2', 'h3', 'dt') and el.get('id'):
            flush()
            cur = {'a': el['id'], 's': clean(el.get_text(' ')), 't': []}
            if el.name == 'dt':
                cur['t'].append(cur['s'])
        elif isinstance(el, NavigableString) and el.parent.name not in ('h2', 'h3', 'dt'):
            cur['t'].append(str(el))
    flush()
    return title, entries


def main():
    docs = []
    for p in PAGES:
        add_ids(p)
        title, entries = index_page(p)
        docs.append({'p': p, 'title': title, 'e': entries})
    js = 'window.SEARCH_INDEX=' + json.dumps(docs, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open('search-index.js', 'w', encoding='utf-8').write(js)
    n = sum(len(d['e']) for d in docs)
    print(f'{len(docs)} pages, {n} sections, {len(js)//1024} KB')


if __name__ == '__main__':
    main()
