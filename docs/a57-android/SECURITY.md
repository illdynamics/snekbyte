# A57 — Security Review

## Permissions (merged manifest)

- **INTERNET:** removed via `tools:node="remove"` → the APK declares no network
  permission. (The Capacitor template adds it by default; it is unnecessary
  because WebViewAssetLoader serves bundled assets over `https://localhost`.)
- **Dangerous runtime permissions:** none (camera, mic, location, contacts,
  phone, storage are all absent).
- Only remaining entry is the self-generated
  `com.illdynamics.snekbyte.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`
  (auto-added by AndroidX for non-exported dynamic receivers; signature-level,
  not user-facing).

## Content / network

- `allowMixedContent: false`, `usesCleartextTraffic: false`.
- All assets served from the local `https://localhost` origin; no `<access>` /
  Cordova allow-list entries remain.
- No remote JS injection, no analytics, no startup fetches.
- No hardcoded signing secrets or keys in the repo/CI.

## WebView hardening

- Capacitor defaults preserved: `WebViewAssetLoader` (assets only, no
  `file://`), no `setAllowFileAccess`, no `setAllowUniversalAccessFromFileURLs`,
  no `addJavascriptInterface` beyond Capacitor's controlled bridge.
- The only JS↔native surface is the `@capacitor/app` plugin (App lifecycle/Back),
  exposed to the page through Capacitor's normal plugin channel; the Android-only
  `window.SnekByteUI` hook is read-only and contains no privileged calls.
- Service workers are unregistered on Android (offline is provided by the
  bundled asset loader, so no SW trust boundary is introduced).

## Release vs debug

- This deliverable is a **debug-signed** APK for testing. A release build would
  additionally disable WebContents debugging (a debug-build-only convenience),
  keep `minifyEnabled` under review and use an owner-controlled release keystore.
- No release signing identity was created (the uberprompt forbids a
  non-recoverable release identity).

## Backups

- `android:allowBackup="false"` avoids leaking WebView data through cloud backup;
  uninstall still deletes local data (documented, not promised otherwise).
