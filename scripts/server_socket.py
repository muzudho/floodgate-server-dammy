import socket

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002  # port we want to use


class ServerSocket():

    def __init__(self):
        self._srv_sock = None

    def set_up(self):
        # create a TCP socket
        self._srv_sock = socket.socket()

        # make the port as reusable port
        self._srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to the address we specified
        self._srv_sock.bind((SERVER_HOST, SERVER_PORT))

        # listen for upcoming connections
        self._srv_sock.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    def clean_up(self):
        if not (self._srv_sock is None):
            self._srv_sock.close()

    def accept(self):
        return self._srv_sock.accept()


server_socket = ServerSocket()
