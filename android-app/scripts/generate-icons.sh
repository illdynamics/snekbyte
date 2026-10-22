#!/usr/bin/env bash
# Regenerate Android launcher icons + splash screens from the canonical
# SnekByte pixel-art icon (reference-pwa/icons/icon-512.png).
#
# The generated PNGs are committed to android-app/android so a plain
# `./gradlew assembleDebug` needs no ImageMagick. Re-run this only when the
# upstream art changes, then commit the outputs.
#
# bash 3.2 (macOS default) compatible: no associative arrays.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/reference-pwa/nuxel-dropin/pwa/nuxel-apps/snekbyte/icons/icon-512.png"
RES="$ROOT/android-app/android/app/src/main/res"

command -v magick >/dev/null 2>&1 || { echo "ERROR: ImageMagick 'magick' not found" >&2; exit 1; }
[ -f "$SRC" ] || { echo "ERROR: source icon $SRC not found" >&2; exit 1; }

BG="#06121c"
LIME="#a0ff51"
CYAN="#29d8f4"

FONT=""
for f in "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
         "/System/Library/Fonts/Supplemental/Arial.ttf" \
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; do
  if [ -f "$f" ]; then FONT="$f"; break; fi
done

# --- 1. Legacy square launcher icons (pre-Android 8), full-bleed dark bg ---
legacy_icon() {
  local d="$1" px="$2" art
  art=$(( px * 70 / 100 ))
  magick "$SRC" -fuzz 2% -trim +repage -resize "${art}x${art}" \
    -background "$BG" -gravity center -extent "${px}x${px}" -strip \
    "PNG32:$RES/mipmap-$d/ic_launcher.png"
  cp "$RES/mipmap-$d/ic_launcher.png" "$RES/mipmap-$d/ic_launcher_round.png"
}
legacy_icon mdpi 48
legacy_icon hdpi 72
legacy_icon xhdpi 96
legacy_icon xxhdpi 144
legacy_icon xxxhdpi 192

# --- 2. Adaptive icon foregrounds (Android 8+), transparent, safe-zone art ---
fg_icon() {
  local d="$1" px="$2" safe
  safe=$(( px * 61 / 100 ))   # adaptive-icon safe zone ~= 66/108
  magick "$SRC" -fuzz 2% -trim +repage -resize "${safe}x${safe}" \
    -background none -gravity center -extent "${px}x${px}" -strip \
    "PNG32:$RES/mipmap-$d/ic_launcher_foreground.png"
}
fg_icon mdpi 108
fg_icon hdpi 162
fg_icon xhdpi 216
fg_icon xxhdpi 324
fg_icon xxxhdpi 432

# --- 3. Adaptive icon background colour (single source of truth) ---
cat > "$RES/values/ic_launcher_background.xml" <<XML
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">$BG</color>
</resources>
XML

cat > "$RES/drawable/ic_launcher_background.xml" <<XML
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <solid android:color="$BG" />
</shape>
XML

echo "Android launcher icons regenerated from $SRC"
