import zmq
import numpy as np
import pandas as pd


ZMQ_PORT = '5558'


class DataAnalyzer:
    def __init__(self):
        self.socket = self.zmq_connect(ZMQ_PORT)

    def zmq_connect(self, port):
        """Receives a port and establishes a ZeroMQ connection via that port."""
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{port}")
        return socket
    
    def listen(self):
        """Listens for client requests."""
        while True:
            request = self.socket.recv_json()
            request_type = request["type"]

            if request_type == "win-percent":
                self.socket.send_string("Received request for a win percentage.")
            if request_type == "leaderboard":
                self.socket.send_string("Received request for a leaderboard")

def main():
    da = DataAnalyzer()
    da.listen()

if __name__ == "__main__":
    main()