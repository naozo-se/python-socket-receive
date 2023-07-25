import socket
from concurrent.futures import ProcessPoolExecutor


# 受信IP
RCV_HOST = "0.0.0.0"
# 受信ポート
RCV_PORT = 50000
# 受信可能数（指定以上超えると、待ちが発生せずに処理終了？？）
BACKLOG = 10
# 一度の通信受信できる最大データバイト数
BUFSIZE = 1024


def handle_connection(conn):
    while True:
        data = conn.recv(BACKLOG)
        if not data:
            break
        conn.send(b":OK" + data)
    conn.close()


def serve_forever(sock):
    with ProcessPoolExecutor() as executor:
        while True:
            conn, addr = sock.accept()
            executor.submit(handle_connection, conn)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((RCV_HOST, RCV_PORT))
    sock.listen(BACKLOG)
    serve_forever(sock)
