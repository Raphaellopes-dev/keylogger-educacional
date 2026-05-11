"""
Analyzer module - Log analysis and statistical reporting.

Reads keylog files and produces human-readable reports including:
    - Most frequently typed keys
    - Typing speed (keys per minute)
    - Active hours / usage patterns
    - Character frequency distribution

For educational use only.
"""

import re
from datetime import datetime
from collections import Counter
from pathlib import Path


def _read_logs(log_paths):
    """Read and concatenate content from multiple log files."""
    content = ""
    for path in sorted(log_paths):
        try:
            content += path.read_text(encoding="utf-8") + "\n"
        except Exception as e:
            print(f"[-] Error reading {path}: {e}")
    return content


def _extract_timestamps(content):
    """
    Extract ISO timestamps from log content.
    Returns list of datetime objects.
    """
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+"
    return [datetime.fromisoformat(m) for m in re.findall(pattern, content)]


def _is_printable(char):
    """Check if a character is a printable keyboard input."""
    return char.isprintable() and char not in ("\n", "\r", "\t")


def analyze(log_dir=None):
    """
    Run full analysis on all available log files.

    Args:
        log_dir: Path to log directory. Defaults to ~/.keylog_edu.

    Returns:
        dict: Analysis results.
    """
    if log_dir is None:
        log_dir = Path.home() / ".keylog_edu"

    log_dir = Path(log_dir)

    if not log_dir.exists():
        return {"error": "No log directory found. Nothing to analyze."}

    log_files = sorted(log_dir.glob("keys_*.log"))
    if not log_files:
        return {"error": "No log files found. Start the keylogger first."}

    content = _read_logs(log_files)

    # Character statistics
    chars = [c for c in content if _is_printable(c)]
    total_chars = len(chars)

    # Key frequency (printable characters)
    char_freq = Counter(chars).most_common(20)

    # Special key counts
    special_keys = re.findall(r"\[([A-Z_]+)\]", content)
    special_freq = Counter(special_keys).most_common(10)

    # Window switches
    windows = re.findall(r"--- \[Window: (.+?)\] ---", content)
    window_freq = Counter(windows).most_common(10)

    # Typing speed & active hours
    timestamps = _extract_timestamps(content)
    typing_speed = 0.0
    active_hours = {}

    if len(timestamps) >= 2:
        time_span = (timestamps[-1] - timestamps[0]).total_seconds()
        if time_span > 0:
            typing_speed = round(total_chars / (time_span / 60), 2)

        # Count entries per hour
        for ts in timestamps:
            hour = ts.strftime("%H:00")
            active_hours[hour] = active_hours.get(hour, 0) + 1

    # Sort active hours
    active_hours_sorted = sorted(active_hours.items(), key=lambda x: x[1], reverse=True)

    # Log file stats
    log_sizes = [(f.name, f.stat().st_size) for f in log_files]

    result = {
        "total_log_files": len(log_files),
        "log_files": [str(f) for f in log_files],
        "log_sizes": log_sizes,
        "total_characters_logged": total_chars,
        "most_typed_characters": char_freq,
        "most_typed_special_keys": special_freq,
        "window_switches": window_freq,
        "typing_speed_kpm": typing_speed,
        "active_hours": active_hours_sorted,
        "unique_characters": len(set(chars)),
    }

    return result


def print_report(result):
    """Print a formatted analysis report to the console."""
    print("=" * 60)
    print("           KEYLOG ANALYSIS REPORT")
    print("=" * 60)

    if "error" in result:
        print(f"\n[!] {result['error']}")
        return

    print(f"\n📁  Log Files:        {result['total_log_files']}")
    print(f"📝  Total Keystrokes: {result['total_characters_logged']:,}")
    print(f"🔤  Unique Keys:      {result['unique_characters']}")
    print(f"⚡  Typing Speed:     {result['typing_speed_kpm']} keys/min")

    print(f"\n{'─' * 60}")
    print("TOP 15 MOST TYPED CHARACTERS")
    print(f"{'─' * 60}")
    for char, count in result["most_typed_characters"][:15]:
        display = repr(char).strip("'")
        print(f"  {display:>8}  →  {count}")

    if result["most_typed_special_keys"]:
        print(f"\n{'─' * 60}")
        print("TOP SPECIAL KEYS")
        print(f"{'─' * 60}")
        for key, count in result["most_typed_special_keys"][:10]:
            print(f"  [{key:>10}]  →  {count}")

    if result["window_switches"]:
        print(f"\n{'─' * 60}")
        print("MOST USED APPLICATIONS")
        print(f"{'─' * 60}")
        for window, count in result["window_switches"][:10]:
            print(f"  {window:<40} {count}")

    if result["active_hours"]:
        print(f"\n{'─' * 60}")
        print("MOST ACTIVE HOURS (logged events)")
        print(f"{'─' * 60}")
        for hour, count in result["active_hours"][:10]:
            print(f"  {hour:<10} →  {count} events")

    print(f"\n{'═' * 60}")
