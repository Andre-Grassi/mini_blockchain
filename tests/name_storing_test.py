import pytest
import threading
from socket import socket
from models.server import Server
from models.operation import Operation


# --- The Test ---
def test_successful_deposit_flow(start_server, mocker):
    """
    Tests if a client can (1) send name, (2) deposit, (3) quit.
    """
    # 1. SETUP

    server, lock = start_server

    # Create a FAKE (Mock) Connection
    mock_connection = mocker.MagicMock(spec=socket)

    # Define what mock_connection.recv() will return, IN ORDER.
    # This simulates the client sending 3 messages and then closing.
    mock_connection.recv.side_effect = [
        b"name Andre\n",  # 1. Client sends name
        b"deposit 100\n",  # 2. Client sends deposit
        b"quit\n",  # 3. Client sends 'quit'
        b"",  # 4. Client closes connection (recv returns 0)
    ]

    # Let's "spy" on the server.send_str function to see what is sent
    # back to the client.
    mocker.spy(server, "send_str")

    # Let's also "spy" on the client_deposit function to verify
    # if it was called correctly.
    mocker.spy(server, "client_deposit")

    # 2. EXECUTION
    # We run the client logic function with our fake objects
    server.answer_client(mock_connection, lock)

    # 3. VERIFICATION (Asserts)

    # Check if the deposit was processed correctly
    # (.spy_call syntax only works in Python 3.8+)
    server.client_deposit.assert_called_once_with("Andre", 100)

    # Check if the connection was closed at the end
    mock_connection.close.assert_called_once()
