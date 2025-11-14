#!/bin/bash

# This script launches the two-phase controller attack.
# $1: The message to send (e.g., "DOSSED")
# $2: DOS flag (1 = run DOS, 0 = skip DOS)

MESSAGE="$1"
DOS_FLAG="$2"

# --- Input Validation ---
# Check 1: Check if arguments are empty
if [ -z "$MESSAGE" ] || [ -z "$DOS_FLAG" ]; then
    echo "Error: Missing arguments."
    echo "Usage: ./attack_ds5.sh <message> <dos_flag>"
    echo "Example: ./attack_ds5.sh \"DOSSED\" 1"
    echo "Example: ./attack_ds5.sh \"SOS\" 0"
    exit 1
fi

# Check 2: Validate message (only letters and spaces allowed)
# This 'grep' command is the most robust way to check.
# It checks if the message contains any character NOT (^) in the set A-Z, a-z, or space.
# 'echo -n' prints the message without a newline.
# 'grep -q' runs in quiet mode.
if echo -n "$MESSAGE" | grep -q "[^A-Za-z ]"; then
    echo "Error: Invalid message."
    echo "Argument 1 must contain only letters (A-Z, a-z) and spaces."
    echo "Example: \"DOSSED\" or \"SOS\""
    exit 1
fi

# Check 3: Validate DOS flag (only 0 or 1 allowed)
if ! [[ "$DOS_FLAG" == "0" || "$DOS_FLAG" == "1" ]]; then
    echo "Error: Invalid DOS flag."
    echo "Argument 2 must be exactly '0' (to skip DOS) or '1' (to run DOS)."
    exit 1
fi
# ------------------------------

echo "--- [PHASE 1: TAUNT] ---"
echo "Sending message in Morse code: $MESSAGE"
echo "------------------------------"

# Run the "polite" taunt script as the normal user
# This relies on the udev-rules we set up.
python3.13 taunt.py "$MESSAGE"

# Check if the taunt script finished successfully
if [ $? -eq 0 ]; then
    echo ""
    # --- Check the DOS Flag ---
    if [ "$DOS_FLAG" -eq 1 ]; then
        echo "--- [PHASE 2: DOS] ---"
        echo "Taunt complete. Launching DOS."
        echo "Controller will become unresponsive."
        echo "------------------------------"
        
        # Run the "hostile" DOS script as root (sudo)
        # This is required for pyusb to detach the kernel driver.
        sudo python3.13 fuzz_ds5.py
    else
        echo "--- [PHASE 2: SKIPPED] ---"
        echo "DOS_FLAG set to 0. Skipping DOS attack."
    fi
else
    echo "Phase 1 (Taunt) failed. Aborting attack."
    exit 1
fi

echo "Attack complete."