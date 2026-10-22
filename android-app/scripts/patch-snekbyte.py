#!/usr/bin/env python3
"""Apply the Android-only shell hook to the staged snekbyte.js.

This is a build-time transformation ONLY. The upstream game engine
(reference-pwa/js/snekbyte.js) is never modified. The transform is pinned to
the exact upstream SHA-256 so an unexpected upstream change fails loudly
instead of silently producing a divergent game.
"""
import hashlib
import sys

EXPECTED_SHA256 = "0738b3629f899e7cab067c07e7af13b330404c07a4c520399a559f282e3c217d"

ANCHOR = (
    "  }\n"
    "  if (document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);\n"
)


SW_ANCHOR = (
    "    if ('serviceWorker' in navigator && window.isSecureContext) {\n"
    "      navigator.serviceWorker.register('./sw.js',{scope:'./'}).catch(function(){ /* optional */ });\n"
    "    }\n"
)

SW_REPLACE = (
    "    if ('serviceWorker' in navigator) {\n"
    "      // Android/Capacitor: bundled assets are served by the local\n"
    "      // WebViewAssetLoader, so no service worker is needed. Unregister any\n"
    "      // previously-installed worker (e.g. from an earlier APK) so a stale\n"
    "      // offline cache can never override freshly bundled game assets after an\n"
    "      // app update. The upstream Nuxel PWA (sw.js + registration) is unchanged.\n"
    "      navigator.serviceWorker.getRegistrations().then(function (regs) {\n"
    "        regs.forEach(function (r) { r.unregister(); });\n"
    "      }).catch(function () {});\n"
    "    }\n"
)

INSERT = (
    "  }\n"
    "  // Android shell hook (build-time only; upstream snekbyte.js is unchanged).\n"
    "  window.SnekByteUI = Object.freeze({\n"
    "    requestPause: function () {\n"
    "      if (view.mode === 'playing' && !view.paused) setPause(true);\n"
    "      savePrefs();\n"
    "    },\n"
    "    invalidate: function () { invalidate(); },\n"
    "    isAtRoot: function () { return !view.dialog && view.mode !== 'playing'; },\n"
    "    handleBack: function () { return handleBack(); }\n"
    "  });\n"
    "  if (document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);\n"
)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.stderr.write(
            f"ERROR: upstream snekbyte.js hash mismatch.\n"
            f"  expected {EXPECTED_SHA256}\n"
            f"  actual   {digest}\n"
            f"Refusing to patch an unknown engine version.\n"
        )
        return 1
    text = data.decode("utf-8")
    if text.count(ANCHOR) != 1:
        sys.stderr.write(f"ERROR: anchor not found exactly once ({text.count(ANCHOR)} matches).\n")
        return 1
    if "window.SnekByteUI" in text:
        sys.stderr.write("ERROR: file already contains the shell hook.\n")
        return 1
    text = text.replace(ANCHOR, INSERT, 1)
    if text.count(SW_ANCHOR) != 1:
        sys.stderr.write(f"ERROR: service-worker anchor not found exactly once ({text.count(SW_ANCHOR)} matches).\n")
        return 1
    text = text.replace(SW_ANCHOR, SW_REPLACE, 1)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
