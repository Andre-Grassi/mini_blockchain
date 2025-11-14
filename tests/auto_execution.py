import argparse
import os
import subprocess
import pytest
import threading
import time
import socket
from models.server import Server
from models.client import Client
import run_server
import run_client
import sys
import io

if __name__ == "__main__":
    # Parse server ip and port arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", type=str, help="Server IP")
    parser.add_argument("server_port", type=int, default=8080, help="Server Port")

    args = parser.parse_args()

    # Run parallel processes for server and client
    server_log = open("server.log", "w", encoding="utf-8")
    server_proc = subprocess.Popen(
        [sys.executable, "../src/run_server.py", str(args.server_port)],
        stdout=server_log,
        stderr=server_log,
    )

    time.sleep(1)  # Give server time to start

    # For each file inside inputs/, run a client
    for input_file in os.listdir("inputs/"):
        input_path = os.path.join("inputs/", input_file)
        # client_log = open(f"client_{input_file}.log", "w", encoding="utf-8")
        client_proc = subprocess.Popen(
            [
                sys.executable,
                "../src/run_client.py",
                "CLIENT_" + input_file.replace(".txt", ""),
                args.server_ip,
                str(args.server_port),
                "--input",
                input_path,
            ],
            stdout=subprocess.PIPE,
        )
        client_proc.wait()
        # client_log.close()

    # Wait for processes to complete
    server_proc.wait()
    client_proc.wait()

    # Close log files
    server_log.close()
    # client_log.close()
