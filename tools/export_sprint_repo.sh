#!/usr/bin/env bash
# Stage the Apart sprint submission into its own repository (sammatuba/collude-or-agree) and push.
# Keeps the same folder layout as this repository, so every path in the paper stays valid.
# Usage: bash tools/export_sprint_repo.sh <staging-dir> [commit message]
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"; DST="$1"; MSG="${2:-Update sprint submission}"
mkdir -p "$DST"
if [ ! -d "$DST/.git" ]; then git -C "$DST" init -q -b main; git -C "$DST" remote add origin git@github.com:sammatuba/collude-or-agree.git; fi
rsync -a --delete --exclude '.venv' --exclude 'data/runs' --exclude 'data/cache' --exclude '.env' --exclude '.env.*' --exclude '__pycache__' --exclude '.pytest_cache' "$SRC/lab/" "$DST/lab/"
mkdir -p "$DST/tools" "$DST/literature" "$DST/projects"
for f in md2docx.js md2apart.py stecheck.py tells.py export_sprint_repo.sh; do [ -f "$SRC/tools/$f" ] && cp "$SRC/tools/$f" "$DST/tools/"; done
rsync -a --delete --exclude '~$*' --exclude '* - Copy.*' --exclude '*:Zone.Identifier' "$SRC/projects/2026-10-apart-collusion-sprint/" "$DST/projects/2026-10-apart-collusion-sprint/"
cp "$SRC/GLOSSARY.md" "$DST/GLOSSARY.md"; cp "$SRC/literature/INDEX.md" "$DST/literature/INDEX.md"
cp "$SRC/lab/.env.example" "$DST/lab/.env.example"
cp "$SRC/tools/sprint-repo-README.md" "$DST/README.md"
cat > "$DST/.gitignore" <<'G'
lab/.env
lab/.env.*
!lab/.env.example
lab/.venv/
lab/data/runs/
lab/data/cache/
__pycache__/
.pytest_cache/
~$*
* - Copy.*
*:Zone.Identifier
G
git -C "$DST" add -A
git -C "$DST" -c user.name="sammatuba" commit -q -m "$MSG" || echo "nothing to commit"
git -C "$DST" push -q -u origin main
echo "pushed to sammatuba/collude-or-agree"
