"""Leak and link check. Run after build.py; exits non-zero on any problem.

Fails if the built site or its sources contain an email address, the word
"outbox", or any term listed in .blocklist (a local, gitignored file with one
term per line). Also checks that every internal link points at a built page.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HREF = re.compile(r'href="(/[^"#]*)"')


def blocklist():
    path = os.path.join(HERE, ".blocklist")
    if not os.path.exists(path):
        print("note: .blocklist is missing; only emails and 'outbox' are checked")
        return []
    return [t.strip() for t in open(path, encoding="utf-8") if t.strip() and not t.startswith("#")]


def files():
    for d, dirs, names in os.walk(HERE):
        dirs[:] = [x for x in dirs if x not in (".git", ".venv", "__pycache__")]
        for n in names:
            if n.endswith((".html", ".md", ".css")):
                yield os.path.join(d, n)


def main():
    terms = [(t, re.compile(re.escape(t), re.I)) for t in blocklist() + ["outbox"]]
    problems = []
    for path in files():
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        rel = os.path.relpath(path, HERE)
        for m in EMAIL.finditer(text):
            problems.append(f"{rel}: email-like text '{m.group(0)}'")
        for t, rx in terms:
            if rx.search(text):
                problems.append(f"{rel}: blocked term '{t}'")
        if rel.endswith(".html"):
            for href in HREF.findall(text):
                target = os.path.join(HERE, href.lstrip("/"))
                if not (os.path.isfile(target) or os.path.isfile(os.path.join(target, "index.html"))):
                    problems.append(f"{rel}: broken internal link {href}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("check passed: no emails, no blocked terms, no broken internal links")


if __name__ == "__main__":
    main()
