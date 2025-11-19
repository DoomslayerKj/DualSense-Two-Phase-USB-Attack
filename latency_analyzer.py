import time
import sys
import signal # NEW: Import signal library
from dualsense_controller import DualSenseController

# --- Global State for Latency Tracking ---
last_report_time = 0.0
total_reports = 0
highest_latency_ms = 0.0 # NEW: Variable to track the peak delay

def on_gyroscope_change(gyroscope):
    """
    This callback is triggered every time the controller sends an input report.
    It measures the interval and updates the global highest latency.
    """
    global last_report_time
    global total_reports
    global highest_latency_ms # Access global tracker

    current_time = time.time()
    total_reports += 1

    if last_report_time > 0:
        # Calculate time since the last report (in milliseconds)
        interval_ms = (current_time - last_report_time) * 1000

        # Update highest latency if the current interval is larger
        if interval_ms > highest_latency_ms:
            highest_latency_ms = interval_ms

        # Print detailed latency data
        if total_reports > 10:
            print(
                f"Interval: {interval_ms:.3f} ms | Peak: {highest_latency_ms:.3f} ms | Total Reports: {total_reports} | Gyro Z: {gyroscope.z}",
                end='\r',
                flush=True
            )

    last_report_time = current_time

def signal_handler(sig, frame):
    """Handles Ctrl+C (SIGINT) to ensure a clean shutdown and print the final report."""
    # This function is called immediately on Ctrl+C.
    # It stops the main loop by raising KeyboardInterrupt.
    print(f"\n[SIGNAL {sig}] Detected Ctrl+C. Initiating shutdown...")
    sys.exit(0) # Exit cleanly, which triggers the 'finally' block

def main():
    global ds
    ds = None
    try:
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)

        print("--- [Input Latency Analyzer] ---")
        print("Waiting for DualSense controller...")
        
        # Initialization
        ds = DualSenseController()
        ds.activate()

        # Subscribe to gyroscope changes for high-frequency reports
        ds.gyroscope.on_change(on_gyroscope_change)
        
        print("Analyzer Active. Baseline report rate should be ~4ms to ~8ms.")
        print("Move the controller slightly to initiate reports. Run DOS in a separate terminal.")
        
        # Keep the program running indefinitely
        while True:
            time.sleep(1)

    except SystemExit:
        # Caught by signal_handler
        pass 
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        print("Ensure the controller is not attached to another program.")

    finally:
        if ds:
            # Print the summary statistics
            print("\n" + "="*50)
            print(f"| FINAL ANALYSIS COMPLETE |")
            print(f"| Baseline Rate: ~4ms")
            print(f"| Total Reports Measured: {total_reports}")
            print(f"| PEAK LATENCY (DOS Impact): {highest_latency_ms:.3f} ms")
            print("="*50)

            print("Analyzer shutting down.")
            ds.deactivate()

if __name__ == "__main__":
    main()
