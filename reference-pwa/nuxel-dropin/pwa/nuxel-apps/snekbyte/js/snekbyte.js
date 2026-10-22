/* SnekByte mobile shell. Core game logic is the original Python parity port in snek-engine.js.
 * Offline-first, no framework, no remote calls, no privileged device permissions.
 */
(function () {
  'use strict';
  var E = window.SnekEngine;
  if (!E) throw new Error('SnekByte engine is unavailable');
  var $ = function (id) { return document.getElementById(id); };
  var canvas = $('screen'), ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('2D canvas unavailable');
  var cfg = E.cloneConfig({});
  // Nuxel defaults to WoNQ enabled to demonstrate the poo meter; the canonical
  // engine defaults remain unchanged and still pass upstream Python parity tests.
  cfg.defaultWonqMode = true;
  var PREFS_KEY = 'nuxel-snekbyte-settings-v2';
  var OLD_PREFS_KEY = 'nuxel-snekbyte-settings-v1';
  var view = { mode: 'menu', paused: false, game: null, settings: E.settings(cfg), activeSettings: null, grid: true,
    highScore: 0, raf: null, last: 0, accumulator: 0, dirty: true, directionQueued: false,
    wasRunningBeforeHide: false, dialog: null, overlaySelection: 0 };
  var playingSettings = function () { return view.mode === 'playing' && view.activeSettings ? view.activeSettings : view.settings; };
  var tickMs = function () { return 1000 / E.speedOf(cfg, playingSettings()); };
  var lastScore = -1, lastCounter = -1;

  function toast(s) {
    $('toast').textContent = s;
    $('toast').classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(function () { $('toast').classList.remove('show'); }, 2100);
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function savePrefs() {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify({
      speedIndex: view.settings.speedIndex, wonqMode: view.settings.wonqMode,
      showGrid: view.grid, highScore: view.highScore
    })); } catch (e) { /* game remains playable with storage disabled */ }
  }
  function loadPrefs() {
    try {
      var raw = localStorage.getItem(PREFS_KEY) || localStorage.getItem(OLD_PREFS_KEY);
      if (!raw) return;
      var p = JSON.parse(raw);
      if (Number.isInteger(p.speedIndex)) view.settings.speedIndex = clamp(p.speedIndex, 0, 4);
      if (typeof p.wonqMode === 'boolean') view.settings.wonqMode = p.wonqMode;
      if (typeof p.showGrid === 'boolean') view.grid = p.showGrid;
      if (Number.isFinite(p.highScore) && p.highScore >= 0) view.highScore = Math.floor(p.highScore);
    } catch (e) { /* invalid old state must not crash launch */ }
  }
  function renderStats() {
    var score = view.game ? view.game.score : 0;
    $('score').textContent = String(score);
    $('best').textContent = String(Math.max(view.highScore, score));
    $('speed').textContent = String(E.speedOf(cfg, playingSettings()));
    $('status').textContent = view.mode === 'playing' ? (view.paused ? 'PAUSED' : 'GO!') :
      view.mode === 'over' ? 'GAME OVER' : 'READY';
    $('pause-button').innerHTML = view.mode === 'playing' && !view.paused ? '⏸ <span>PAUSE</span>' : '▶ <span>RESUME</span>';
    var counter = view.game ? view.game.shitCounter : 0;
    var activeWonq = playingSettings().wonqMode;
    $('meter-count').textContent = (activeWonq ? counter : 'OFF') + ' / ' + cfg.wonqModePoopThreshold;
    $('meter-progress').setAttribute('aria-valuenow', String(activeWonq ? counter : 0));
    $('meter-progress').setAttribute('aria-valuetext', activeWonq ? counter + ' of 5 snacks' : 'WoNQ mode disabled');
    $('meter').classList.toggle('disabled', !activeWonq);
    Array.prototype.forEach.call($('meter-progress').children, function (n, i) {
      n.classList.toggle('filled', activeWonq && i < counter);
    });
    $('meter-note').textContent = activeWonq ?
      'Every 5 snacks drops a permanent poop obstacle. Watch your tail!' :
      'WoNQ Mode is off — enable it in Settings for poop obstacles.';
    if (score !== lastScore || counter !== lastCounter) {
      lastScore = score; lastCounter = counter;
    }
  }
  function showOverlay(title, desc, actions) {
    $('overlay').hidden = false;
    $('overlay-title').textContent = title;
    $('overlay-subtitle').textContent = desc;
    var container = $('overlay-buttons');
    container.textContent = '';
    actions.forEach(function (item, i) {
      var button = document.createElement('button');
      button.type = 'button'; button.textContent = item.label;
      if (i === 0) button.className = 'primary';
      button.addEventListener('click', item.action);
      container.appendChild(button);
    });
  }
  function hideOverlay() { $('overlay').hidden = true; }
  function showMenu() {
    view.mode = 'menu'; view.paused = true; view.accumulator = 0;
    showOverlay('SNEKBYTE', 'Eat snacks. Grow longer. Drop chaos. WoNQ mode is ' + (view.settings.wonqMode ? 'ON' : 'OFF') + '.', [
      { label: '▶ PLAY', action: startGame },
      { label: '⚙ SETTINGS', action: openSettings }
    ]);
    renderStats(); view.dirty = true;
  }
  function startGame() {
    // Never modify cfg rules; use the exact port of the Python game.
    var seed = Date.now() >>> 0;
    view.game = E.reset(cfg, [], E.createRng(seed));
    view.activeSettings = E.settings(cfg, { speedIndex: view.settings.speedIndex, wonqMode: view.settings.wonqMode, foodPlan: null, rng: E.createRng((seed ^ 0x45fb79ad) >>> 0) });
    view.mode = 'playing'; view.paused = false; view.accumulator = 0;
    view.directionQueued = false; view.last = 0;
    hideOverlay(); renderStats(); view.dirty = true;
    if (document.visibilityState !== 'hidden') startLoop();
    try { canvas.focus({ preventScroll: true }); } catch (e) { canvas.focus(); }
  }
  function finishGame() {
    view.mode = 'over'; view.paused = true;
    if (view.game.score > view.highScore) { view.highScore = view.game.score; savePrefs(); toast('NEW HIGH SCORE!'); }
    var why = { wall: 'The wall won.', self: 'Your tail fought back.', poop: 'You stepped in it. 💩' }[view.game.cause] || 'Game over.';
    showOverlay('GAME OVER', why + ' Score: ' + view.game.score + '.', [
      { label: '↻ RETRY', action: startGame },
      { label: '☰ MENU', action: showMenu }
    ]);
    renderStats(); view.dirty = true;
  }
  function setPause(paused) {
    if (view.mode !== 'playing') return;
    view.paused = !!paused;
    view.accumulator = 0; view.last = 0;
    if (view.paused) showOverlay('PAUSED', 'Taking a breather? The snake is waiting.', [
      { label: '▶ RESUME', action: function () { setPause(false); } },
      { label: '☰ MENU', action: showMenu }
    ]);
    else { hideOverlay(); startLoop(); }
    renderStats(); view.dirty = true;
  }
  function openDialog(which) {
    // Playing is paused while a dialog is open, including if it was open already.
    if (view.mode === 'playing' && !view.paused) setPause(true);
    view.dialog = which;
    $(which + '-panel').hidden = false;
    if (which === 'settings') {
      $('speed-setting').value = String(view.settings.speedIndex);
      $('wonq-setting').checked = !!view.settings.wonqMode;
      $('grid-setting').checked = !!view.grid;
      updateSpeedLabel();
    }
    view.dirty = true;
  }
  function closeDialog() {
    if (!view.dialog) return;
    $(view.dialog + '-panel').hidden = true;
    view.dialog = null;
    view.dirty = true;
  }
  function openSettings() { openDialog('settings'); }
  function updateSpeedLabel() {
    $('speed-label').textContent = E.speedName(cfg, view.settings) + ' · ' + E.speedOf(cfg, view.settings) + ' ticks/s';
  }
  function sendDirection(dx, dy) {
    if (view.mode !== 'playing' || view.paused || !view.game || view.directionQueued || view.dialog) return;
    if (E.turn(view.game, [dx, dy])) view.directionQueued = true;
    // one accepted direction change per simulation tick; prevents impossible
    // 180° reversals using two touches before the next engine step.
  }
  var DIRS = { up: [0,-1], down: [0,1], left: [-1,0], right: [1,0] };
  function handleBack() {
    if (view.dialog) closeDialog();
    else if (view.mode === 'playing' && !view.paused) setPause(true);
    else if (view.mode === 'playing') showMenu();
    else if (view.mode === 'over') showMenu();
    else return false;
    return true;
  }
  function onKey(e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.target.matches('input')) return;
    if (e.key === 'Escape' || e.key === 'Backspace') {
      if (handleBack()) e.preventDefault();
      return;
    }
    if (view.dialog) return;
    var k = e.key.toLowerCase();
    var dirs = { arrowup:'up',w:'up',arrowdown:'down',s:'down',arrowleft:'left',a:'left',arrowright:'right',d:'right' };
    if (dirs[k]) { var d = DIRS[dirs[k]]; sendDirection(d[0], d[1]); e.preventDefault(); }
    else if (k === ' ' || k === 'p') {
      if (view.mode === 'playing') { setPause(!view.paused); e.preventDefault(); }
      else if (view.mode === 'menu' || view.mode === 'over') { startGame(); e.preventDefault(); }
    } else if (k === 'enter' && view.mode !== 'playing') { startGame(); e.preventDefault(); }
  }
  function initSwipe() {
    var ox = 0, oy = 0, pointerId = null;
    // Pointer events on the canvas only; buttons and nav dock keep normal touch semantics.
    canvas.addEventListener('pointerdown', function (e) {
      if (view.mode !== 'playing' || view.paused) return;
      if (pointerId !== null) return;
      pointerId = e.pointerId; ox = e.clientX; oy = e.clientY;
      try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
    });
    canvas.addEventListener('pointerup', function (e) {
      if (pointerId !== e.pointerId) return;
      var dx = e.clientX - ox, dy = e.clientY - oy;
      pointerId = null;
      var threshold = 22;
      if (Math.max(Math.abs(dx), Math.abs(dy)) < threshold) return;
      var d = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? DIRS.right : DIRS.left) : (dy > 0 ? DIRS.down : DIRS.up);
      sendDirection(d[0], d[1]);
    });
    ['pointercancel', 'lostpointercapture'].forEach(function (type) {
      canvas.addEventListener(type, function () { pointerId = null; });
    });
  }
  function fillRect(x,y,w,h,c) { ctx.fillStyle=c; ctx.fillRect(x,y,w,h); }
  function drawCell(p, color, border) {
    var s=cfg.gridSize, x=p[0]*s, y=p[1]*s;
    fillRect(x+1,y+1,s-2,s-2,color);
    if (border) { ctx.strokeStyle=border;ctx.lineWidth=1;ctx.strokeRect(x+1.5,y+1.5,s-3,s-3); }
  }
  function drawPoop(p) {
    var s=cfg.gridSize, x=p[0]*s,y=p[1]*s;
    fillRect(x+3,y+12,s-6,5,'#784b2d');
    fillRect(x+5,y+8,s-10,5,'#b97b3e');
    fillRect(x+7,y+4,s-14,5,'#dfae6b');
    fillRect(x+7,y+8,2,2,'#0b171b'); fillRect(x+11,y+8,2,2,'#0b171b');
  }
  function drawBoard() {
    var w=cfg.screenWidth,h=cfg.screenHeight,s=cfg.gridSize;
    fillRect(0,0,w,h,'#07151b');
    if (view.grid) {
      ctx.strokeStyle='rgba(40,121,142,.23)';ctx.lineWidth=1;
      ctx.beginPath();
      for (var x=0;x<=cfg.gridWidth;x++) {ctx.moveTo(x*s+.5,0);ctx.lineTo(x*s+.5,h);}
      for (var y=0;y<=cfg.gridHeight;y++) {ctx.moveTo(0,y*s+.5);ctx.lineTo(w,y*s+.5);}
      ctx.stroke();
    }
    if (!view.game) {
      ctx.fillStyle='#56d7dc';ctx.font='bold 28px monospace';ctx.textAlign='center';
      ctx.fillText('PRESS PLAY',w/2,h/2);
      return;
    }
    var game=view.game;
    game.poops.forEach(function (p) { drawPoop(p.position); });
    if (game.food.position) {
      var p=game.food.position;
      drawCell(p,'#fa6171','#ffd0cc');
      fillRect(p[0]*s+6,p[1]*s+5,6,6,'#ffd1b6');
    }
    game.snake.positions.forEach(function (p,i) {
      drawCell(p,i===0?'#f9e06f':'#84ef79',i===0?'#f8a93c':'#327c4f');
      if (i===0 && p[0]>=0 && p[0]<cfg.gridWidth && p[1]>=0 && p[1]<cfg.gridHeight) {
        fillRect(p[0]*s+5,p[1]*s+6,3,3,'#08151a');
        fillRect(p[0]*s+12,p[1]*s+6,3,3,'#08151a');
      }
    });
  }
  function loop(ts) {
    view.raf=null;
    if (document.visibilityState === 'hidden') return;
    var delta=view.last?clamp(ts-view.last,0,120):0;
    view.last=ts;
    if (view.mode==='playing' && !view.paused && !view.dialog) {
      view.accumulator+=delta;
      var period=tickMs(), steps=0;
      while (view.accumulator>=period && steps<3) {
        view.accumulator-=period;steps++;
        var beforePoopCount=view.game.poops.length;
        E.step(view.game,view.activeSettings); view.directionQueued=false;
        if (view.game.poops.length>beforePoopCount) {
          toast('💩 POO DROP! Watch your tail!');
          $('meter').classList.add('drop-flash');
          clearTimeout(view.pooFlashTimer);
          view.pooFlashTimer=setTimeout(function(){$('meter').classList.remove('drop-flash');},480);
        }
        // Don't accumulate unbounded telemetry or memory in long-running sessions.
        if (view.game.events.length>80) view.game.events.splice(0,view.game.events.length-60);
        renderStats();view.dirty=true;
        if (view.game.gameOver) { finishGame();break; }
      }
      if (steps>=3) view.accumulator=0; // avoid catch-up storms after device stalls
    }
    if (view.dirty) { drawBoard();view.dirty=false; }
    // Menu/paused screens need no continuous 60 FPS polling; stop the rAF
    // after painting once. Game loop restarts on Start/Resume.
    if (view.mode==='playing' && !view.paused && !view.dialog) startLoop();
  }
  function startLoop() {
    if (view.raf!==null || document.visibilityState==='hidden') return;
    view.raf=requestAnimationFrame(loop);
  }
  function stopLoop() { if(view.raf!==null)cancelAnimationFrame(view.raf);view.raf=null;view.last=0; }
  function invalidate() {view.dirty=true;startLoop();if(view.mode!=='playing'||view.paused)setTimeout(function(){ if(view.dirty){drawBoard();view.dirty=false;} },0);}
  function onVisibility() {
    if (document.visibilityState==='hidden') {
      if(view.mode==='playing'&&!view.paused)setPause(true);
      stopLoop();savePrefs();
    } else { view.last=0;invalidate(); }
  }
  function install() {
    loadPrefs();
    $('best').textContent=String(view.highScore);
    $('settings-button').addEventListener('click',openSettings);
    $('help-button').addEventListener('click',function(){openDialog('help');});
    $('settings-close').addEventListener('click',closeDialog);
    $('settings-done').addEventListener('click',closeDialog);
    $('help-close').addEventListener('click',closeDialog);
    $('help-done').addEventListener('click',closeDialog);
    $('speed-setting').addEventListener('input',function(){view.settings.speedIndex=clamp(Number(this.value)||0,0,4);updateSpeedLabel();renderStats();savePrefs();});
    $('wonq-setting').addEventListener('change',function(){
      // Switching rules mid-round would make pre-existing poop obstacles inert.
      // Apply only to next round; pause current round and explain clearly.
      view.settings.wonqMode=!!this.checked;
      savePrefs();renderStats();toast('WoNQ mode '+(this.checked?'ON':'OFF')+' — applies to next game');
    });
    $('grid-setting').addEventListener('change',function(){view.grid=!!this.checked;savePrefs();invalidate();});
    $('back-button').addEventListener('click',function(){if(!handleBack())showMenu();});
    $('pause-button').addEventListener('click',function(){if(view.mode==='playing')setPause(!view.paused);});
    Array.prototype.forEach.call(document.querySelectorAll('[data-dir]'),function(button){
      button.addEventListener('click',function(){var d=DIRS[button.getAttribute('data-dir')];sendDirection(d[0],d[1]);});
    });
    document.addEventListener('keydown',onKey);
    initSwipe();
    document.addEventListener('visibilitychange',onVisibility);
    window.addEventListener('pagehide',function(){ if(view.mode==='playing'&&!view.paused)setPause(true);stopLoop();savePrefs(); });
    window.addEventListener('resize',invalidate);
    showMenu();invalidate();
    // Service worker optional: WebKitGTK deployments without SW still run offline
    // as a locally served, network-independent application.
    if ('serviceWorker' in navigator && window.isSecureContext) {
      navigator.serviceWorker.register('./sw.js',{scope:'./'}).catch(function(){ /* optional */ });
    }
  }
  if (document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);
  else install();
}());
