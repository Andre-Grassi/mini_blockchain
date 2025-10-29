import socket

BUFFER_SIZE = 1024


class Server:
    def __init__(self, port: int):
        self.ip = self._get_own_ip()
        self.port = port
        self.buffer_size = BUFFER_SIZE

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_socket(self):
        self.socket.bind((self.ip, self.port))

    def close(self):
        self.socket.close()

    def _get_own_ip(self):
        aux_socket = None
        try:
            # Create a UDP socket
            aux_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Connect to an extern IP
            # 8.8.8.8 IP is a public DNS from Google
            aux_socket.connect(("8.8.8.8", 1))

            # Get local IP associated with this socket
            own_ip = aux_socket.getsockname()[0]
        except Exception as e:
            print(f"Couldn't get local IP: {e}")
        finally:
            if aux_socket:
                aux_socket.close()

        return own_ip
