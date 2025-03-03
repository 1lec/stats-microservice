import zmq
import numpy as np
import pandas as pd


ZMQ_PORT = '5558'

def decimal_to_percent(decimal):
    """Receives a decimal representing a proportion and converts it to a percentage with up to 2 decimal places."""
    return round(decimal * 100, 2)

class DataAnalyzer:
    """Receives requests via ZMQ and performs data manipulations based on the request."""
    def __init__(self):
        self.socket = self.zmq_connect(ZMQ_PORT)

    def zmq_connect(self, port):
        """Receives a port and establishes a ZeroMQ connection via that port."""
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{port}")
        return socket
    
    def calculate_winning_percentage(self, dataframe):
        """Receives a DataFrame of game results for a player, and, using the Results column, calculates the winning percentage of
        that player."""
        decimal_value = dataframe["Results"].mean()      # from 0 to 1 with variable decimal places
        win_percent = decimal_to_percent(decimal_value)  # from 0.00 to 100.00 with up to 2 decimal places
        self.socket.send_json({"win-percent": win_percent})

    def create_leaderboard(self, dataframe):
        """Receives a Dataframe of game results for all players and creates a list of lists of name and winning percentage
        sorted by winning percentage."""
        # Groups all results by Name, calculates the winning percentage for each, and takes the top 10 in descending order
        decimals = dataframe.groupby("Name")[["Results"]].mean()
        sorted_decimals = decimals.sort_values(by="Results", ascending=False)
        sorted_top_10_percents = sorted_decimals[["Results"]].apply(decimal_to_percent).head(10)

        # Creates a JSON-safe list of lists from the above dataframe
        top_10_json = []
        for name, percent in sorted_top_10_percents.iterrows():
            top_10_json.append([name, percent["Results"]])

        self.socket.send_json({"leaderboard": top_10_json})
    
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