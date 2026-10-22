/* SnekByte Android shell bridge.
 *
 * This file is staged into www/ ONLY by the Android build (never into the
 * Nuxel PWA). It wires Capacitor's native App lifecycle/Back events to the
 * tiny window.SnekByteUI hook that the stage-time patch adds to snekbyte.js.
 *
 * Safety:
 *   - No remote code, no network requests, no file access.
 *   - Every listener checks that SnekByteUI exists before calling it.
 *   - Back handling is game-first; the system "exit app" only happens when the
 *     game reports it is already at the root menu (double-back style exit).
 */
(function () {
  'use strict';

  function ui() { return window.SnekByteUI || null; }

  function ready() {
    var cap = window.Capacitor;
    if (!cap || !cap.Plugins || !cap.Plugins.App) return null;
    return cap.Plugins.App;
  }

  function addAppListener(event, handler) {
    var app = ready();
    if (!app) return false;
    try {
      var p = app.addListener(event, handler);
      // Return a handle with a .remove() so callers can clean up.
      return p && typeof p.then === 'function' ? p : { remove: function () {} };
    } catch (e) {
      return false;
    }
  }

  function onBackButton() {
    var g = ui();
    if (g && typeof g.handleBack === 'function') {
      if (g.handleBack()) return; // consumed by the game (close dialog / pause / menu)
    }
    // At the root menu: let the system Back key perform the normal
    // "move task to back" behaviour so the user can leave the game.
    var app = ready();
    if (app && typeof app.exitApp === 'function') {
      try { app.exitApp(); } catch (e) { /* ignore */ }
    }
  }

  function onPause() {
    var g = ui();
    if (g && typeof g.requestPause === 'function') g.requestPause();
  }

  function onResume() {
    var g = ui();
    if (g && typeof g.invalidate === 'function') g.invalidate();
  }

  function boot() {
    if (addAppListener('backButton', onBackButton) === false) {
      // Capacitor absent (plain browser preview): the game already handles
      // Escape/Backspace via its own key handler, so nothing else is needed.
      return;
    }
    addAppListener('pause', onPause);
    addAppListener('resume', onResume);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}());
