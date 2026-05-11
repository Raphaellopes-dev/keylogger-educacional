#!/usr/bin/env python3
"""
Educational Keylogger - CLI Entry Point

A strictly educational tool for understanding how keyloggers work
and how to defend against them. For educational use only.

Commands:
    start   - Start the keylogger (requires warning acknowledgment)
    stop    - Stop the running keylogger
    status  - Check if the keylogger is running
    analyze - Analyze captured log files
    protect - Scan system for potential keyloggers
"""

import sys
import os
from pathlib import Path

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keylog.listener import Keylogger
from keylog import analyzer
from keylog import protector


WARNING_FILE = Path(__file__).parent / "WARNING.txt"


def show_warning():
    """Display and require acceptance of the ethical warning."""
    if WARNING_FILE.exists():
        print(WARNING_FILE.read_text(encoding="utf-8"))

    print("\n" + "!" * 60)
    print("  THIS SOFTWARE IS FOR EDUCATIONAL USE ONLY.")
    print("  Using it on systems you do not own or have")
    print("  explicit permission to monitor is ILLEGAL.")
    print("!" * 60)

    try:
        response = input("\n  Type 'I AGREE' to confirm you will use this ethically: ")
        if response.strip().upper() != "I AGREE":
            print("\n[-] You must agree to the terms. Exiting.")
            sys.exit(1)
        print("[+] Acknowledged. Proceeding...\n")
    except (KeyboardInterrupt, EOFError):
        print("\n[-] Aborted.")
        sys.exit(1)


def cmd_start():
    """Start the educational keylogger."""
    show_warning()
    kl = Keylogger()
    if kl.is_running():
        print("[!] Keylogger is already running. Use 'stop' first.")
        return
    kl.start()
    print("[*] The keylogger is now running in the background.")
    print(f"[*] Logs are stored in: {Path.home() / '.keylog_edu'}")
    print("[*] Run 'python main.py stop' to stop logging.")


def cmd_stop():
    """Stop the running keylogger."""
    kl = Keylogger()
    if not kl.is_running():
        print("[!] Keylogger is not running.")
        return
    kl.stop()
    print("[+] Keylogger has been stopped.")


def cmd_status():
    """Show keylogger status."""
    kl = Keylogger()
    running = kl.is_running()
    log_files = kl.get_logs()

    print("=" * 50)
    print("         KEYLOGGER STATUS")
    print("=" * 50)
    print(f"  Running:      {'✅ YES' if running else '❌ NO'}")
    print(f"  Log files:    {len(log_files)}")

    if log_files:
        print(f"\n  {'─' * 46}")
        print("  LOG FILES")
        print(f"  {'─' * 46}")
        for lf in log_files[-5:]:  # Show last 5
            size = lf.stat().st_size
            print(f"  {lf.name:<30} {size:>8,} bytes")

    print()


def cmd_analyze():
    """Analyze captured keystroke logs."""
    log_dir = Path.home() / ".keylog_edu"
    result = analyzer.analyze(log_dir)
    analyzer.print_report(result)


def cmd_protect():
    """Run a protection/ detection scan."""
    result = protector.run_full_check()
    protector.print_report(result)


def print_help():
    """Display help information."""
    print("=" * 50)
    print("   EDUCATIONAL KEYLOGGER - HELP")
    print("=" * 50)
    print(f"""
  Usage: python {Path(__file__).name} <command>

  Commands:
    start       Start the keylogger (⚠️  requires warning ack)
    stop        Stop the keylogger
    status      Show keylogger running status
    analyze     Analyze captured logs
    protect     Scan for potential keyloggers
    help        Show this help message

  Examples:
    python {Path(__file__).name} start
    python {Path(__file__).name} analyze
    python {Path(__file__).name} protect

  DISCLAIMER: For educational use only. Do NOT use on
  systems you do not own or have permission to monitor.
""")


def main():
    """Main CLI dispatcher."""
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    commands = {
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "analyze": cmd_analyze,
        "protect": cmd_protect,
        "help": print_help,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"[-] Unknown command: {command}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
