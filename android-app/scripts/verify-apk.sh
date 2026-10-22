#!/usr/bin/env bash
# Verify dist/android/snekbyte-debug.apk is a real, signed, installable APK with
# the intended identity, label, permissions and bundled offline game assets.
#
#   bash android-app/scripts/verify-apk.sh [path-to-apk]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APK="${1:-$ROOT/dist/android/snekbyte-debug.apk}"

find_sdk() {
  if [ -n "${ANDROID_SDK_ROOT:-}" ] && [ -d "$ANDROID_SDK_ROOT/build-tools" ]; then
    echo "$ANDROID_SDK_ROOT"; return 0
  fi
  if [ -n "${ANDROID_HOME:-}" ] && [ -d "$ANDROID_HOME/build-tools" ]; then
    echo "$ANDROID_HOME"; return 0
  fi
  for cand in "$ROOT/.scratch-snakepwn6000/toolchain/sdk" "$HOME/Library/Android/sdk"; do
    if [ -d "$cand/build-tools" ]; then echo "$cand"; return 0; fi
  done
  return 1
}

SDK="$(find_sdk)" || { echo "ERROR: Android SDK build-tools not found" >&2; exit 1; }
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
APKSIGNER="$BT/apksigner"
AAPT2="$BT/aapt2"

command -v unzip >/dev/null 2>&1 || { echo "ERROR: unzip not found" >&2; exit 1; }

fail=0
check() { if [ "$1" = "0" ]; then echo "PASS: $2"; else echo "FAIL: $2"; fail=1; fi; }

[ -f "$APK" ] && [ -s "$APK" ]; check $? "APK exists and is non-empty ($(stat -f%z "$APK" 2>/dev/null || stat -c%s "$APK") bytes)"

# Signature
"$APKSIGNER" verify "$APK" >/dev/null 2>&1; check $? "apksigner verify (debug-signed)"

# Identity / metadata
BADGING="$("$AAPT2" dump badging "$APK" 2>/dev/null)"
echo "$BADGING" | grep -q "package: name='com.illdynamics.snekbyte'"; check $? "package id = com.illdynamics.snekbyte"
echo "$BADGING" | grep -q "application-label:'SnekByte'"; check $? "app label = SnekByte"
echo "$BADGING" | grep -q "launchable-activity: name='com.illdynamics.snekbyte.MainActivity'"; check $? "launchable activity present"
echo "$BADGING" | grep -q "minSdkVersion:'23'"; check $? "minSdkVersion = 23"
echo "$BADGING" | grep -q "targetSdkVersion:'35'"; check $? "targetSdkVersion = 35"

# Permissions: must NOT request INTERNET or any dangerous runtime permission.
PERMS="$("$AAPT2" dump permissions "$APK" 2>/dev/null)"
if echo "$PERMS" | grep -q "android.permission.INTERNET"; then
  check 1 "no INTERNET permission (fully offline bundle)"
else
  check 0 "no INTERNET permission (fully offline bundle)"
fi
if echo "$PERMS" | grep -qE 'CAMERA|RECORD_AUDIO|ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION|READ_CONTACTS|READ_PHONE_STATE|READ_EXTERNAL_STORAGE|WRITE_EXTERNAL_STORAGE'; then
  check 1 "no dangerous runtime permissions"
else
  check 0 "no dangerous runtime permissions"
fi

# Bundled assets: the game must live inside the APK, never fetched at runtime.
LISTING="$(unzip -l "$APK")"
for asset in \
  assets/public/index.html \
  assets/public/css/snekbyte.css \
  assets/public/js/snek-engine.js \
  assets/public/js/snekbyte.js \
  assets/public/js/android-shell.js \
  assets/public/icons/icon-512.png \
  assets/public/icons/icon-192.png \
  assets/public/manifest.json; do
  echo "$LISTING" | grep -q "$asset"; check $? "bundled asset: $asset"
done

# SHA-256 manifest (only when verifying the default dist artifact).
if [ "$APK" = "$ROOT/dist/android/snekbyte-debug.apk" ] && [ -f "$APK.sha256" ]; then
  EXPECTED="$(awk '{print $1}' "$APK.sha256")"
  ACTUAL="$(shasum -a 256 "$APK" | awk '{print $1}')"
  [ "$EXPECTED" = "$ACTUAL" ]; check $? "SHA-256 matches dist manifest"
fi

echo ""
if [ "$fail" = "0" ]; then
  echo "VERIFY: PASS"
else
  echo "VERIFY: FAIL"
  exit 1
fi
