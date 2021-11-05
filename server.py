from threading import Thread
import sys
import signal
from scripts.log_output import LogOutput, log_output
from scripts.server_p import ServerP
from scripts.server_socket import server_socket
from server_config import MESSAGE_SIZE

separator_token = "<SEP>"  # we will use this to separate the client name & message
client_sockets = None

server_p = None


def set_up():
    global log_output
    global server_p

    print("# Set up")
    log_output.set_up()

    server_p = ServerP()


def clean_up():
    global server_socket
    global client_sockets

    # close client sockets
    print("Clean up")
    if not (client_sockets is None):
        for cs in client_sockets:
            cs.close()

    # close server socket
    server_socket.clean_up()


def listen_for_client(client_sock):
    """
    This function keep listening for a message from `client_sock` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    global separator_token
    global client_sockets

    while True:
        try:
            # keep listening for a message from `client_sock` socket
            line = client_sock.recv(MESSAGE_SIZE).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")

            print(f"Remove a socket")
            client_sockets.remove(client_sock)
            break

        # 処理は server_p に委譲します
        server_p.listen_line(line)

        # とりあえずエコー
        send_line(client_sock, line)


def send_line(client_sock, line):
    client_sock.send(line.encode())

    s = LogOutput.format_send(line)

    # Display
    print(s)

    # Log
    log_output.write(s)
    log_output.flush()


def run_server():
    global server_socket
    global client_sockets

    # initialize list/set of all connected client's sockets
    client_sockets = set()

    server_socket.set_up()

    while True:
        print(f"Wait a connection")
        # we keep listening for new connections all the time
        client_socket, client_address = server_socket.accept()
        print(f"[+] {client_address} connected.")

        # add the new connected client to connected sockets
        client_sockets.add(client_socket)

        # start a new thread that listens for each client's messages
        thr = Thread(target=listen_for_client, args=(client_socket,))

        # make the thread daemon so it ends whenever the main thread ends
        thr.daemon = True

        # start the thread
        thr.start()


def main():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)
    set_up()

    try:
        run_server()
    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    sys.exit(main())
