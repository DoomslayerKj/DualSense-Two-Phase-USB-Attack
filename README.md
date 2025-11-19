🎮 DualSense Two-Phase USB Attack (Advanced DOS Lab)

This project demonstrates a rigorous comparative analysis of attack vectors against the Sony DualSense 5 controller's firmware. It exploits the difference between high-level application control and low-level hardware communication.

⚠️ WARNING: Hostile Code and Usage

THIS IS A DENIAL OF SERVICE (DOS) ATTACK. This repository contains code that performs real-time resource exhaustion on embedded hardware.

USE ONLY ON YOUR OWN DEVICES.

The DOS scripts (fuzz_ds5.py and fuzz_ds5_mild.py) require root privileges (sudo) because they forcibly detach the kernel driver.

The system setup requires using --break-system-packages (automated by setup.sh), which is suitable only for dedicated lab VMs (like Kali).

⚙️ Project Architecture & Technical Goals

The lab is split into two distinct phases, leveraging different Python libraries and OS permissions to prove a security concept:

Phase

Script

Library

Target

Goal Demonstrated

Phase 1: Hijack

taunt.py

dualsense-controller

HID Interface

High-Level Control (Sending proprietary Output Reports to control lights/rumble, with OS permission).

Phase 2: DOS

fuzz_ds5.py

pyusb

Control Endpoint (EP0)

Firmware Task Starvation (Bypassing the kernel to send abusive SET_CONFIGURATION packets).

💾 Project Files

File

Description

setup.sh

Automated Installer: Installs all system and Python dependencies (python3.13, libhidapi-dev, udev-rules).

attack_ds5.sh

Orchestrator: The main script to launch the taunt and select the DOS mode.

taunt.py

Phase 1: Blinks Morse code in "Hacker Green" (0, 255, 0) with haptic taps.

fuzz_ds5.py

Phase 2 (Mode 2 - Extreme): The permanent firmware DOS flood.

fuzz_ds5_mild.py

Phase 2 (Mode 1 - Mild): The intermittent DOS burst cycle for latency measurement.

latency_analyzer.py

External tool for quantifying the attack's impact on input performance.

requirements.txt

Python package list (dualsense-controller, pyusb).

🚀 Setup (Linux/Kali VM)

Make setup.sh Executable:

chmod +x setup.sh


Run the Setup Script (Requires SUDO):

sudo ./setup.sh


Controller Connection: After the setup script completes, unplug your controller and plug it back in to ensure the new udev hardware rules are applied.

🔬 Experiment Execution

The main script (attack_ds5.sh) takes two required arguments: the MESSAGE (in quotes) and the DOS_FLAG (0, 1, or 2).

I. Performance Degradation Test (Mild DOS: FLAG 1)

This mode demonstrates Intermittent Denial of Service and requires running two terminals simultaneously to quantify the attack's impact.

Window

Command

Purpose

Expected Latency

Terminal 1 (Analyzer)

python3.13 latency_analyzer.py

Measurement: Reports input speed (baseline is ~4-8ms).

Spikes to >3000ms

Terminal 2 (Attacker)

sudo ./attack_ds5.sh "LAG" 1

Attack: Launches the Mild DOS burst cycle.



II. Complete Failure Test (Extreme DOS: FLAG 2)

Command: sudo ./attack_ds5.sh "FREEZE" 2

Result: Controller blinks "FREEZE," then instantly stops communicating, requiring a software/physical reset.

III. Baseline Test (Taunt Only: FLAG 0)

Command: ./attack_ds5.sh "SOS" 0

Result: Controller blinks "SOS" and returns to normal (proves the Hijack works without DOS).