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
        decimal_value = dataframe["Results"].mean()  # from 0 to 1 with variable decimal places
        win_percent = round(decimal_value * 100, 2)  # from 0.00 to 100.00 with up to 2 decimal places
        self.socket.send_json({"win-percent": win_percent})

    def create_leaderboard(self, dataframe):
        """Receives a Dataframe of game results for all players, and returns a list of the top 10 names by winning percentage in
        descending order."""
        pass
    
    def listen(self):
        """Listens for client requests."""
        while True:
            request = self.socket.recv_json()
            request_type = request["type"]

            if request_type == "win-percent":
                df = pd.DataFrame(request["results"], columns = ["Name", "Results"])
                self.calculate_winning_percentage(df)
            if request_type == "leaderboard":
                df = pd.DataFrame(request["results"], columns = ["Name", "Results"])
                self.create_leaderboard(df)

def main():
    da = DataAnalyzer()
    da.listen()

if __name__ == "__main__":
    main()