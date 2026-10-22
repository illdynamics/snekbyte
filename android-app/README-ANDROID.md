# SnekByte for Android (Capacitor)

A **genuinely installable, offline Android APK** built from the completed Nuxel
SnekByte HTML/CSS/JavaScript game (the Python/Pygame parity port), wrapped in a
**version-pinned Capacitor Android** shell. No Python runtime, no remote WebView,
no network dependency.

- **Android application ID:** `com.illdynamics.snekbyte`
- **Display name:** `SnekByte`
- **Package contents:** the bundled PWA game (`index.html`, `css/`, `js/`, `icons/`)
  served from Capacitor's secure local `WebViewAssetLoader` (`https://localhost`).
- **APK output:** `../dist/android/snekbyte-debug.apk`

---

## 1. Prerequisites

| Tool | Required | Verified version |
|---|---|---|
| Node.js + npm | yes | v20.20.2 / 10.8.2 |
| JDK | 21 (Capacitor 7 / AGP 8.7 compile Java 21) | Temurin 21.0.13 |
| Android SDK | `platforms;android-35`, `build-tools;35.0.0`, `platform-tools` | API 35 |
| ImageMagick (`magick`) | optional (committed icons are used otherwise) | any |

The build script auto-detects JDK 21 and the SDK. To install the SDK on macOS:

```bash
brew install --cask temurin@21
mkdir -p ~/Android/sdk/cmdline-tools && cd ~/Android/sdk/cmdline-tools
curl -LO https://dl.google.com/android/repository/commandlinetools-mac-13114758_latest.zip
unzip -q commandlinetools-mac-13114758_latest.zip && mv cmdline-tools latest
export ANDROID_HOME=~/Android/sdk
yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_HOME" \
  "platform-tools" "platforms;android-35" "build-tools;35.0.0"
```

---

## 2. Build (one command)

```bash
bash android-app/scripts/build-debug.sh
```

This is idempotent and reproducible (consecutive runs produce a byte-identical
APK). It:

1. runs `npm ci` with the pinned `package-lock.json`,
2. stages the verbatim upstream PWA web assets into `www/` and applies **one**
   pinned, additive Android hook (`scripts/patch-snekbyte.py`) — the upstream
   game engine is never modified,
3. regenerates the Android launcher icons from the canonical snake/poop art,
4. runs `npx cap sync android`,
5. hardens the regenerated Cordova `config.xml` (removes `<access origin="*">`),
6. runs `./gradlew --no-daemon :app:assembleDebug`,
7. copies the signed APK to `dist/android/` with a SHA-256 manifest.

Verify the artifact:

```bash
bash android-app/scripts/verify-apk.sh
```

Every successful `main` build is also published as a GitHub Release. The
installable release asset is the verified APK itself, named `SnekByte.apk`,
with a matching `SnekByte.apk.sha256` checksum.

---

## 3. Install / update / uninstall

```bash
# Install (or update over the same signed debug package; local data is kept)
adb install -r dist/android/snekbyte-debug.apk

# Launch
adb shell am start -n com.illdynamics.snekbyte/.MainActivity

# Uninstall (this deletes WebView localStorage: high score + preferences)
adb uninstall com.illdynamics.snekbyte
```

The app requests **zero dangerous permissions** and has **no INTERNET
permission**. It plays fully offline.

---

## 4. Offline first launch (airplane mode)

1. Uninstall any previous build, install the APK.
2. Enable airplane mode **before** the first launch.
3. Launch. The main menu, all icons, the D-pad, settings and the Poop-o-meter
   render entirely from bundled assets; logcat shows every request served from
   `https://localhost` (the local WebViewAssetLoader) and no external fetches.

---

## 5. Signing

- **Debug APK** is signed with the standard Android debug keystore
  (`CN=Android Debug, O=Android, C=US`) — suitable for sideloading/testing only.
- **No signing secret is stored in the repo or CI.** To produce a release APK
  later, create your own keystore once and keep it private:

```bash
keytool -genkey -v -keystore ~/snekbyte-release.jks -keyalg RSA -keysize 2048 \
  -validity 10000 -alias snekbyte
# then configure signingConfig in android-app/android/app/build.gradle (never commit the .jks)
```

Do **not** create a throwaway release identity you cannot recover for updates.

---

## 6. Android-specific behaviour

- **Back key:** game-first. Closes a dialog, pauses an active game, or returns to
  the menu; at the root menu it performs the normal "move task to back".
- **Backgrounding:** the native `pause` event pauses the game immediately (even
  though the Capacitor WebView keeps `document.visibilityState === "visible"`).
- **Persistence:** speed, WoNQ toggle, grid visibility and best score live in
  WebView `localStorage` and survive activity recreation, rotation, app relaunch,
  phone reboot and **update** of the same signed package. Uninstall deletes them.
- **Service workers:** bundled assets are served by WebViewAssetLoader, so the
  Android build intentionally unregisters any service worker to guarantee a
  fresh APK's assets are always used after an update.
- **Edge-to-edge:** `viewport-fit=cover` + `env(safe-area-inset-*)` keep the
  D-pad, settings sheet and Poop-o-meter clear of system bars and gesture-nav.
