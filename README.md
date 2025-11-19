DualSense Two-Phase USB Attack (Lab Project)

This project demonstrates two different methods of interacting with a Sony DualSense 5 controller at a hardware level: a high-level "Hijack" and a low-level "Denial of Service" (DOS).

WARNING: This is for educational purposes and for use on your own hardware only. The DOS scripts (fuzz_ds5.py and fuzz_ds5_mild.py) are real Denial of Service attacks that freeze your controller and require sudo (root) privileges to run. Use at your own risk.

Project Files

setup.sh: The main setup script to install all dependencies.

attack_ds5.sh: The main orchestration script (use this to run the attack).

taunt.py: (Phase 1) The Python script for the high-level "Hijack" to send Morse code.

fuzz_ds5.py: (Phase 2, Mode 2) The Python script for the Extreme DOS flood.

fuzz_ds5_mild.py: (Phase 2, Mode 1) The Python script for the Mild (Intermittent) DOS burst cycle.

latency_analyzer.py: The external measurement tool (run separately).

requirements.txt: The list of all Python dependencies.

README.md: This file.

Setup (Linux Only)

Make setup.sh Executable:

chmod +x setup.sh


Run the Setup Script:

sudo ./setup.sh


Connect Controller:
After the setup script finishes, unplug your controller's USB cable and plug it back in.

How to Run the Experiments

The main script (attack_ds5.sh) takes two arguments: MESSAGE (in quotes) and DOS_FLAG (0, 1, or 2).

1. Baseline Test (Taunt Only)

Command: ./attack_ds5.sh "SOS" 0

Result: Controller blinks "SOS" and returns to normal (blue light).

2. Performance Degradation Test (Mild DOS)

This requires two separate terminal windows to run simultaneously, allowing you to quantify the attack.

Window

Command

Purpose

Terminal 1 (Analyzer)

python3.13 latency_analyzer.py

Measures the input speed (baseline is ~4-8ms).

Terminal 2 (Attacker)

sudo ./attack_ds5.sh "LAG" 1

Launches the Mild DOS cycle (3s freeze / 3s recover).

Observation: During the attack, the Interval reported in Terminal 1 will spike dramatically (e.g., from 4ms to >3000ms or freeze entirely) when the burst hits, and then drop back down, proving intermittent service denial. Use the PEAK LATENCY value for your report.

3. Complete Failure Test (Extreme DOS)

Command: sudo ./attack_ds5.sh "FAILURE" 2

Result: Controller blinks "FAILURE," freezes permanently, and requires a software reset to recover.
