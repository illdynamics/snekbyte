# A57 — Source Audit

## What is preserved (unchanged)

- Root Python project: `main.py`, `snekbyte.py`, `requirements.txt`, `src/**`,
  `tests/**` — byte-identical to the A56 drop-in archive
  (`diff -rq src .scratch-snakepwn6000/extracted/snekbyte-main/src` → no output).
- Nuxel PWA app metadata: `app.json` (`org.nuxel.SnekByte`), `manifest.json`,
  `sw.js` — verbatim except the single isolated UI fix documented in
  GAME-PARITY.md.
- Nuxel icon pack: `nuxel-applications-icon-pack/01-02_snekbyte.png`
  (SHA-256 `91199487…`, 128×128 pixel-art snake + poop) — verbatim.
- Parity fixture + tooling under `nuxel-dropin/tools/s10plus/a33/snekbyte/`.

## What is added (new, scoped to Android packaging)

| Path | Purpose |
|---|---|
| `android-app/` | Capacitor wrapper project (package.json, capacitor.config.ts, scripts) |
| `android-app/www/` | generated staging output (gitignored; rebuilt by `npm run stage`) |
| `android-app/android/` | generated Capacitor Android Gradle project (committed, with native customizations) |
| `reference-pwa/` | verbatim PWA + parity tooling as the single game source of truth |
| `docs/a57-android/` | this documentation set |
| `.github/workflows/android-build.yml` | CI that builds and uploads the debug APK |

## What is transformed at build time only (upstream never modified)

`android-app/scripts/patch-snekbyte.py` is pinned to the exact upstream SHA-256
and applies two additive changes to a **copy** staged into `www/`:

1. Adds `window.SnekByteUI` (a frozen, read-only `requestPause` / `invalidate` /
   `handleBack` / `isAtRoot` bridge) so the native shell can pause on
   background and route the Back key.
2. Replaces the service-worker registration with an explicit
   `navigator.serviceWorker.getRegistrations().then(unregister)` so a stale
   offline cache can never override freshly bundled assets after an APK update.

The original `reference-pwa/.../js/snekbyte.js` and `sw.js` are untouched.

## Android native customizations (committed under android-app/android)

- `MainActivity.java`: edge-to-edge + transparent system bars + light system-bar
  icons; keeps Capacitor's secure `WebViewAssetLoader` defaults.
- `AndroidManifest.xml`: `tools:node="remove"` drops the template's INTERNET
  permission → **zero network permission**; `usesCleartextTraffic=false`;
  `allowBackup=false`.
- `styles.xml` / `colors.xml`: dark theme + modern `Theme.SplashScreen` using the
  snake/poop artwork as the splash icon (no blocking legacy splash bitmaps).
- `mipmap-*`: launcher icons regenerated from the canonical snake/poop art
  (legacy square + adaptive-foreground at mdpi…xxxhdpi).

## No fabrication

- No empty APK, no placeholder assets, no remote WebView, no hardcoded keys.
- Every "PASS" in ANDROID-TESTS.md maps to a real command/log/device readback
  (evidence in `docs/a57-android/evidence/`).
