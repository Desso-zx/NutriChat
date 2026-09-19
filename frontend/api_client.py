import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def ask_question(question: str, timeout: int = 60) -> dict:
    """
    Send a question to the backend's /query endpoint.
    Returns {"answer": str, "sources": list[str]} on success.
    Raises requests.RequestException on network/timeout failure.
    Raises ValueError on a non-200 response (e.g. validation error).
    """
    response = requests.post(
        f"{API_BASE_URL}/query",
        json={"question": question},
        timeout=timeout,
    )

    if response.status_code != 200:
        raise ValueError(f"Backend returned {response.status_code}: {response.text}")

    return response.json()


def check_backend_health() -> bool:
    """Quick check whether the backend is reachable at all."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    