from fastapi import FastAPI
import socket
import time

app = FastAPI(title="NetGuard AI")

HOST = "127.0.0.1"


@app.get("/")
def home():
    return {
        "application": "NetGuard AI",
        "status": "Running"
    }


@app.get("/api/tcp")
def tcp_test():
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as client:

            client.settimeout(3)
            client.connect((HOST, 5000))

            message = b"NetGuard AI Test"
            start = time.perf_counter()

            client.sendall(message)

            data = b""

            while len(data) < len(message):
                chunk = client.recv(4096)
                if not chunk:
                    raise ConnectionError("Disconnected")
                data += chunk

            latency = (time.perf_counter() - start) * 1000

            return {
                "protocol": "TCP",
                "status": "Success" if data == message else "Failed",
                "latency": round(latency, 2),
                "sent": message.decode(),
                "received": data.decode()
            }

    except Exception as e:
        return {
            "protocol": "TCP",
            "status": "Failed",
            "error": str(e)
        }


@app.get("/api/udp")
def udp_test():
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        ) as client:

            client.settimeout(3)

            message = b"NetGuard AI Test"
            start = time.perf_counter()

            client.sendto(message, (HOST, 5001))
            data, addr = client.recvfrom(4096)

            latency = (time.perf_counter() - start) * 1000

            return {
                "protocol": "UDP",
                "status": "Success" if data == message else "Failed",
                "latency": round(latency, 2),
                "sent": message.decode(),
                "received": data.decode()
            }

    except Exception as e:
        return {
            "protocol": "UDP",
            "status": "Failed",
            "error": str(e)
        }

from fastapi.responses import FileResponse
from pathlib import Path


@app.get("/dashboard")
def dashboard():
    return FileResponse(
        Path(__file__).parent / "templates" / "index.html"
    )

from network_monitor import monitor_network


@app.get("/api/monitor/tcp")
def monitor_tcp():
    
    return monitor_network("TCP", 10)


@app.get("/api/monitor/udp")
def monitor_udp():
    return monitor_network("UDP", 10)

from ai_agent import analyze_network


@app.get("/api/ai/analyze")
def ai_network_analysis():
    tcp_data = monitor_network("TCP", 10)
    udp_data = monitor_network("UDP", 10)

    return analyze_network(tcp_data, udp_data)