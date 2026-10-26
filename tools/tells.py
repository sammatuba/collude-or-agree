"""Find phrases that mark machine-written prose ("tells") in Markdown or HTML files.

Usage:  python3 tools/tells.py FILE [FILE ...]
Prints each hit with its line number, then a count per file. Exit code 1 if any hit.

The list is deliberately strict. A hit is not always wrong; read each one and decide.
Allowed exceptions: glossary terms, direct quotes, and code.
"""
import re
import sys

TELLS = [
    r"\bthus\b", r"\btherefore\b", r"\bhence\b",
    r"\bit is (important|worth|useful) (to|noting)", r"\bnote that\b", r"\bin other words\b",
    r"\bdelve", r"\bcrucial", r"\brobust", r"\bleverag", r"\bnuance", r"\blandscape\b", r"\btapestry\b",
    r"\bunderscore", r"\bhighlight", r"\bfoster", r"\bseamless", r"\bpivotal", r"\btestament\b",
    r"\bcomprehensive\b", r"\bholistic\b", r"\bjourney\b", r"\bin summary\b", r"\bto summarize\b",
    r"\boverall,", r"\bultimately\b", r"\bimportantly\b", r"\bnotably\b", r"\binterestingly\b",
    r"\bstated with care\b", r"\bthe main lesson\b", r"\bthe key (insight|idea|point|question)\b",
    r"—", r"\bnot only\b.*\bbut also\b", r"\bthis is exactly\b", r"\bexactly what\b", r"\bprecisely\b",
    r"\bsimply put\b", r"\bput simply\b", r"\blet us\b", r"\bwe believe\b", r"\barguably\b",
    r"\bsharpest\b", r"\bcleanly\b", r"\bneat(ly)?\b", r"\belegant", r"\btrivially\b",
    r"\bserves as\b", r"\bacts as\b", r"\bplays a (key |central )?role\b", r"\bin the context of\b",
    r"\bat its core\b", r"\bboils down\b", r"\bthe bottom line\b", r"\bwhat matters\b",
    r"\bthe short version\b", r"\bhere'?s the thing\b", r"\bin a nutshell\b", r"\bthe takeaway\b",
    r"\bkey takeaway", r"\bgame.changer", r"\bdeep dive\b", r"\bunpack\b", r"\bnavigate\b",
    r"\bshowcase", r"\bvibrant\b", r"\bmeticulous", r"\brealm\b", r"\bparadigm\b",
    r"\bit'?s worth\b", r"\bworth noting\b", r"\bkeep in mind\b", r"\bbear in mind\b",
    r"\bthat said\b", r"\bwith that said\b", r"\bto be clear\b", r"\bto be fair\b",
    r"\bcrucially\b", r"\bfundamentally\b", r"\bessentially\b", r"\bbasically\b",
    r"\bin fact\b", r"\bindeed\b", r"\bof course\b", r"\bclearly\b", r"\bobviously\b",
    r"\bstraightforward\b", r"\bconvincing standard\b", r"\bstark\b", r"\bsubtle\b",
    r"\bthe danger is\b", r"\bthe trap\b", r"\ba trap\b", r"\blook-alike", r"\bsurface\b",
    r"\?\s*$", r"\?\s+[A-Z]",  # rhetorical questions in prose
    r"\bnever (?:just|simply|merely)\b", r"\bmore and more\b", r"\bagain and again\b",
    r"\bremember\b", r"\bimagine\b", r"\bthink of\b", r"\bpicture\b",
]
PAT = [re.compile(t, re.I) for t in TELLS]


def scan(path: str) -> int:
    n = 0
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("http", "- [R", "- [S", "- [W", "| [S", "| [R")):
            continue
        for p in PAT:
            m = p.search(line)
            if m:
                n += 1
                print(f"{path}:{i}: [{m.group(0)!r}] {line.strip()[:110]}")
    return n


if __name__ == "__main__":
    total = 0
    for f in sys.argv[1:]:
        c = scan(f)
        print(f"== {f}: {c} hits")
        total += c
    sys.exit(1 if total else 0)
