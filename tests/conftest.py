import pytest
import threading
from models.server import Server


@pytest.fixture(scope="module")
def start_server():
    server = Server(0)
    lock = threading.Lock()

    yield server, lock

    print("\n[Fixture] Closing server...")
    server.close()
