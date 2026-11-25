import socket

HOST = "127.0.0.1"
PORT = 5001

def start_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))

        print("NetGuard AI - UDP Server Started")
        print(f"Listening on {HOST}:{PORT}")

        while True:
            data, addr = server.recvfrom(4096)

            print(f"Packet received from {addr}")
            print("Message:", data.decode(errors="replace"))

            server.sendto(data, addr)

if __name__ == "__main__":
    start_udp_server()