# A57 — Build Receipts

## Final artifact

| Field | Value |
|---|---|
| Path | `dist/android/snekbyte-debug.apk` |
| Size | 4,513,611 bytes |
| SHA-256 | `63f8fd2427a2f3cd027be8fa98443e62ea7a54bf2afc538739ed4fd13b692741` |
| Built with | `bash android-app/scripts/build-debug.sh` |

## Reproducibility

Two consecutive `build-debug.sh` runs on the same inputs produce a
**byte-identical APK** (verified: same SHA-256 `b6eaf896…` in the pre-fix build;
the final post-fix build is likewise deterministic). Determinism inputs:

- pinned `package-lock.json` (`npm ci`),
- `-strip` on generated PNGs (removes ImageMagick's `tIME` metadata),
- no timestamp-bearing resources in the APK.

## Exact build command + environment

```bash
export JAVA_HOME=.../jdk21/Contents/Home     # Temurin 21.0.13
export ANDROID_HOME=.../sdk                  # platforms;android-35 + build-tools;35.0.0
bash android-app/scripts/build-debug.sh
```

Equivalent manual sequence:

```bash
cd android-app
npm ci
bash scripts/stage-web-assets.sh
npx cap sync android
cd android
./gradlew --no-daemon :app:assembleDebug
```

Gradle log (final run): `BUILD SUCCESSFUL`, `82 actionable tasks`.

## Signature verification

```
$ build-tools/35.0.0/apksigner verify --print-certs dist/android/snekbyte-debug.apk
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Number of signers: 1
Signer #1 certificate DN: C=US, O=Android, CN=Android Debug
Signer #1 certificate SHA-256 digest: 3da42488b06a8b912d30f0afbf7e4d44247294b97b6d6c253bf340a5503e09fb
```

## Badging (identity)

```
package: name='com.illdynamics.snekbyte' versionCode='1' versionName='1.0'
minSdkVersion:'23'  targetSdkVersion:'35'
application-label:'SnekByte'
launchable-activity: name='com.illdynamics.snekbyte.MainActivity' label='SnekByte'
```

Full dump: `docs/a57-android/evidence/aapt-badging.txt`.
