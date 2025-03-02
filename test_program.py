import zmq


ZMQ_PORT = '5558'


class StatsTester:
    def __init__(self):
        self.socket = self.zmq_connect(ZMQ_PORT)

    def zmq_connect(self, port):
        """Receives a port and establishes a ZeroMQ connection via that port."""
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://localhost:{port}")
        return socket
    
    def request_winning_percentage(self, name, results):
        """Receives a name of a player and their collection of results and sends a request for the winning percentage of that player."""
        request = {"type": "win-percent", "name": name, "results": results}
        self.socket.send_json(request)
        response = self.socket.recv().decode()
        print(response)

    def request_leaderboard(self, results):
        """Receives a collection of results and sends a request for a leaderboard."""
        request = {"type": "leaderboard", "results": results}
        self.socket.send_json(request)
        response = self.socket.recv().decode()
        print(response)
    
    def run(self):
        """Sends requests to the stats_microservice."""
        pass


def main():
    st = StatsTester()
    st.run()

if __name__ == "__main__":
    main()