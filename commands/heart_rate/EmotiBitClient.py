'''
@author Alessia Bussard
@description Client-side EmotiBit heart rate processor for battleship game
'''

import threading
import time
import numpy as np
import pickle
import socket
from scipy import signal
from pythonosc import dispatcher
from pythonosc import osc_server
from PyQt5.QtCore import QObject, pyqtSignal

# Import socket connection and heart rate request
from commands.heart_rate.HeartRateRequest import HeartRateRequest
from model.socket.SocketConnection import SocketConnection
from model.socket.SocketData import SocketData


class EmotiBitClient(QObject):
    """
    Client-side processor for EmotiBit data.
    Simply processes and provides the current heart rate.
    """
    # PyQt signal for heart rate updates
    heart_rate_updated = pyqtSignal(float)
    # Add a new signal for opponent heart rate updates
    opponent_heart_rate_updated = pyqtSignal(str, float)

    # Singleton instance
    _instance = None

    @staticmethod
    def get_instance(socket_data=None):
        """Get or create the singleton instance."""
        if EmotiBitClient._instance is None:
            EmotiBitClient._instance = EmotiBitClient(socket_data)
        elif socket_data is not None:
            # Update socket data if provided
            EmotiBitClient._instance.socket_data = socket_data
            EmotiBitClient._instance._initialized = True
        return EmotiBitClient._instance

    def __init__(self, socket_data=None):
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

        if socket_data is not None:
            self.socket_data = socket_data
        else:
            self.socket_data = SocketData()

        # Create socket connection for sending data to server
        self.socket_data = SocketData()
        self.socket_connection = None
        self.last_sent_hr = 0
        self.hr_threshold = 1.0  # Only send updates when HR changes by this amount
        self.use_mock_hr = True  # Set to False to use real PPG

        print("EmotiBit client processor initialized")

    def start(self):
        """Start the EmotiBit processor."""
        if self.running:
            return

        self.running = True

        # First connect to heart rate server
        try:
            self.hr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.hr_socket.connect((self.socket_data.get_ip_address(), 8081))  # HR server port

            # Send player ID to identify this connection
            player_id = "YOUR_PLAYER_ID"  # You need to get this from your game
            self.hr_socket.send(pickle.dumps(player_id))

            # Start a thread to listen for opponent heart rate updates
            threading.Thread(target=self.listen_for_opponent_hr, daemon=True).start()

            print("Connected to heart rate server")
        except Exception as e:
            print(f"Error connecting to heart rate server: {e}")
            self.hr_socket = None

        # Then initialize the game socket connection
        if self.socket_data._initialized and self.socket_data.get_ip_address() and self.socket_data.get_port():
            try:
                self.socket_connection = SocketConnection(
                    self.socket_data.get_ip_address(),
                    self.socket_data.get_port()
                )
                self.socket_connection.connect()
                print("Connected to game server")
            except Exception as e:
                print(f"Error connecting to game server: {e}")
                self.socket_connection = None

        # Start the heart rate generation as before
        if self.use_mock_hr:
            self.hr_calc_thread = threading.Thread(target=self.mock_heart_rate_loop)
            self.hr_calc_thread.daemon = True
            self.hr_calc_thread.start()

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

        while self.running:
            mock_hr = random.uniform(60, 100)  # Simulate HR between 60-100 BPM

            self.latest_hr = mock_hr
            print(f"[MOCK] Current heart rate: {mock_hr:.1f} BPM")

            self.heart_rate_updated.emit(mock_hr)

            if self.socket_connection and abs(mock_hr - self.last_sent_hr) >= self.hr_threshold:
                self.send_heart_rate_to_server(mock_hr)
                self.last_sent_hr = mock_hr

            time.sleep(1.0)  # Simulate real-time update every second

    def calculate_heart_rate(self):
        """Calculate heart rate from PPG data."""
        min_data_points = self.sampling_rate * 4  # At least 4 seconds of data

        while self.running:
            # Check if we have enough data
            if len(self.ppg_green_buffer) >= min_data_points:
                try:
                    # Get the signal as numpy array
                    green_signal = np.array(self.ppg_green_buffer[-min_data_points:])

                    # Normalize the signal
                    green_signal = (green_signal - np.mean(green_signal)) / np.std(green_signal)

                    # Apply bandpass filter (0.5-3.5 Hz = 30-210 BPM)
                    b, a = signal.butter(3, [0.5 / (self.sampling_rate / 2), 3.5 / (self.sampling_rate / 2)],
                                         btype='band')
                    filtered_green = signal.filtfilt(b, a, green_signal)

                    # Find peaks in the filtered signal
                    peaks, _ = signal.find_peaks(filtered_green, distance=int(self.sampling_rate * 0.5))

                    if len(peaks) >= 2:
                        # Calculate heart rate from peak intervals
                        peak_intervals = np.diff(peaks)
                        mean_interval = np.mean(peak_intervals)

                        # Convert to beats per minute
                        hr_bpm = 60 * self.sampling_rate / mean_interval

                        # Sanity check - HR should be between 40-180 BPM for most adults
                        if 40 <= hr_bpm <= 180:
                            self.latest_hr = hr_bpm
                            print(f"Current heart rate: {hr_bpm:.1f} BPM")

                            # Emit the heart rate update signal
                            self.heart_rate_updated.emit(hr_bpm)

                            # Send heart rate to server if connection exists and value changed significantly
                            if self.socket_connection and abs(hr_bpm - self.last_sent_hr) >= self.hr_threshold:
                                self.send_heart_rate_to_server(hr_bpm)
                                self.last_sent_hr = hr_bpm
                except Exception as e:
                    print(f"Error calculating heart rate: {e}")

            # Sleep to avoid using too much CPU
            time.sleep(0.5)

    def get_current_heart_rate(self):
        """Get the most recently calculated heart rate."""
        return self.latest_hr

    def listen_for_opponent_hr(self):
        """Listen for heart rate updates from opponents"""
        while self.running and self.hr_socket:
            try:
                data = self.hr_socket.recv(1024)
                if not data:
                    break

                hr_update = pickle.loads(data)

                if isinstance(hr_update, dict) and "player_id" in hr_update and "heart_rate" in hr_update:
                    opponent_id = hr_update["player_id"]
                    opponent_hr = hr_update["heart_rate"]

                    print(f"Opponent {opponent_id} heart rate: {opponent_hr} BPM")

                    # Emit a signal that the UI can listen for
                    self.opponent_heart_rate_updated.emit(opponent_id, opponent_hr)

                elif isinstance(hr_update, str):
                    # Regular confirmation message
                    print(f"Heart rate server: {hr_update}")
                else:
                    print(f"Unknown message format: {hr_update}")

            except Exception as e:
                print(f"Error receiving opponent heart rate: {e}")
                import traceback
                traceback.print_exc()


    def send_heart_rate_to_server(self, heart_rate):
        """Send heart rate to the server"""
        try:
            if self.hr_socket:
                # Create heart rate request
                request = HeartRateRequest(heart_rate)

                # Serialize and send
                serialized = pickle.dumps(request)
                self.hr_socket.send(serialized)

                # Get response
                response = self.hr_socket.recv(1024)
                response_data = pickle.loads(response)

                print(f"Sent heart rate ({heart_rate:.1f} BPM) to server. Response: {response_data}")

                # Emit signal for UI update
                self.heart_rate_updated.emit(heart_rate)
            else:
                print("Cannot send heart rate: No heart rate server connection")
        except Exception as e:
            print(f"Error sending heart rate to server: {e}")