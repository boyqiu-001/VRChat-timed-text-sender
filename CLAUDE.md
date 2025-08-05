# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VRChat OSC Message Sender** - A Python application that sends timed chat messages to VRChat via OSC protocol with a tkinter GUI.

## Quick Start Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Test individual components
python -c "from osc_client import OSCClient; print('OSC client imported successfully')"
```

### Building
```bash
# Build executable (Windows)
build.bat

# Build executable (cross-platform)
python build.py
```

## Architecture

### Core Components
- **main.py**: Application entry point, handles initialization and startup
- **gui.py**: tkinter GUI implementation with all user interface elements
- **osc_client.py**: OSC communication wrapper using python-osc library
- **message_sender.py**: Thread-based message scheduling and sending logic
- **config_manager.py**: JSON-based configuration persistence

### Key Design Patterns
- **Observer Pattern**: MessageSender uses callbacks to notify GUI of status changes
- **Threading**: Non-blocking message sending via threading.Timer
- **MVC-like**: GUI (View) -> MessageSender (Controller) -> OSCClient (Model)

## File Structure
```
osc-timer/
├── main.py              # Entry point
├── gui.py               # tkinter GUI
├── osc_client.py        # OSC communication
├── message_sender.py    # Message scheduling
├── config_manager.py    # Configuration
├── build.py            # PyInstaller script
├── build.bat           # Windows build batch
└── requirements.txt    # Dependencies
```

## Key Configuration
- **OSC Target**: `/chatbox/input` (VRChat's chat message endpoint)
- **Default Port**: 9000 (VRChat OSC default)
- **Config File**: `config.json` (auto-created)
- **Build Output**: `dist/VRChat-OSC-Sender.exe`

## Development Notes
- Uses python-osc for OSC protocol implementation
- tkinter for cross-platform GUI
- PyInstaller for single-file executable generation
- Threading used for non-blocking message sending
- Configuration auto-saved on window close

## Testing OSC Connection
- VRChat must have OSC enabled in settings
- Default IP: 127.0.0.1 (localhost)
- Test button in GUI verifies connection before sending