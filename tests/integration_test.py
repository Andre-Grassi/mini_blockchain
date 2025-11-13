import pytest
import threading
import time
import socket
from models.server import Server
from models.client import Client
import run_server
import run_client
import sys


def test_integration():
    """Test that client can connect to server."""

    # Step 1: Start server in a thread
    server_thread = threading.Thread(target=run_server.main, args=(8080,), daemon=True)
    server_thread.start()

    # Give server time to start
    time.sleep(0.1)

    fake_input = io.StringIO("first line\nsecond line\n")  # whatever the client expects

    old_stdin = sys.stdin
    sys.stdin = fake_input

    # Step 2: Start client and connect to server
    client_thread = threading.Thread(
        target=run_client.main, args=("CLIENT_NAME", "localhost", 8080), daemon=True
    )
    client_thread.start()

    # Wait for server thread to complete
    client_thread.join()
    server_thread.join()

    print("Test passed!")
