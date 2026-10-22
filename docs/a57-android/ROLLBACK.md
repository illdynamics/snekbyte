# A57 — Rollback

The Android packaging is fully additive and scoped. To return to the pre-A57
state:

## Remove the Android packaging

```bash
git rm -r android-app reference-pwa docs/a57-android .github/workflows/android-build.yml
# or, if not yet committed, simply delete those directories
```

The root Python project and the Nuxel/Fedora PWA are **not** touched, so no
rollback is needed for them. The only change inside the PWA is the one-line
`activeWonq` fix in `reference-pwa/.../js/snekbyte.js`; revert it with:

```diff
- $('wonq-setting').checked = !!view.settings.wonqMode;
+ $('wonq-setting').checked = !!activeWonq;
```

(and restore the pre-fix SHA-256 `7f6b104c…` in
`android-app/scripts/patch-snekbyte.py` if the Android patch is also being kept).

## Remove local build artifacts (not committed)

- `dist/android/` (gitignored)
- `.scratch-snakepwn6000/` (gitignored toolchain: Android SDK + JDK 21)
- `~/.gradle`, `~/.android/avd/snekbyte_test.avd` (host caches, outside the repo)

## Remove the installed app

```bash
adb uninstall com.illdynamics.snekbyte
```

## No Nuxel system changes

This operation did **not** modify the Nuxel phone kernel, Fedora OS, boot
images, camera, modem, display drivers or update pipeline. Android SDK packages
were installed only on the development host (macOS), never on the Nuxel S10+.
