# A57 — APK Contents

The APK contains the **complete game**; nothing is fetched at runtime.

```
assets/public/index.html
assets/public/css/snekbyte.css
assets/public/js/snek-engine.js      (verbatim upstream parity engine)
assets/public/js/snekbyte.js         (upstream + pinned Android hook + SW unregister)
assets/public/js/android-shell.js    (Android-only Capacitor bridge)
assets/public/icons/icon-{48,72,96,128,144,152,192,384,512}.png
assets/public/icons/icon.svg
assets/public/manifest.json
assets/public/app.json
assets/public/sw.js                  (present for upstream integrity; unused on Android)
assets/public/cordova.js             (empty Capacitor stub)
assets/public/cordova_plugins.js     (empty Capacitor stub)
assets/capacitor.config.json
assets/capacitor.plugins.json
+ compiled classes.dex, resources.arsc, res/mipmap-* launcher icons,
  AndroidManifest.xml (merged)
```

Verification command:

```bash
unzip -l dist/android/snekbyte-debug.apk | grep -E 'assets/public'
```

Launcher icons are the canonical pixel-art snake + poop, regenerated as both
legacy square icons and adaptive-foreground PNGs (safe-zone scaled), with a dark
`#06121c` background.
