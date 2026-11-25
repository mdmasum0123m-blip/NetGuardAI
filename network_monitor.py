import socket
import time
import statistics

HOST = "127.0.0.1"
TCP_PORT = 5000
UDP_PORT = 5001


def monitor_network(protocol, count=10):

    protocol = protocol.upper()

    if protocol not in ("TCP", "UDP"):
        raise ValueError("Invalid protocol")

    latencies = []
    lost_packets = 0

    for i in range(count):

        message = f"NetGuard Packet {i + 1}".encode()

        try:

            if protocol == "TCP":

                with socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                ) as client:

                    client.settimeout(2)
                    client.connect((HOST, TCP_PORT))

                    start = time.perf_counter()

                    client.sendall(message)

                    data = b""

                    while len(data) < len(message):
                        chunk = client.recv(4096)

                        if not chunk:
                            break

                        data += chunk

                    end = time.perf_counter()

            else:

                with socket.socket(
                    socket.AF_INET,
                    socket.SOCK_DGRAM
                ) as client:

                    client.settimeout(2)

                    start = time.perf_counter()

                    client.sendto(
                        message, (HOST, UDP_PORT)
                    )

                    data, addr = client.recvfrom(4096)

                    end = time.perf_counter()

            if data == message:

                latency = (end - start) * 1000
                latencies.append(latency)

            else:

                lost_packets += 1

        except OSError:

            lost_packets += 1

        time.sleep(0.1)

    received_packets = len(latencies)

    packet_loss = (lost_packets / count) * 100

    average_latency = (
        statistics.mean(latencies)
        if latencies else None
    )

    minimum_latency = (
        min(latencies) if latencies else None
    )

    maximum_latency = (
        max(latencies) if latencies else None
    )

    jitter = None

    if len(latencies) > 1:

        differences = [
            abs(latencies[i] - latencies[i - 1])
            for i in range(1, len(latencies))
        ]

        jitter = statistics.mean(differences)

    def rounded(value):
        return round(value, 2) if value is not None else None

    return {
        "protocol": protocol,
        "packets_sent": count,
        "packets_received": received_packets,
        "packets_lost": lost_packets,
        "packet_loss": round(packet_loss, 2),
        "average_latency": rounded(average_latency),
        "minimum_latency": rounded(minimum_latency),
        "maximum_latency": rounded(maximum_latency),
        "jitter": rounded(jitter),
        "latency_history": [
            round(value, 2) for value in latencies
        ]
    }