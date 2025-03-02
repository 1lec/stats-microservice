import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")

    socket.send_string("Message from client!")
    response = socket.recv_string()
    print(response)

if __name__ == "__main__":
    main()