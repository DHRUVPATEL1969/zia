import sounddevice as sd
import numpy as np
import sys
import time

def print_sound_level(indata, frames, time, status):
    """This function is called for each audio block."""
    if status:
        print(status, file=sys.stderr)
    
    # Calculate the volume (Root Mean Square)
    volume_norm = np.linalg.norm(indata) * 10
    
    # Create a simple visual bar
    bar = '#' * int(volume_norm)
    
    # Print the volume level and the bar
    # The `\r` at the end makes the line overwrite itself
    print(f"🎤 Input Level: {int(volume_norm):<4} [{bar:<50}]", end='\r')


def run_diagnostic():
    """
    Main diagnostic function to test microphone input.
    """
    print("--- zia-X Microphone Diagnostic ---")
    try:
        print(f"\nAvailable audio devices:\n{sd.query_devices()}")
        default_device = sd.default.device
        print(f"\nDefault Input Device: {default_device}")
        
        # Get details of the default input device
        device_info = sd.query_devices(default_device[0], 'input')
        samplerate = device_info['default_samplerate']
        channels = 1 # Mono
        
        print(f"Using samplerate: {samplerate} Hz")
        print("\nStarting audio stream... Please talk into your microphone.")
        print("You should see the input level change as you speak.")
        print("Press Ctrl+C to stop the test.")
        
        # Open a stream to listen to the microphone
        with sd.InputStream(samplerate=samplerate, channels=channels, callback=print_sound_level):
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n--- Diagnostic Test Finished ---")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("This might mean the wrong microphone is selected or there's a driver issue.")

if __name__ == "__main__":
    run_diagnostic()