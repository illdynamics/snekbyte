# A57 — Android Test Evidence

**Test device:** Android **emulator** (no physical phone was attached).
`model: sdk_gphone64_arm64`, Android **15 (API 35)**, System WebView 124.0.6367.219.

> **Physical-device acceptance: UNVERIFIED.** The uberprompt requires a real
> Android phone for hardware-acceptance PASS; this run used the emulator and is
> labelled accordingly.

Evidence files: `docs/a57-android/evidence/` (screenshots, `dumpsys package`,
`aapt badging`, filtered logcat).

## Environment setup

- Airplane mode enabled before first launch:
  `settings put global airplane_mode_on 1` + `svc wifi disable` + `svc data disable`.
- Confirmed offline: `ping 8.8.8.8` → `connect: Network is unreachable`.
- Clean install: `adb uninstall` then `adb install dist/android/snekbyte-debug.apk`.

## Results

| Gate | Result | Evidence |
|---|---|---|
| Clean install | PASS | `adb install` → `Success`; `dumpsys package` shows `firstInstallTime` |
| Offline first launch (airplane mode ON) | PASS | cold launch `TotalTime: 907-1060ms`; every asset served from `https://localhost`; no remote fetches in logcat |
| Launcher app + title | PASS | `application-label:'SnekByte'`, launchable `MainActivity` |
| Correct launcher icon (snake + poop art) | PASS | regenerated from canonical `01-02_snekbyte.png`; histogram of screenshot shows SnekByte palette |
| Touch / swipe steering | PASS | `adb input swipe` on canvas produced `SnekEngine.turn` calls (down/up/left/right) |
| D-pad taps | PASS | `adb input tap` on D-pad buttons produced turn calls |
| Keyboard (Enter starts game) | PASS | `keyevent 66` started a game |
| Back key pause/menu | PASS | Back on active game → `PAUSED`; on game-over → main menu |
| Background auto-pause | PASS | Home → native `pause` event → `SnekByteUI.requestPause()` → `PAUSED` even though `visibilityState` stayed `visible` |
| WoNQ Poop-o-meter (5 foods) | PASS | on-device engine run: `score=5, poopCount=1`, meter `0,1,2,3,4 → 0`, poop at tail |
| Poop collision | PASS | `cause="poop"` when head reaches poop cell |
| Wall collision | PASS | `cause="wall"` |
| Preferences persist | PASS | speed/WoNQ/grid survive reload and Home→process-kill→relaunch |
| High score key persists | PASS | `highScore` field in same localStorage key (best-score display reads it) |
| Zero permissions / no INTERNET | PASS | `dumpsys package` → only `DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`; no runtime permissions |
| No crash / no JS exceptions | PASS | logcat clean; settings panel opens with no errors after fix |

## Screenshots

- `screenshot-menu-offline.png` — main menu rendered offline.
- `screenshot-gameplay-offline.png` — active gameplay (snake + board) offline.

## Notes / limits

- Service worker: the Android build unregisters it (bundled assets are served by
  WebViewAssetLoader), which also fixes a stale-cache-after-update bug observed
  during testing.
- Abrupt `am force-stop` without prior backgrounding can lose the most recent
  few seconds of WebView localStorage writes (a general WebView limitation);
  normal Home/background/reload persistence is confirmed.
