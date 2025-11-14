#!/bin/bash

# This script automates the full setup for the DualSense Attack Lab.
# It must be run with sudo.

# --- 1. Check for sudo ---
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run with sudo."
  echo "Usage: sudo ./setup.sh"
  exit 1
fi

echo "--- [DualSense Attack Lab Setup] ---"

# --- 2. Install System Dependencies ---
echo "[1/5] Updating system package lists..."
apt-get update

echo "[2/5] Checking for system dependencies (python3.13, libhidapi-dev)..."

# Check for Python 3.13
if ! command -v python3.13 &> /dev/null; then
    echo "python3.13 not found. Installing..."
    apt-get install -y python3.13 python3.13-dev python3-pip
else
    echo "python3.13 is already installed."
fi

# Check for libhidapi-dev
if ! dpkg -l | grep -q "libhidapi-dev"; then
    echo "libhidapi-dev not found. Installing..."
    apt-get install -y libhidapi-dev
else
    echo "libhidapi-dev is already installed."
fi

# --- 3. Install Python Dependencies ---
echo "[3/5] Installing Python (pip) dependencies..."

if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found. Aborting."
    exit 1
fi

# --- NEW: Add warning and --break-system-packages flag ---
echo ""
echo -e "\033[1;31m/!\\ WARNING /!\\\033[0m"
echo "This script will use 'pip install --break-system-packages'."
echo "This is required on many modern Linux distros to bypass the"
echo "'externally-managed-environment' protection."
echo ""
echo "This is generally safe for a dedicated lab VM like Kali,"
echo "but it is not recommended on a primary production machine."
echo ""
echo -e "Continuing in 5 seconds... (Press \033[1;33mCtrl+C\033[0m to cancel)"
echo ""
sleep 5

# Install for root (for fuzz_ds5.py)
echo "Installing pip requirements for root user..."
python3.13 -m pip install --break-system-packages -r requirements.txt

# Install for the original user (for taunt.py)
# We get the original user's name from $SUDO_USER
if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
    echo "Installing pip requirements for local user ($SUDO_USER)..."
    sudo -u $SUDO_USER python3.13 -m pip install --break-system-packages -r requirements.txt
else
    echo "Warning: Could not find original user."
    echo "You may need to manually run this command as your normal user:"
    echo "python3.13 -m pip install --break-system-packages -r requirements.txt"
fi
# --------------------------------------------------------

# --- 4. Set udev-rules ---
echo "[4/5] Setting up udev rules for the controller..."

UDEV_RULE_FILE="/etc/udev/rules.d/99-dualsense.rules"
UDEV_RULE_CONTENT='SUBSYSTEM=="hidraw", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", MODE="0666"'

if [ -f "$UDEV_RULE_FILE" ]; then
    echo "udev rule file already exists. Skipping creation."
else
    echo "Creating udev rule file..."
    echo $UDEV_RULE_CONTENT | tee $UDEV_RULE_FILE
fi

echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger

# --- 5. Set File Permissions ---
echo "[5/5] Setting file permissions..."

if [ -f "attack_ds5.sh" ]; then
    chmod +x attack_ds5.sh
    echo "Made attack_ds5.sh executable."
else
    echo "Warning: attack_ds5.sh not found. Skipping."
fi

echo ""
echo "--- SETUP COMPLETE ---"
echo ""
echo "IMPORTANT: Unplug your controller and plug it back in NOW."
echo "This is required to apply the new hardware rules."
echo ""
echo "You can now run the attack:"
echo "./attack_ds5.sh \"SOS\" 0"
