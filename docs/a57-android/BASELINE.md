# A57 — SnekByte Android APK — Clean Baseline

## Source archive

| Field | Value |
|---|---|
| Archive | `~/Downloads/snekbyte-main-SNAKEPWN-5000-dropin.zip` |
| Archive size | 215,577 bytes |
| Archive SHA-256 | `606ba46d87ad26d15beb94b92f8d060974526a9727fe0d407f339ec0619f9a1b` |
| Extracted into | `.scratch-snakepwn6000/extracted/snekbyte-main/` (scratch, gitignored) |
| PWA source of truth (committed) | `reference-pwa/nuxel-dropin/pwa/nuxel-apps/snekbyte/` |
| Parity tooling (committed) | `reference-pwa/nuxel-dropin/tools/s10plus/a33/snekbyte/` |

> The exact byte hash of the drop-in archive was recorded on the build host. The
> committed `reference-pwa/` tree is the verbatim PWA + provenance/parity tools
> extracted from that archive, so the archive itself does not need to be
> re-committed.

## Repository state

| Field | Value |
|---|---|
| Branch | `main` |
| Base commit | `84430528bf0b6c9d0810975e117a3fc9e298ce08` ("refactor: remove redundant directories and update project name") |
| Remote | `https://github.com/illdynamics/snekbyte.git` |
| Existing Android project | none (first Android packaging) |
| Python source changed? | **No** — `src/`, `main.py`, `snekbyte.py`, `requirements.txt` are byte-identical to the archive |
| Nuxel PWA changed? | **Only one isolated bug fix** (see GAME-PARITY.md), otherwise verbatim |

## Game engine version

- Engine: `js/snek-engine.js` — deterministic Python/Pygame parity port.
- Upstream SHA-256 of `snek-engine.js`: `f1028ceff2ff923e85b1679c458640b0e4d677388d2b0ee761666efd4a3d7c3e` (unchanged in this operation).
- Upstream SHA-256 of `js/snekbyte.js` before the one-line fix:
  `7f6b104cfa97d6dac266fa3400a8ca5659faac8cf21f6f31edf1a3efecb22943`.
- Upstream SHA-256 of `js/snekbyte.js` after the one-line fix:
  `0738b3629f899e7cab067c07e7af13b330404c07a4c520399a559f282e3c217d`.

## Toolchain (development host = macOS arm64)

| Component | Version |
|---|---|
| Node.js | v20.20.2 |
| npm | 10.8.2 |
| JDK | Temurin 21.0.13 (build toolchain; system default is 17, detected and overridden by the build script) |
| Android SDK | platforms;android-35, build-tools;35.0.0, platform-tools 37.0.1 |
| Capacitor | core/cli/android 7.6.9 (+ @capacitor/app 7.1.2) |
| Android Gradle Plugin | 8.7.2 |
| Gradle | 8.11.1 (wrapper, `-all` distribution) |
| Android target/min | targetSdk 35, compileSdk 35, minSdk 23 |

Capacitor **8** was intentionally not used because it requires Node >= 22;
this host runs Node 20. Capacitor **7.6.9** is the pinned, mutually-compatible
release for Node 20 + AGP 8.7 + Gradle 8.11 + JDK 21.

## Known incompatibilities addressed

1. Capacitor 8 → Node 22 requirement → pinned Capacitor 7.
2. Capacitor 7.6.9 template compiles Java 21 → build script pins JDK 21.
3. macOS default `/bin/bash` is 3.2 (no associative arrays) → build scripts are
   bash-3.2 compatible.
4. ImageMagick embeds a `tIME` chunk in generated PNGs (breaks reproducible
   builds) → `-strip` is applied.
