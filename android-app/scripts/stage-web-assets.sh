#!/usr/bin/env bash
# Deterministically stage the Nuxel SnekByte PWA into android-app/www for bundling.
#
# The game engine is NOT copied into the Android project in a modified form:
#   - reference-pwa/ is the verbatim upstream game source (source of truth)
#   - www/js/snekbyte.js gets ONE pinned, additive Android hook via
#     scripts/patch-snekbyte.py (fails on any hash mismatch)
#   - www/js/android-shell.js and the one <script> tag in index.html are the
#     only Android-specific additions.
#
# The result is a fully offline set of local assets; no remote URLs are added.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP="$ROOT/android-app"
REF="$ROOT/reference-pwa/nuxel-dropin/pwa/nuxel-apps/snekbyte"
WWW="$APP/www"

if [ ! -f "$REF/index.html" ]; then
  echo "ERROR: reference-pwa/index.html not found at $REF" >&2
  exit 1
fi

# Clean and rebuild www so stale files can never linger in a build.
rm -rf "$WWW"
mkdir -p "$WWW"

# 1. Copy the upstream web assets verbatim (game engine source of truth).
cp -R "$REF/." "$WWW/"
# The reference tree also contains dev-only parity tooling/tests; drop those
# from the device bundle (they are never loaded at runtime).
rm -rf "$WWW/tests" "$WWW/tools" "$WWW/icon-pack" "$WWW/UPSTREAM-PROVENANCE.md"

# 2. Apply the pinned Android-only hook to the game UI layer.
python3 "$APP/scripts/patch-snekbyte.py" "$REF/js/snekbyte.js" "$WWW/js/snekbyte.js"

# 3. Stage the Capacitor shell bridge and reference it from index.html.
cp "$APP/scripts/android-shell.js" "$WWW/js/android-shell.js"
python3 - "$WWW/index.html" <<'PYEOF'
import sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    html = f.read()
TAG = '<script src="js/android-shell.js"></script>'
if 'android-shell.js' in html:
    print("index.html already references android-shell.js")
else:
    if html.count('</body>') != 1:
        sys.stderr.write("ERROR: expected exactly one </body> in index.html\n")
        sys.exit(1)
    html = html.replace('</body>', '  ' + TAG + '\n</body>', 1)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("injected android-shell.js script tag")
PYEOF

# 4. Safety audit: the bundled app must not depend on any remote host.
if grep -rEn 'https?://' "$WWW" --include='*.html' --include='*.js' --include='*.css' | grep -vE 'schemas\.googleapis|www\.w3\.org|serviceworker|androidScheme' ; then
  echo "ERROR: remote URL found in staged web assets (see above)." >&2
  exit 1
fi

# 5. Syntax-check the staged JavaScript.
node --check "$WWW/js/snek-engine.js"
node --check "$WWW/js/snekbyte.js"
node --check "$WWW/js/android-shell.js"

echo "Staged web assets:"
find "$WWW" -type f | sed "s#$WWW/##" | sort
