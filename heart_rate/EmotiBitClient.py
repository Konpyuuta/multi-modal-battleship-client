'''
@author Alessia Bussard
@description Client-side EmotiBit heart rate processor for battleship game
'''

import threading
import time
import numpy as np
from scipy import signal
from pythonosc import dispatcher
from pythonosc import osc_server
from PyQt5.QtCore import QObject, pyqtSignal

# from commands.speech.StartSpeechModuleCommand import StartSpeechModuleCommand
# Import socket connection and heart rate request

from heart_rate.HeartRate import HeartRate
# from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData


class EmotiBitClient(QObject):
    """
    Client-side processor for EmotiBit data.
    Simply processes and provides the current heart rate.
    """
    # PyQt signal for heart rate updates
    heart_rate_updated = pyqtSignal(float)

    # Singleton instance
    _instance = None

    @staticmethod
    def get_instance():
        """Get or create the singleton instance."""
        if EmotiBitClient._instance is None:
            EmotiBitClient._instance = EmotiBitClient()
        return EmotiBitClient._instance

    def __init__(self):
        """Initialize the EmotiBit processor."""
        super().__init__()

        # Ensure this is only initialized once
        if EmotiBitClient._instance is not None:
            raise Exception("This class is a singleton. Use get_instance() instead.")

        # Data processing variables
        self.ppg_green_buffer = []
        self.ppg_timestamps = []
        self.latest_hr = 0
        self.sampling_rate = 25  # From EmotiBit config
        self.buffer_duration = 5  # Seconds of data to keep
        self.buffer_size = int(self.sampling_rate * self.buffer_duration)

        # Thread control
        self.running = False
        self.osc_server = None
        self.hr_calc_thread = None
        self.server_thread = None

        # OSC server settings
        self.ip = "0.0.0.0"  # Listen on all interfaces
        self.port = 12345  # EmotiBit OSC port

        # Initialize the dispatcher
        self.disp = dispatcher.Dispatcher()
        self.disp.map("/EmotiBit/0/PPG:GRN", self.ppg_green_handler)
        self.disp.set_default_handler(self.default_handler)

        # Create socket connection for sending data to server
        self.socket_data = SocketData()
        self.socket_connection = None
        self.last_sent_hr = 0
        self.hr_threshold = 1.0  # Only send updates when HR changes by this amount
        self.use_mock_hr = False  # Set to False to use real PPG

        print("EmotiBit client processor initialized")

    def start(self):
        self.running = True
        # Start the correct heart rate calculation method
        self.use_mock_hr = False
        if self.use_mock_hr:
            self.hr_calc_thread = threading.Thread(target=self.mock_heart_rate_loop)
            self.hr_calc_thread.daemon = True
            self.hr_calc_thread.start()
            #self.t = threading.Thread(target=StartSpeechModuleCommand().execute())
            #self.t.daemon = True
            #self.t.start()
        else:
            self.hr_calc_thread = threading.Thread(target=self.calculate_heart_rate)
            self.hr_calc_thread.daemon = True
            self.hr_calc_thread.start()

            # Start the OSC server in a separate thread
            self.server_thread = threading.Thread(target=self.run_osc_server)
            self.server_thread.daemon = True
            self.server_thread.start()

        print(f"EmotiBit client processor started on {self.ip}:{self.port}")

    def stop(self):
        """Stop the EmotiBit processor."""
        if not self.running:
            return

        self.running = False

        if self.osc_server:
            self.osc_server.shutdown()

        print("EmotiBit client processor stopped")

    def run_osc_server(self):
        """Run the OSC server to receive EmotiBit data."""
        try:
            self.osc_server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.disp)
            print(f"Listening for EmotiBit OSC data on {self.ip}:{self.port}")
            self.osc_server.serve_forever()
        except Exception as e:
            print(f"Error in OSC server: {e}")
            if self.running:
                # Try to restart the server after a delay
                time.sleep(5)
                if self.running:
                    self.run_osc_server()

    def ppg_green_handler(self, address, *args):
        """Handle incoming green PPG data."""
        if args and len(args) > 0:
            self.ppg_green_buffer.append(args[0])
            # print(f"Received PPG green data: {args[0]}")
            self.ppg_timestamps.append(time.time())

            # Keep buffer at defined size
            if len(self.ppg_green_buffer) > self.buffer_size:
                self.ppg_green_buffer = self.ppg_green_buffer[-self.buffer_size:]
                self.ppg_timestamps = self.ppg_timestamps[-self.buffer_size:]

    def default_handler(self, address, *args):
        """Default handler for other OSC messages."""
        # We don't need to handle other messages for this simple implementation
        pass

    def mock_heart_rate_loop(self):
        """Mock heart rate generator for testing."""
        import random

        while True:
            mock_hr = random.uniform(60, 100)  # Simulate HR between 60-100 BPM

            self.latest_hr = mock_hr
            HeartRate().set_heart_rate(mock_hr)
            #self.heart_rate_updated.emit(mock_hr)

            '''if self.socket_connection and abs(mock_hr - self.last_sent_hr) >= self.hr_threshold:
                self.send_heart_rate_to_server(mock_hr)
                self.last_sent_hr = mock_hr'''

            time.sleep(1.0)  # Simulate real-time update every second

    def calculate_heart_rate(self):
        """Calculate heart rate from PPG data."""
        min_data_points = 100  # At least 4 seconds of data
        print('the calculate heart rate function is called')

        while self.running:
            # Check if we have enough data
            if len(self.ppg_green_buffer) >= min_data_points:
                try:
                    # Get the signal as numpy array
                    green_signal = np.array(self.ppg_green_buffer[-min_data_points:])
                    # print(f"Signal min: {np.min(green_signal)}, max: {np.max(green_signal)}, mean: {np.mean(green_signal)}")

                    # Normalize the signal
                    green_signal = (green_signal - np.mean(green_signal)) / np.std(green_signal)

                    # Apply bandpass filter (0.5-3.5 Hz = 30-210 BPM)
                    b, a = signal.butter(3, [0.5 / (self.sampling_rate / 2), 3.5 / (self.sampling_rate / 2)],
                                         btype='band')
                    filtered_green = signal.filtfilt(b, a, green_signal)

                    # Find peaks in the filtered signal
                    peaks, _ = signal.find_peaks(filtered_green, distance=int(self.sampling_rate * 0.5))
                    # print(f"Found {len(peaks)} peaks in the signal")

                    if len(peaks) >= 2:
                        # Calculate heart rate from peak intervals
                        peak_intervals = np.diff(peaks)
                        mean_interval = np.mean(peak_intervals)

                        # Convert to beats per minute
                        hr_bpm = 60 * self.sampling_rate / mean_interval
                        # print(f"Calculated HR: {hr_bpm:.1f} BPM")

                        # Sanity check - HR should be between 40-180 BPM for most adults
                        if 40 <= hr_bpm <= 180:
                            self.latest_hr = hr_bpm
                            HeartRate().set_heart_rate(hr_bpm)
                            # print(f"Current heart rate: {hr_bpm:.1f} BPM")
                        # else:
                            # print(f"Calculated HR {hr_bpm:.1f} BPM out of valid range (40-180 BPM)")

                            # # Emit the heart rate update signal
                            # self.heart_rate_updated.emit(hr_bpm)
                            #
                            # # Send heart rate to server if connection exists and value changed significantly
                            # if self.socket_connection and abs(hr_bpm - self.last_sent_hr) >= self.hr_threshold:
                            #     self.send_heart_rate_to_server(hr_bpm)
                            #     self.last_sent_hr = hr_bpm
                except Exception as e:
                    print(f"Error calculating heart rate: {e}")

            # Sleep to avoid using too much CPU
            time.sleep(0.5)

    def get_current_heart_rate(self):
        """Get the most recently calculated heart rate."""
        return self.latest_hr

    def send_heart_rate_to_server(self, heart_rate):
        """
        Send the current heart rate to the game server

        Args:
            heart_rate (float): The current heart rate in BPM
        """
        try:
            if self.socket_connection:
                pass
                # Create heart rate request
                #request = HeartRateRequest(heart_rate)

                # Send request to server
                #response = self.socket_connection.send_request(request)

                # Log success
                #print(f"Sent heart rate ({heart_rate:.1f} BPM) to server. Response: {response}")
                #print(f"Sent heart rate ({heart_rate:.1f} BPM) to server. Response: {response}")
            else:
                print("Cannot send heart rate: No server connection")
        except Exception as e:
            print(f"Error sending heart rate to server: {e}")


