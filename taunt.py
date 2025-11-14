import sys
import time
from dualsense_controller import DualSenseController

# --- Morse Code Definitions ---
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    ' ': '/'
}

# --- Timings (in seconds) ---
DOT_DURATION = 0.15
DASH_DURATION = 0.45
SYMBOL_GAP = 0.15  # Gap between dots/dashes in a letter
LETTER_GAP = 0.45  # Gap between letters
WORD_GAP = 1.0     # Gap between words

RUMBLE_BURST_DURATION = 0.05 

# --- Signal States ---
COLOR_ON = (0, 255, 0) # Green
COLOR_OFF = (0, 0, 0)
RUMBLE_ON = 255        # Max rumble for a strong "kick"
RUMBLE_OFF = 0

def play_signal(ds, duration, symbol):
    """
    Activates lightbar for the full duration.
    Activates player LEDs based on the symbol.
    Activates rumble for a short burst.
    """
    if duration <= RUMBLE_BURST_DURATION:
        duration = RUMBLE_BURST_DURATION + 0.01

    # --- Signal ON ---
    ds.lightbar.set_color(*COLOR_ON)
    ds.left_rumble.set(RUMBLE_ON)
    ds.right_rumble.set(RUMBLE_ON)
    
    # --- NEW: Set Player LEDs based on symbol ---
    if symbol == '.':
        ds.player_leds.set_center()
    elif symbol == '-':
        ds.player_leds.set_all()
    # -------------------------------------------

    # --- Wait for the short burst ---
    time.sleep(RUMBLE_BURST_DURATION)

    # --- Turn Rumble OFF, keep Lights ON ---
    ds.left_rumble.set(RUMBLE_OFF)
    ds.right_rumble.set(RUMBLE_OFF)
    
    # --- Wait for the rest of the signal's duration ---
    time.sleep(duration - RUMBLE_BURST_DURATION)
    
    # --- Turn Lightbar and LEDs OFF ---
    ds.lightbar.set_color(*COLOR_OFF)
    ds.player_leds.set_off() # NEW
    time.sleep(SYMBOL_GAP)

def play_gap(duration):
    """Waits for a gap duration (all lights and rumble off)."""
    global ds # Access the global controller object
    ds.left_rumble.set(RUMBLE_OFF)
    ds.right_rumble.set(RUMBLE_OFF)
    ds.lightbar.set_color(*COLOR_OFF)
    ds.player_leds.set_off() # NEW
    time.sleep(duration)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3.13 taunt.py <message>")
        print("Example: python3.13 taunt.py 'SOS'")
        return

    message = sys.argv[1].upper()
    global ds  # Make ds global so play_gap can access it
    ds = None

    try:
        print(f"Looking for controller to send taunt: '{message}'")
        ds = DualSenseController()
        ds.activate()
        print("Controller Active! Sending taunt...")
        time.sleep(1) # Give controller time to be ready

        for char in message:
            if char == ' ':
                print("/ (word gap)")
                play_gap(WORD_GAP)
            elif char in MORSE_CODE_DICT:
                morse_symbols = MORSE_CODE_DICT[char]
                print(f"Char: {char} ({morse_symbols})")
                
                for symbol in morse_symbols:
                    if symbol == '.':
                        print("  . (dot)")
                        play_signal(ds, DOT_DURATION, '.') # Pass symbol
                    elif symbol == '-':
                        print("  - (dash)")
                        play_signal(ds, DASH_DURATION, '-') # Pass symbol
                
                play_gap(LETTER_GAP)
            else:
                pass # Ignore characters not in the dict

        print("\nTaunt complete.")

    except Exception as e:
        print(f"\n!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!")
        print(f"An error occurred: {e}")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

    finally:
        if ds:
            print("Deactivating controller.")
            ds.left_rumble.set(0)
            # --- THIS IS THE FIX ---
            ds.right_rumble.set(0) # Was 'right_rumSble'
            # -----------------------
            ds.lightbar.set_color(0, 0, 255) # Set back to blue
            ds.player_leds.set_off() # NEW
            time.sleep(0.5)
            ds.deactivate()

if __name__ == "__main__":
    main()