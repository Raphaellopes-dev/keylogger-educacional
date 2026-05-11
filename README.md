╔══════════════════════════════════════════════════════════════════════════════╗
║                            ⚠️  WARNING  ⚠️                                  ║
║                                                                              ║
║   This is an EDUCATIONAL project ONLY. It is designed to teach how          ║
║   keyloggers work and how to defend against them.                           ║
║                                                                              ║
║   UNAUTHORIZED USE of keyloggers on systems you do not own or have          ║
║   explicit written permission to monitor is ILLEGAL and UNETHICAL.          ║
║                                                                              ║
║   Misuse of this software may violate:                                      ║
║   - Computer Fraud and Abuse Act (CFAA)                                     ║
║   - GDPR / Data Protection Laws                                             ║
║   - Local and International Cybercrime Laws                                 ║
║                                                                              ║
║   YOU have been warned. Use responsibly and ONLY on your own devices.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

# Educational Keylogger

A **strictly educational** Python keylogger project demonstrating how input
monitoring works at the system level, and how to detect and protect against
such tools. Built for cybersecurity students, ethical hackers, and developers
wanting to understand defensive security.

## Features

- **Keystroke Logging** - Captures key presses with full special key support
- **Window Tracking** - Logs active application window titles (Windows)
- **Timestamps** - Every event is timestamped for forensic analysis
- **Log Rotation** - Automatically creates a new log file each day
- **Key Statistics** - Analyze logs to see most typed keys, typing speed, active hours
- **Protection Checks** - Detect suspicious keyboard hooks and potential keyloggers
- **Service Mode** - Runs as a background daemon process

## Installation

```bash
# 1. Clone or download the project
# 2. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Start the keylogger (with big warning confirmation)
python main.py start

# Stop the keylogger
python main.py stop

# Analyze captured logs
python main.py analyze

# Check for potential keyloggers on this system
python main.py protect

# Show current logging status
python main.py status
```

## Project Structure

```
keylogger-educacional/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── WARNING.txt            # Ethical warning (displayed on first run)
├── README.md              # This file
└── keylog/                # Core package
    ├── __init__.py
    ├── listener.py        # Keystroke capture logic
    ├── analyzer.py        # Log analysis and statistics
    └── protector.py       # Keylogger detection
```

## Legal Notice

> This software is provided **for educational purposes only**. The author does
> not condone or support any illegal or unethical use of this software. Users
> are solely responsible for ensuring their use complies with all applicable
> local, state, and federal laws. Installing keyloggers on systems you do not
> own or have explicit permission to monitor is **illegal** in most
> jurisdictions.

## How to Protect Against Keyloggers

1. **Use a Password Manager** - Auto-fill credentials to avoid typing them
2. **Enable Two-Factor Authentication** - Even if keys are captured, 2FA blocks access
3. **Virtual Keyboard** - Use on-screen keyboards for sensitive input
4. **Anti-Keylogger Software** - Tools that detect and block keyboard hooks
5. **Regular Scans** - Run the `protect` command to check for suspicious hooks
6. **Keep Software Updated** - Patch vulnerabilities that keyloggers exploit
7. **Check Running Processes** - Review unfamiliar processes periodically
