#!/usr/bin/python3

#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

import argparse
import threading
import signal
import sys
import socket

from models.server import Server
from models.operation import Operation


def main(server_port: int):
    server = Server(server_port)

    print(f"Server IP: {server.ip}")

    server.bind_socket()
    server.socket.listen(5)

    print(f"Server listening on {server.ip}:{server_port}")

    # Shared state
    lock = threading.Lock()
    shutdown_event = threading.Event()
    active_threads = []

    def signal_handler(signum, frame):
        """Handle shutdown signals gracefully."""
        sig_name = signal.Signals(signum).name
        print(f"\n{sig_name} received, shutting down...")

        # Signal all threads to stop
        shutdown_event.set()

        # Close socket to unblock accept()
        try:
            server.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl + C
    signal.signal(signal.SIGTERM, signal_handler)  # Terminate signal
    signal.signal(signal.SIGHUP, signal_handler)  # Hangup signal

    # Main accept loop
    try:
        while not shutdown_event.is_set():
            try:
                connection, client_address = server.socket.accept()

                if shutdown_event.is_set():
                    connection.close()
                    break

                print(f"Accepted connection from {client_address}")

                # Create non-daemon thread
                thread = threading.Thread(
                    target=server.answer_client,
                    args=(connection, lock, shutdown_event),  # pass event
                    daemon=False,  # non-daemon for graceful cleanup
                    name=f"Client-{client_address}",
                )
                active_threads.append(thread)
                thread.start()

            except OSError:
                # Socket closed by signal handler
                if shutdown_event.is_set():
                    break
                raise

    finally:
        print("Waiting for client threads to finish...")

        # Wait for all threads to finish (with timeout)
        for thread in active_threads:
            thread.join(timeout=5.0)  # wait max 5s per thread
            if thread.is_alive():
                print(f"Warning: {thread.name} did not finish in time")

        # Final cleanup
        try:
            server.socket.close()
        except:
            pass

        print("Server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the mini blockchain server")
    parser.add_argument(
        "server_port",
        type=int,
        help="The port to run the server on",
    )

    args = parser.parse_args()

    try:
        main(args.server_port)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
