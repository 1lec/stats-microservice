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
    
    def calculate_winning_percentage(self, dataframe):
        """Receives a DataFrame of game results for a player, and, using the Results column, calculates the winning percentage of that player."""
        decimal_value = dataframe.describe().loc[["mean"]].values[0][0]  # from 0 to 1 with variable decimal places
        win_percent = round(decimal_value * 100, 2)  # from 0.00 to 100.00 with up to 2 decimal places
        self.socket.send_json({"win-percent": win_percent})
    
    def listen(self):
        """Listens for client requests."""
        while True:
            request = self.socket.recv_json()
            request_type = request["type"]

            if request_type == "win-percent":
                df = pd.DataFrame(request["results"], columns = ["Name", "Results"])
                self.calculate_winning_percentage(df)
            if request_type == "leaderboard":
                self.socket.send_string("Received request for a leaderboard")

def main():
    da = DataAnalyzer()
    da.listen()

if __name__ == "__main__":
    main()