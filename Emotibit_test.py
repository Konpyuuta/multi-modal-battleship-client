'''
EmotiBit Test Script
-------------------
A simple script to test that the EmotiBitClient is properly
receiving and processing data from an EmotiBit device.

Usage:
    python EmotiBitTest.py

This script will initialize the EmotiBitClient, start it,
and continuously print heart rate values to the console.
Press Ctrl+C to exit.
'''

import time
import signal
import sys
from EmotiBitClient import EmotiBitClient

# Flag to control the main loop
running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C to exit gracefully"""
    global running
    print("\nStopping EmotiBit test...")
    running = False


# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def main():
    print("Starting EmotiBit Test Script")
    print("-----------------------------")
    print("This script will monitor heart rate data from the EmotiBit device.")
    print("Press Ctrl+C to exit.")
    print()

    # Initialize the EmotiBit client
    print("Initializing EmotiBitClient...")
    emotibit = EmotiBitClient.get_instance()

    # Define a callback for heart rate updates
    def heart_rate_callback(hr):
        print(f"[{time.strftime('%H:%M:%S')}] Heart Rate: {hr:.1f} BPM")

    # Connect the callback
    emotibit.heart_rate_updated.connect(heart_rate_callback)

    # Start the EmotiBit client
    print(f"Starting EmotiBit client on port {emotibit.port}...")
    emotibit.start()

    print("\nWaiting for data...")
    print("If you don't see any data within 30 seconds, check that:")
    print("1. Your EmotiBit device is powered on and recording")
    print("2. The OSC settings in EmotiBit are configured correctly")
    print("3. The correct IP address and port are being used")
    print("4. There are no firewall issues blocking the connection")

    # Main loop to keep the script running
    last_hr = 0
    no_data_count = 0

    while running:
        # Check if we're getting data
        current_hr = emotibit.get_current_heart_rate()

        # If no heart rate data for a while, provide more feedback
        if current_hr == 0 and last_hr == 0:
            no_data_count += 1
            if no_data_count % 5 == 0:  # Every ~5 seconds
                print(f"No heart rate data received yet... (waiting {no_data_count * 1} seconds)")
                print(f"Buffer size: {len(emotibit.ppg_green_buffer)} samples")
        else:
            no_data_count = 0

        last_hr = current_hr
        time.sleep(1)

    # Clean up
    print("Stopping EmotiBit client...")
    emotibit.stop()
    print("Test complete.")


if __name__ == "__main__":
    main()