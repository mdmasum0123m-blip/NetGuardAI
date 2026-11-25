import socket
import time

HOST = "127.0.0.1"
PORT = 5001

def test_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(3)

        message = b"Hello from NetGuard AI UDP"

        start = time.perf_counter()

        client.sendto(message, (HOST, PORT))

        try:
            data, addr = client.recvfrom(4096)

            end = time.perf_counter()
            latency = (end - start) * 1000

            print("UDP Communication Successful!")
            print("Sent:", message.decode())
            print("Received:", data.decode())
            print(f"Latency: {latency:.2f} ms")

        except socket.timeout:
            print("UDP Timeout: No response received")

if __name__ == "__main__":
    test_udp()