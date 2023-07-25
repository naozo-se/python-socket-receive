import socket

# from concurrent.futures import ProcessPoolExecutor, Future, as_completed
from multiprocessing import Process, Semaphore
import time

# 受信IP
RCV_HOST = "0.0.0.0"
# 受信ポート
RCV_PORT = 50000
# 受信可能数（指定以上超えると、待ちが発生せずに処理終了？？）
BACKLOG = 10
# 一度の通信受信できる最大データバイト数
BUFSIZE = 1024
# 最大同時処理数
MAXWORKER = 10
# プロセス格納
procs = dict()
procs_ids = []


# 受信～返信処理
def data_comminicate(conn):
    while True:
        try:
            # 通信を受信
            rcv_msg = conn.recv(BUFSIZE)
            # 内容がないときは、処理をしない
            if not rcv_msg:
                break
            # 受信内容の確認
            print("rcv_msg:", rcv_msg)

            # 多重化しているかの確認(ここに受信データを使った処理を記載)
            print("before sleep:", rcv_msg)
            time.sleep(5)
            print("after sleep:", rcv_msg)

            # 返信処理
            conn.send(b":Received - " + rcv_msg)

        except Exception as e:
            break
        finally:
            conn.close()
            return True


def zonbie_process_kill():
    # キャンセル
    del_ids = []

    for key_id in procs_ids:
        if key_id in procs and not procs[key_id].is_alive():
            proc = procs.pop(key_id)
            proc.kill()
            del_ids.append(key_id)

    for key_id in del_ids:
        del_ids.remove(key_id)


if __name__ == "__main__":
    try:
        # ソケット定義
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 再使用設定(３つ目の引数は違う可能性あり)
        sct.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, BACKLOG)
        # 受信設定
        sct.bind((RCV_HOST, RCV_PORT))
        sct.listen(BACKLOG)

        # マルチプロセスで実行
        # with Process(MAXWORKER) as executor:

        semaphore = Semaphore(MAXWORKER)
        semaphore.acquire(block=False)

        # 継続受信のため、ループ
        while True:
            try:
                print("start 1")

                # zonbie_process_kill()

                # コネクション定義(切断処理の判定対策)
                conn = None
                # 受信の待機
                (conn, addr) = sct.accept()

                proc = Process(target=data_comminicate, args=(conn,))
                key_id = proc.authkey
                # print("key_id", key_id)

                procs[key_id] = proc
                procs_ids.append(key_id)

                # マルチプロセスで データ受信～返信を実行
                proc.start()

                # proc = executor.map(data_comminicate, [conn], timeout=1.0)
                # proc.add_done_callback(temp_call_back)

            except KeyboardInterrupt as e:
                # キーボード(ctrl+c等)で抜けたとき
                print("KeyboardInterrupt", e)
            finally:
                # 受信せずに終わる場合(ctrl+c等)は、処理を抜けさせる
                if conn is None:
                    break

    except Exception as e:
        # socketオブジェクトの定義ミス
        print("socket variable error", e)
    finally:
        # socketオブジェクト終了
        sct.close()
