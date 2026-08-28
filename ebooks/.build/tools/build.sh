#!/usr/bin/env bash
# Assemble the ebook HTML from fragments.
#   preview.html  (ebooks/.build/preview.html) — dev copy, references assets/mermaid.min.js
#   prt-converge.html (ebooks/prt-converge.html) — final, self-contained (mermaid inlined)
set -euo pipefail
cd "$(dirname "$0")/.."           # ebooks/.build
ROOT="$(pwd)"

FRAGMENTS=(src/front.html src/act-1.html src/act-2.html src/act-3.html src/act-4.html src/act-5.html src/act-6.html src/act-7.html src/back.html)

TAG="${BUILD_TAG:-}"
out_preview="$ROOT/preview${TAG:+-$TAG}.html"
out_final="$ROOT/../prt-converge.html"

cat src/head.html > "$out_preview"
for f in "${FRAGMENTS[@]}"; do
  if [ -f "$f" ]; then cat "$f" >> "$out_preview"; else echo "build.sh: skipping missing $f" >&2; fi
done
cat src/tail.html >> "$out_preview"

if [ -n "$TAG" ]; then
  echo "build.sh: assembled $(grep -c '<section class="slide"' "$out_preview" || true) slides -> $(basename "$out_preview") (tagged build; final artifact untouched)"
  exit 0
fi

# Final: inline mermaid.min.js and the converge icon so the artifact is self-contained.
MMD="$ROOT/assets/mermaid.min.js"
ICON="$ROOT/assets/converge-icon.svg"
python3 - "$out_preview" "$MMD" "$ICON" "$out_final" <<'PY'
import base64, sys
src, mmd, icon, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
html = open(src, encoding="utf-8").read()
tag = '<script src="assets/mermaid.min.js"></script>'
inlined = "<script>\n" + open(mmd, encoding="utf-8").read() + "\n</script>"
assert tag in html, "mermaid script tag not found in preview.html"
html = html.replace(tag, inlined)
uri = "data:image/svg+xml;base64," + base64.b64encode(open(icon, "rb").read()).decode()
html = html.replace("assets/converge-icon.svg", uri)
open(out, "w", encoding="utf-8").write(html)
PY

slides=$(grep -c '<section class="slide"' "$out_preview" || true)
echo "build.sh: assembled $slides slides -> preview.html + ../prt-converge.html"
