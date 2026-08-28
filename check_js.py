#!/usr/bin/env python3
"""Parse every inline <script> block in every page and report syntax errors.

verify_facts.py checks the numbers. This checks the code. A single unescaped
apostrophe in a JS string kills an entire script block with no visible error
on the page, which is how Lab 8's SQL sandbox was broken.

Run before every deploy. Exits nonzero if anything fails.
"""
import re, subprocess, sys, glob, os, shutil, tempfile, pathlib

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not shutil.which('node'):
    print("node not found; cannot check JavaScript. Install Node or skip this check.")
    sys.exit(2)

failures = []
blocks = 0

for path in sorted(glob.glob('*.html')):
    text = pathlib.Path(path).read_text()
    for i, body in enumerate(re.findall(r'<script[^>]*>(.*?)</script>', text, re.S)):
        if not body.strip():
            continue
        blocks += 1
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as fh:
            fh.write(body)
            tmp = fh.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode:
            msg = next((ln.strip() for ln in r.stderr.splitlines()
                        if 'Error' in ln), r.stderr.strip()[:120])
            failures.append((path, i, msg))

    # unbalanced divs usually mean a botched edit
    if text.count('<div') != text.count('</div>'):
        failures.append((path, '-', f"div mismatch: {text.count('<div')} open, "
                                    f"{text.count('</div>')} close"))

print(f"checked {blocks} script blocks across {len(glob.glob('*.html'))} pages")
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for path, i, msg in failures:
        print(f"  {path}  block {i}  {msg}")
    sys.exit(1)
print("all clean")
