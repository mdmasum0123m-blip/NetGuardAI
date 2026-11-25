
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from network_monitor import monitor_network

load_dotenv(Path(__file__).parent / ".env")

PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.1-flash-lite"


def generate_ai_response(client, prompt):

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:

        for attempt in range(2):

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if not response.text:
                    raise ValueError("Empty AI response")

                return response.text, model

            except Exception as e:
                code = getattr(e, "code", None)

                if code in (429, 404):
                    break

                if code == 503 and attempt == 0:
                    time.sleep(3)
                    continue

                if code == 503:
                    break

                raise

    raise RuntimeError("AI models temporarily unavailable")


def analyze_network(tcp_data, udp_data):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "Failed",
            "error": "API key not found"
        }

    try:
        client = genai.Client(api_key=api_key)

        decision_prompt = f"""
You are NetGuard AI, an autonomous network agent.

TCP measurements:
{json.dumps(tcp_data)}

UDP measurements:
{json.dumps(udp_data)}

Analyze latency, packet loss and jitter.

Choose exactly one diagnostic action:

RETEST_TCP
RETEST_UDP
RETEST_BOTH
NO_ACTION

If measurements are unstable or insufficient,
choose a suitable retest.

Return only the action name.
"""

        decision, decision_model = generate_ai_response(
            client, decision_prompt
        )

        decision = decision.strip().upper()

        allowed_actions = [
            "RETEST_TCP",
            "RETEST_UDP",
            "RETEST_BOTH",
            "NO_ACTION"
        ]

        if decision not in allowed_actions:
            decision = "RETEST_BOTH"
            decision_source = "Safe default"
        else:
            decision_source = "AI"

        action_log = [
            "Initial TCP and UDP data collected",
            "AI analyzed network measurements",
            f"Decision: {decision}"
        ]

        new_results = {}

        if decision in ["RETEST_TCP", "RETEST_BOTH"]:

            new_results["tcp"] = monitor_network(
                "TCP", 20
            )

            action_log.append(
                "TCP diagnostic test executed"
            )

        if decision in ["RETEST_UDP", "RETEST_BOTH"]:

            new_results["udp"] = monitor_network(
                "UDP", 20
            )

            action_log.append(
                "UDP diagnostic test executed"
            )

        if decision == "NO_ACTION":
            action_log.append(
                "No additional test required"
            )

        report_prompt = f"""
You are NetGuard AI.

Initial TCP Data:
{json.dumps(tcp_data)}

Initial UDP Data:
{json.dumps(udp_data)}

Diagnostic Decision:
{decision}

Decision Source:
{decision_source}

Additional Test Results:
{json.dumps(new_results)}

Generate a professional report containing:

1. Overall network health
2. TCP vs UDP comparison
3. Latency, packet loss and jitter
4. Detected network problems
5. Diagnostic action and findings
6. Practical recommendations
7. Suitable protocol for applications
8. Final conclusion

Use simple English.
Do not invent measurements.
These are local network tests,
not internet speed measurements.
"""

        report, report_model = generate_ai_response(
            client, report_prompt
        )

        action_log.append(
            "Final AI report generated"
        )

        return {
            "status": "Success",
            "agent": "NetGuard AI",
            "mode": "Autonomous Agentic AI",
            "model": report_model,
            "decision_model": decision_model,
            "decision": decision,
            "decision_source": decision_source,
            "action_log": action_log,
            "tcp_data": tcp_data,
            "udp_data": udp_data,
            "diagnostic_results": new_results,
            "analysis": report
        }

    except Exception as e:

        return {
            "status": "Failed",
            "error": str(e)
        }
