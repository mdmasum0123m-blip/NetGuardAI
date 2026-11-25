# NetGuard AI

## Autonomous Network Monitoring and Analysis System

NetGuard AI is an Agentic AI-based network monitoring
application developed to analyze and compare TCP and UDP
communication performance.

## Features

- TCP client-server communication
- UDP client-server communication
- Real-time network monitoring
- Packet loss detection
- Latency and jitter measurement
- TCP and UDP performance comparison
- Automatic network monitoring
- Gemini AI-powered network analysis
- Autonomous decision-making
- Network recommendations
- Interactive web dashboard

## Technologies Used

- Python
- FastAPI
- TCP and UDP Socket Programming
- Google Gemini AI
- HTML, CSS and JavaScript
- Chart.js
- Git and GitHub

## System Architecture

User Dashboard
    |
FastAPI Backend
    |
Network Monitoring Engine
    |
TCP and UDP Client-Server Communication
    |
Gemini AI Agent
    |
Decision Making and Recommendations

## Installation

Clone the repository:

```bash
git clone https://github.com/mdmasum0123m-blip/NetGuardAI.git
cd NetGuardAI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

## Running the Application

Open three separate terminals with the virtual
environment activated.

Terminal 1:

```bash
python tcp_server.py
```

Terminal 2:

```bash
python udp_server.py
```

Terminal 3:

```bash
python -m uvicorn main:app --reload
```

## Access the Application

Dashboard:
http://127.0.0.1:8000/dashboard

Swagger API:
http://127.0.0.1:8000/docs

## Agentic AI Workflow

1. Collect TCP and UDP network metrics.
2. Analyze network performance.
3. Identify potential network problems.
4. Make an autonomous decision.
5. Perform additional tests when required.
6. Generate a final analysis and recommendations.

## Project Limitations

The current implementation monitors local loopback
communication. It does not measure external internet
performance.

## Security

API keys are stored in environment variables and
excluded from GitHub using the .gitignore file.

## Developer

Name: MIAH MASUM

Student ID: 25014180

University: Sejong University

Department: Computer Science and Engineering

Course: Computer Networks

## Project Purpose

This project demonstrates the practical integration
of TCP/UDP networking, network performance monitoring,
and Agentic Artificial Intelligence.