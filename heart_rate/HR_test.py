from EmotiBitClient import EmotiBitClient
import time
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Get the singleton instance
    client = EmotiBitClient.get_instance()

    # Set to use real data instead of mock data
    client.use_mock_hr = False

    # Start the client
    print("Starting EmotiBit client...")
    client.start()
    print("Client started. Running status:", client.running)

    # Keep the script running and monitor the status
    try:
        last_buffer_size = 0
        buffer_stuck_count = 0

        while True:
            # Check heart rate and buffer
            current_hr = client.get_current_heart_rate()
            buffer_size = len(client.ppg_green_buffer)

            # Check if buffer is growing
            if buffer_size == last_buffer_size and buffer_size > 0:
                buffer_stuck_count += 1
                if buffer_stuck_count % 10 == 0:  # Every 20 seconds
                    print(f"WARNING: Buffer has been stuck at {buffer_size} for {buffer_stuck_count * 2} seconds")
            else:
                buffer_stuck_count = 0

            last_buffer_size = buffer_size

            print(f"Current heart rate: {current_hr:.1f} BPM, PPG buffer size: {buffer_size}")

            # If we have a reasonable amount of data, let's analyze the signal
            if buffer_size >= 100 and buffer_size % 50 == 0:  # Every 2 seconds after reaching 100 points
                print("\nAnalyzing signal...")
                signal_data = np.array(client.ppg_green_buffer[-100:])

                # Basic signal analysis
                print(
                    f"Signal stats - Min: {np.min(signal_data):.2f}, Max: {np.max(signal_data):.2f}, Mean: {np.mean(signal_data):.2f}, Std: {np.std(signal_data):.2f}")

                # Check if the signal has variation (not flat or stuck)
                if np.std(signal_data) < 0.001:
                    print("WARNING: Signal has very low variation, possibly stuck or flat")

                # Try manual heart rate calculation
                if len(signal_data) >= 100:
                    try:
                        # Normalize
                        norm_signal = (signal_data - np.mean(signal_data)) / np.std(signal_data)

                        # Apply bandpass filter
                        from scipy import signal as sig

                        b, a = sig.butter(3, [0.5 / (25 / 2), 3.5 / (25 / 2)], btype='band')
                        filtered = sig.filtfilt(b, a, norm_signal)

                        # Find peaks
                        peaks, _ = sig.find_peaks(filtered, distance=int(25 * 0.5))

                        print(f"Found {len(peaks)} peaks in filtered signal")

                        if len(peaks) >= 2:
                            # Calculate heart rate
                            peak_intervals = np.diff(peaks)
                            mean_interval = np.mean(peak_intervals)
                            hr_bpm = 60 * 25 / mean_interval
                            print(f"Manual HR calculation: {hr_bpm:.1f} BPM")
                    except Exception as e:
                        print(f"Error in manual HR calculation: {e}")

                print("Signal analysis complete\n")

            time.sleep(2)
    except KeyboardInterrupt:
        # Stop the client when you press Ctrl+C
        print("\nStopping EmotiBit client...")
        client.stop()
        print("Client stopped. Test finished.")