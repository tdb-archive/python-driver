import socket


class TerraError(Exception):
    """
    A class to represent errors that may occur while running a query
    """

    def __init__(self, desc):
        super().__init__(desc)


class ConnectionError(TerraError):
    """
    This error is raised when a connection cannot be established between
    the client and the database
    """

    def __init__(self):
        super().__init__("An error occurred while connecting to the server")


class SocketRWError(TerraError):
    """
    This error is raised when data cannot be read from/written to the socket
    """

    def __init__(self):
        super().__init__("An error occurred while writing data to the socket")


class InvalidResponseError(TerraError):
    """
    This error is raised when the server sends an invalid response
    """

    def __init(self):
        super().__init__("The server sent an invalid response")


class Connection:
    """
    The connection class. This is used to define
    """

    def __init__(self, host="localhost", port=2003):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        except:
            raise ConnectionError

    def write_resp(self, stream):
        try:
            self.socket.sendall(stream)
        except:
            raise SocketRWError
