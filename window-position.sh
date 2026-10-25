#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Saved Window Position
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🪟
# @raycast.packageName Window

# Documentation:
# @raycast.description Resize the frontmost window to a saved size and center it on its current screen
# @raycast.author ahmosys
# @raycast.authorURL https://raycast.com/ahmosys

# Saved size in macOS points (clamped to the screen's usable area)
W=1309 H=1016

osascript -l JavaScript - "$W" "$H" <<'JXA'
ObjC.import("AppKit");

function run([w, h]) {
  w = Number(w);
  h = Number(h);
  const proc = Application("System Events").applicationProcesses.whose({ frontmost: true })[0];
  const win = proc.windows[0];
  const [x, y] = win.position();
  const [cw, ch] = win.size();

  // NSScreen uses bottom-left origin; System Events uses top-left of the main screen
  const screens = $.NSScreen.screens;
  const mainH = screens.objectAtIndex(0).frame.size.height;
  const cx = x + cw / 2;
  const cy = mainH - (y + ch / 2);

  let visible = screens.objectAtIndex(0).visibleFrame;
  for (let i = 0; i < screens.count; i++) {
    const s = screens.objectAtIndex(i);
    const f = s.frame;
    if (cx >= f.origin.x && cx < f.origin.x + f.size.width && cy >= f.origin.y && cy < f.origin.y + f.size.height) {
      visible = s.visibleFrame;
      break;
    }
  }

  const vw = visible.size.width;
  const vh = visible.size.height;
  const vTop = mainH - (visible.origin.y + vh);
  w = Math.min(w, vw);
  h = Math.min(h, vh);

  // Move first so macOS does not clamp the size to the previous screen, then re-center
  const pos = [Math.round(visible.origin.x + (vw - w) / 2), Math.round(vTop + (vh - h) / 2)];
  win.position = pos;
  win.size = [w, h];
  win.position = pos;
}
JXA
