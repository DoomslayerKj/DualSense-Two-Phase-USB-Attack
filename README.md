# **🎮 DualSense Two-Phase USB Attack (Advanced DOS Lab)**

**Thesis:** This project demonstrates that consumer-grade embedded controllers are vulnerable to **Firmware Task Starvation** and proves the necessity of kernel-level driver detachment to execute hostile, low-level USB attacks.

### **⚠️ WARNING: Hostile Code and Usage**

**THIS IS A DENIAL OF SERVICE (DOS) ATTACK.** This repository contains code that performs **real-time resource exhaustion** on embedded hardware.

* **USE ONLY ON YOUR OWN DEVICES.**  
* The DOS scripts (fuzz\_ds5.py and fuzz\_ds5\_mild.py) require **root privileges (sudo)** because they forcibly detach the kernel driver (dev.detach\_kernel\_driver(0)).  
* The system setup requires using \--break-system-packages (automated by setup.sh), suitable only for dedicated lab VMs.

### **🧠 Project Architecture & Technical Goals**

The lab is split into two distinct phases, comparing the "polite" and "hostile" methods of USB communication:

| Phase | Script | Library | Target | Goal Demonstrated |
| :---- | :---- | :---- | :---- | :---- |
| **Phase 1: Hijack (Control)** | taunt.py | dualsense-controller | **HID Interface** | **High-Level Control** (Sending proprietary *Output Reports* to control lights/rumble, with OS permission). |
| **Phase 2: DOS** | fuzz\_ds5.py | pyusb | **Control Endpoint (EP0)** | **Firmware Task Starvation** (Bypassing the kernel to send abusive SET\_CONFIGURATION packets). |

### **📊 Experiment Execution**

The main script (attack\_ds5.sh) takes two required arguments: the MESSAGE (in quotes) and the DOS\_FLAG (0, 1, or 2).

0 = NO DOS, 1 = Mild DOS, 2 = MAX DOS

#### **I. Performance Degradation Test (Mild DOS: FLAG 1\)**

This mode demonstrates **Intermittent Denial of Service** by cycling between a **Burst Phase** (Hostile Detachment) and a **Recovery Phase** (Driver Re-attachment). This test must be run alongside the latency\_analyzer.py tool.

| Window | Command | Purpose | Impact |
| :---- | :---- | :---- | :---- |
| **Terminal 1 (Analyzer)** | python3.13 latency\_analyzer.py | **Measurement:** Reports input speed (baseline is **\~4-8ms**). | **Spikes to \>3000ms** |
| **Terminal 2 (Attacker)** | sudo ./attack\_ds5.sh "LAG" 1 | **Attack:** Launches the Mild DOS burst cycle. | **Input stream is visibly broken/frozen.** |

#### **II. Complete Failure Test (Extreme DOS: FLAG 2\)**

* **Command:** sudo ./attack\_ds5.sh "FREEZE" 2  
* **Result:** Controller blinks "FREEZE," then instantly stops communicating due to terminal task starvation. The device requires a full **USB Reset** (dev.reset()) to restore normal operation.

### **⚙️ Setup & File Reference**

| File | Description |
| :---- | :---- |
| setup.sh | **Automated Installer:** Installs all system and Python dependencies (python3.13, libhidapi-dev, udev-rules). |
| attack\_ds5.sh | **Orchestrator:** The main script to launch the taunt and select the DOS mode. |
| latency\_analyzer.py | External tool for *quantifying* the attack's impact on input performance. |

#### **Setup Steps (Linux/Kali VM)**

1. chmod \+x setup.sh  
2. sudo ./setup.sh

### **📝 Final Abstract**

This project successfully weaponizes the mandatory USB protocol command, SET\_CONFIGURATION, proving that high-speed, legitimate signals can exhaust the low-power ARM microcontroller in the DualSense 5\. This method achieves a robust Denial of Service that bypasses standard operating system security controls.