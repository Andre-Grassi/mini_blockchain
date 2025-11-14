#!/usr/bin/python3
"""Entry point for the blockchain client application.

Connects to a blockchain server via TCP and allows users to perform operations
(name registration, deposits, withdrawals). Supports both interactive mode
(stdin) and automated mode (file input). Uses a separate thread for user input
to allow concurrent message reception from the server.

Authors: Andre Grassi de Jesus, Ricardo Faria
Last Modified: Nov. 14 2025
"""

import argparse
import sys
from models.client import Client
from models.operation import Operation
import signal
import socket
from queue import Queue, Empty
import threading
import os


def input_thread(input_queue: Queue, shutdown_event: threading.Event):
    """Thread to read user input without blocking main loop."""

    __builtins__.print(
        "Usage:\n\t- deposit <amount>\n\t- withdraw <amount>\n\t- q to quit\n"
    )

    while not shutdown_event.is_set():
        try:
            message = input()
            if message:
                input_queue.put(message)
        except EOFError:
            # Ctrl+D pressed
            shutdown_event.set()
            break


def main(client_name: str, server_ip: str, server_port: int, client_input=sys.stdin):
    # Override print to add client name prefix
    def print(*args, **kwargs):
        __builtins__.print(f"[{client_name}]", *args, **kwargs)

    client = Client(client_name)

    print("My IP:", client.ip)
    print("Connecting to server", server_ip, "on port", server_port)

    client.connect_to(server_ip, server_port)
    connection = client.socket

    # Set socket timeout to keep checking for shutdown_event
    connection.settimeout(1.0)

    # Send name to server
    client.send_str(connection, "name " + client_name)

    shutdown_event = threading.Event()
    input_queue = Queue()

    if client_input != sys.stdin:
        for operation in client_input:
            input_queue.put(operation)
        # No need for input thread in this case

    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully."""

        sig_name = signal.Signals(signum).name
        print(f"\n{sig_name} received, shutting down...")

        shutdown_event.set()

    # Register signal handlers
    try:
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl + C
        signal.signal(signal.SIGTERM, signal_handler)  # Terminate signal
        signal.signal(signal.SIGHUP, signal_handler)  # Hangup signal
    except ValueError:
        # Signals can only be registered in main thread
        print("Warning: Signal handlers not registered (not in main thread)")

    if client_input == sys.stdin:
        # Start input thread
        input_thread_obj = threading.Thread(
            target=input_thread,
            args=(input_queue, shutdown_event),
            daemon=True,
            name="InputThread",
        )
        input_thread_obj.start()

    try:
        while not shutdown_event.is_set():
            try:
                message = input_queue.get_nowait()

                (action, _) = client.parse_message(message)

                print("Sending:", message)

                client.send_str(connection, message)

                if action is not None and action == Operation.QUIT.value:
                    print("Quitting.")
                    shutdown_event.set()

            except Empty:  # No input received from user
                pass

            # Listen server response
            # Attention: the client will ALWAYS wait for a server response here and
            # won't proceed without receiving something.
            try:
                recv_message_b = connection.recv(client.buffer_size)

                if not recv_message_b:
                    break  # Connection was closed, Break immediately

                recv_message = recv_message_b.decode()

                print(f"Received: {recv_message}")

            except socket.timeout:
                continue  # Normal execution

    except OSError:
        print("Closed")

    client.terminate()

    # Check if it's main thread and input is stdin to avoid issues in automated runs
    if (
        threading.current_thread() == threading.main_thread()
        and client_input == sys.stdin
    ):
        os._exit(0)  # Force exit, because input_thread is blocked by input function


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("client_name", type=str, help="The name of the client.")

    parser.add_argument(
        "server_ip", type=str, help="The IP of the server to connect to."
    )

    parser.add_argument(
        "server_port", type=int, help="The port of the server to connect to."
    )

    parser.add_argument(
        "--input",
        type=argparse.FileType("r"),
        default=None,
        help="File with operations to execute (default: stdin).",
    )

    args = parser.parse_args()

    if args.input:
        client_input = args.input.read().strip().split("\n")
    else:
        client_input = sys.stdin

    main(args.client_name, args.server_ip, args.server_port, client_input)
