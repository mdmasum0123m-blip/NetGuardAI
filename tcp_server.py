import socket

HOST = "127.0.0.1"
PORT = 5000

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)

        print("NetGuard AI - TCP Server Started")
        print(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()

            with conn:
                print(f"Client connected: {addr}")

                while True:
                    data = conn.recv(4096)

                    if not data:
                        break

                    conn.sendall(data)

if __name__ == "__main__":
    start_tcp_server()
