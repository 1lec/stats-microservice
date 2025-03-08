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
        print(f"Stats Microservice is running and is listening on port {port}...")
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
        completed_dataframe = self.reassign_indices(sorted_top_10_percents)

        top_10_json = completed_dataframe.to_json()
        self.socket.send_json(top_10_json)

    def reassign_indices(self, df):
        """Receives a DataFrame with Names as indices and a single column of winning percentages and
        returns a new DataFrame with places (1st, 2nd, 3rd, etc.) as indices and Name and Winning
        Percentage as columns."""
        df = df.rename(columns={"Results": "Winning Percentage"})
        df = df.reset_index()
        places = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        row_count = len(df)
        df.index = places[:row_count]

        return df

    
    def listen(self):
        """Listens for client requests."""
        while True:
            request = self.socket.recv_json()
            print("Request received:", request)
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