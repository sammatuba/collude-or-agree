"""Rough ASD-STE100 checks on a Markdown file: sentences over N words (prose, list items,
table cells), paragraphs over 6 sentences. Skips frontmatter, code blocks, references, URLs."""
import re, sys
path, limit = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 25
text = open(path, encoding="utf-8").read()
text = re.sub(r"^---.*?---\n", "", text, flags=re.S)
text = re.sub(r"```.*?```", "", text, flags=re.S)
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
text = text.split("## References")[0] + ("\n## Appendix" + text.split("## Appendix", 1)[1] if "## Appendix" in text else "")
long_, paras = [], []
for line in text.splitlines():
    s = line.strip()
    if not s or s.startswith("#") or set(s) <= set("|-: "):
        continue
    chunks = [c for c in s.strip("|").split("|")] if s.startswith("|") else [s]
    for c in chunks:
        c = re.sub(r"https?://\S+", "URL", c)
        c = re.sub(r"^[-*\d.]+\s+", "", c.strip())
        c = c.replace("**", "").replace("`", "")
        sents = re.split(r"(?<=[.?!:])\s+(?=[A-Z\[\"(])", c)
        if not s.startswith("|") and not s.startswith("-") and len(sents) > 6:
            paras.append((len(sents), c[:70]))
        for x in sents:
            n = len(x.split())
            if n > limit:
                long_.append((n, x))
print(f"{path}: {len(long_)} sentences over {limit} words; {len(paras)} paragraphs over 6 sentences")
for n, x in long_:
    print(f"  [{n}] {x}")
for n, x in paras:
    print(f"  PARA[{n}] {x}...")
