import socket
import time

HOST = "127.0.0.1"
PORT = 5000

def test_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        client.connect((HOST, PORT))

        message = b"Hello from NetGuard AI"

        start = time.perf_counter()

        client.sendall(message)

        data = b""
        while len(data) < len(message):
            chunk = client.recv(4096)
            if not chunk:
                raise ConnectionError("Server disconnected")
            data += chunk

        end = time.perf_counter()
        latency = (end - start) * 1000

        print("TCP Connection Successful!")
        print("Sent:", message.decode())
        print("Received:", data.decode())
        print(f"Latency: {latency:.2f} ms")

if __name__ == "__main__":
    test_tcp()