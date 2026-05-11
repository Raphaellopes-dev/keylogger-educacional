"""
Protector module - Keylogger detection and protection.

Provides educational tools to check a Windows system for:
    - Suspicious running processes
    - Keyboard hook installations
    - Known keylogger process names

For educational use only. Helps users understand how anti-keylogger
software works.
"""

import os
import sys
import ctypes
from pathlib import Path


# Known keylogger-related process names (educational sample)
SUSPICIOUS_PROCESSES = [
    "keylogger", "keylog", "logkeys", "pykeylogger",
    "refog", "actualspy", "kidlogger", "spytech",
    "e-blaster", "flexispy", "mobile-spy", "mspy",
    "theone", "winspy", "advanced-keylogger",
]

# Known legitimate processes that can be used for keylogging
LEGITIMATE_HOOK_PROCESSES = [
    "ctfmon.exe", "osk.exe", "tabtip.exe",
]


def check_processes():
    """
    Scan running processes for suspicious names.

    Returns:
        list: Matching suspicious processes found.
    """
    found = []
    try:
        import psutil
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                name = proc.info["name"] or ""
                cmdline = " ".join(proc.info["cmdline"] or [])

                for suspicious in SUSPICIOUS_PROCESSES:
                    if suspicious.lower() in name.lower():
                        found.append({
                            "pid": proc.info["pid"],
                            "name": name,
                            "reason": f"Name matches known keylogger: '{suspicious}'",
                            "cmdline": cmdline[:200],
                        })
                        break

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except ImportError:
        return [{"error": "psutil not installed. Run: pip install psutil"}]

    return found


def check_keyboard_hooks():
    """
    Check for system-wide keyboard hooks (Windows).

    Uses Win32 API to enumerate keyboard hooks.
    This is a simplified educational check.

    Returns:
        list: Detected hook information.
    """
    hooks = []
    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # Check SetWindowsHookEx with WH_KEYBOARD_LL (low-level keyboard hook)
        # This is a simplified detection - real detection is more complex
        WH_KEYBOARD_LL = 13

        # We can't enumerate hooks directly via public Win32 API,
        # but we can check for common hook DLLs
        common_hooks = [
            "keyhook.dll", "keyboard_hook.dll", "log_hook.dll",
        ]

        for dll_name in common_hooks:
            # Check if the DLL is loaded in any process
            for proc_entry in os.popen("tasklist /M " + dll_name + " 2>nul").readlines():
                if "No tasks" not in proc_entry and dll_name.lower() in proc_entry.lower():
                    hooks.append({
                        "type": "Keyboard Hook DLL",
                        "dll": dll_name,
                        "process": proc_entry.strip(),
                    })

    except Exception as e:
        hooks.append({"error": str(e)})

    return hooks


def check_startup_entries():
    """
    Check for suspicious startup entries that might auto-launch keyloggers.

    Returns:
        list: Suspicious startup entries.
    """
    entries = []
    startup_paths = [
        Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup",
        Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup",
    ]

    for startup_dir in startup_paths:
        if startup_dir.exists():
            for item in startup_dir.iterdir():
                for suspicious in SUSPICIOUS_PROCESSES:
                    if suspicious.lower() in item.name.lower():
                        entries.append({
                            "path": str(item),
                            "name": item.name,
                            "location": str(startup_dir),
                        })
                        break

    return entries


def run_full_check():
    """
    Run all protection checks and return compiled results.

    Returns:
        dict: Results from all checks.
    """
    result = {
        "suspicious_processes": check_processes(),
        "keyboard_hooks": check_keyboard_hooks(),
        "startup_entries": check_startup_entries(),
        "recommendations": [],
    }

    # Generate recommendations
    if result["suspicious_processes"]:
        result["recommendations"].append(
            "Suspicious processes found. Investigate and terminate if unrecognized."
        )

    if result["keyboard_hooks"]:
        result["recommendations"].append(
            "Keyboard hooks detected. This may indicate a keylogger is installed."
        )

    if result["startup_entries"]:
        result["recommendations"].append(
            "Suspicious startup entries found. Check and remove if unknown."
        )

    if not any([result["suspicious_processes"], result["keyboard_hooks"], result["startup_entries"]]):
        result["recommendations"].append(
            "No obvious signs of keyloggers detected. Stay vigilant and check regularly."
        )

    result["recommendations"].extend([
        "Use a password manager to avoid typing sensitive data.",
        "Enable two-factor authentication on all accounts.",
        "Keep your antivirus software updated.",
        "Review installed programs and browser extensions periodically.",
    ])

    return result


def print_report(result):
    """Print a formatted protection report to the console."""
    print("=" * 60)
    print("       KEYLOGGER PROTECTION SCAN REPORT")
    print("=" * 60)

    print(f"\n{'─' * 60}")
    print("PROCESS SCAN")
    print(f"{'─' * 60}")
    if result["suspicious_processes"]:
        for p in result["suspicious_processes"]:
            if "error" in p:
                print(f"  [!] {p['error']}")
            else:
                print(f"  ⚠  PID {p['pid']:>6}  {p['name']:<30}")
                print(f"      Reason: {p['reason']}")
    else:
        print("  ✅ No suspicious processes found.")

    print(f"\n{'─' * 60}")
    print("KEYBOARD HOOKS")
    print(f"{'─' * 60}")
    if result["keyboard_hooks"]:
        for h in result["keyboard_hooks"]:
            if "error" in h:
                print(f"  [!] Hook check note: {h['error']}")
            else:
                print(f"  ⚠  {h['type']}: {h['dll']} → {h['process']}")
    else:
        print("  ✅ No unauthorized keyboard hooks detected.")

    print(f"\n{'─' * 60}")
    print("STARTUP ENTRIES")
    print(f"{'─' * 60}")
    if result["startup_entries"]:
        for e in result["startup_entries"]:
            print(f"  ⚠  {e['name']} in {e['location']}")
    else:
        print("  ✅ No suspicious startup entries found.")

    print(f"\n{'─' * 60}")
    print("RECOMMENDATIONS")
    print(f"{'─' * 60}")
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\n{'═' * 60}")
