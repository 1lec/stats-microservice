import zmq
import numpy as np
import pandas as pd


ZMQ_PORT = '5558'


class DataAnalyzer:
    def __init__(self):
        self.socket = self.zmq_connect(ZMQ_PORT)

    def zmq_connect(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{port}")
        return socket
    
    def listen(self):
        request = self.socket.recv_string()
        print(request)
        self.socket.send_string("Request received!")

def main():
    da = DataAnalyzer()
    da.listen()

if __name__ == "__main__":
    main()