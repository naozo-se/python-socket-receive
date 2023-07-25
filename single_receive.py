import socket

# 受信IP
RCV_HOST = "0.0.0.0"
# 受信ポート
RCV_PORT = 50000
# 受信可能数（指定以上超えると、待ちが発生せずに処理終了？？）
BACKLOG = 10
# 一度の通信受信できる最大データバイト数
BUFSIZE = 1024

if __name__ == "__main__":

    try:
        # ソケット定義
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 再使用設定(３つ目の引数は違う可能性あり)
        sct.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, BACKLOG)
        # 受信設定
        sct.bind((RCV_HOST, RCV_PORT))
        sct.listen(BACKLOG)

        # 継続受信のため、ループ
        while True:
            # コネクション定義(切断処理の判定対策)
            conn = None
            try:
                # 受信の待機
                (conn, addr) = sct.accept()

                # 通信を受信
                rcv_msg = conn.recv(BUFSIZE)
                # 受信内容の確認
                print("rcv_msg:", rcv_msg)
                # 送信側に値を返す
                conn.send(b"recived:" + rcv_msg)

            finally:
                # 受信せずに終わる場合(ctrl+z等)は、処理を抜けさせる
                if conn is None:
                    break
                # コネクションを閉じる
                conn.close()

    finally:
        # ソケットを閉じる
        sct.close()
