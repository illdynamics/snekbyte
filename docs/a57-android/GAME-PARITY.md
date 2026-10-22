# A57 — Game Parity

## Rule provenance

`js/snek-engine.js` is the deterministic port of the Python entry path
(`main.py → src/main.py → src/game_loop.run_game()`) and is **unchanged** in this
operation. The `UPSTREAM-PROVENANCE.md` record documents every ported rule:

- snake resets length 1 at (20,15) heading RIGHT;
- a length>1 snake may not reverse;
- eat → `length += 1`, `score += 1`, new food on a free cell;
- WoNQ ON: every **fifth** actual food drops a persistent poop at the tail cell
  and resets the counter;
- game-over precedence wall → self → poop.

## Verification re-run after this operation

```bash
node reference-pwa/nuxel-dropin/pwa/nuxel-apps/snekbyte/tests/test-snek-engine.js
python3 .scratch-snakepwn6000/extracted/snekbyte-main/scripts/check-snekbyte-bundle.py
node --check reference-pwa/nuxel-dropin/pwa/nuxel-apps/snekbyte/js/snekbyte.js
```

Result: **48 passed, 0 failed**, including the 41-tick replay of
`fixtures/parity.json` (recorded from the real upstream Python game) with
`0 divergence(s)` over wall/self/poop endings. The bundle/integrity check also
passes (`PASS SnekByte PWA package/icon paths and core integration contract`).

## On-device engine checks (Android 15 emulator, via WebView DevTools)

- Deterministic 5-food run: `score=5`, `snake.length=6`, `poopCount=1`,
  meter readings `0,1,2,3,4 → 0` on the 5th food, poop position `[21,15]`
  == tail cell. ✅
- Poop collision: `gameOver=true, cause="poop"`, head `[21,15]` == poop. ✅
- Wall collision: `gameOver=true, cause="wall"`. ✅
- Self collision covered by the upstream 41-tick parity replay. ✅

## Isolated UI bug fix (single line)

The A56 PWA's settings dialog referenced an undefined variable
(`activeWonq`) outside its scope, so opening **Settings** threw
`ReferenceError: activeWonq is not defined` and failed to restore the
WoNQ/grid toggles (the speed preference was unaffected).

```diff
- $('wonq-setting').checked = !!activeWonq;
+ $('wonq-setting').checked = !!view.settings.wonqMode;
```

This is a clearly isolated bug fix (the uberprompt permits "a clearly isolated
bug fix"). It changes the phone shell only; the canonical engine defaults and
the Python parity fixtures are untouched and still pass. Verified on-device:
after the fix, opening Settings produces **no exception** and correctly restores
speed (`Fastest · 20 ticks/s`), WoNQ (`false`) and grid (`false`) from
`localStorage`.

## WoNQ default

- Engine canonical default: `OFF` (unchanged, `CONFIG.defaultWonqMode = false`).
- Nuxel/Android phone shell default: `ON` (set in `snekbyte.js` at startup so
  the Poop-o-meter is visible immediately) — preserved.
