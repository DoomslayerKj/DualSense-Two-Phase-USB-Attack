DualSense Two-Phase USB Attack (Lab Project)

This project demonstrates two different methods of interacting with a Sony DualSense 5 controller at a hardware level: a high-level "Hijack" and a low-level "Denial of Service" (DOS).

WARNING: This is for educational purposes and for use on your own hardware only. The DOS script (fuzz_ds5.py) is a real Denial of Service attack that will freeze your controller and requires sudo (root) privileges to run. Use at your own risk.

Project Files

setup.sh: The main setup script to install all dependencies.

attack_ds5.sh: The main bash script to orchestrate the attack.

taunt.py: (Phase 1) The Python script for the high-level "Hijack" to send Morse code.

fuzz_ds5.py: (Phase 2) The Python script for the low-level "DOS" flood.

requirements.txt: The list of all Python dependencies.

README.md: This file.

Setup (Linux Only)

This project is designed for a Debian-based Linux (like Kali or Ubuntu).

1. Make setup.sh Executable:

chmod +x setup.sh


2. Run the Setup Script:
This script must be run with sudo. It will install all system and Python dependencies for you, and set up the required hardware rules.

sudo ./setup.sh


3. Connect Controller:
After the setup script finishes, unplug your controller's USB cable and plug it back in. This is a crucial step to apply the new udev-rules.

You are now ready to run the attack.

How to Run

The main script (attack_ds5.sh) takes two arguments: MESSAGE (in quotes) and DOS_FLAG (0 or 1).

Example 1: Taunt Only (No DOS)
This will blink "SOS" in green on the controller's LEDs and rumble, then exit cleanly.

./attack_ds5.sh "SOS" 0


Example 2: Full Attack (Taunt + DOS)
This will blink "DOSSED" and then immediately launch the DOS flood, freezing the controller.

./attack_ds5.sh "DOSSED" 1
