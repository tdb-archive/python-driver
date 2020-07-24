#
# Created on Fri Jul 24 2020
#
# This file is a part of the Python TerrabaseDB driver
#
# Copyright (c) 2020, Sayan Nandan <ohsayan at outlook dot com>
# Licensed under the Apache License, Version 2.0 (the "License");
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import socket
from enum import Enum


class ResponseType(Enum):
    SIMPLE = '*'
    PIPELINE = '$'


class TerraError(Exception):
    """
    A class to represent errors that may occur while running a query
    """

    def __init__(self, desc):
        super().__init__(desc)


class ConnectivityError(TerraError):
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

    def __init__(self, msg="The server sent an invalid response"):
        super().__init__(msg)


class Connection:
    """
    The connection class. This is used for reading/writing data to/from the
    sockets
    """

    def __init__(self, host="localhost", port=2003):
        try:
            self.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        except:
            raise ConnectionError

    def __write_resp(self, stream):
        try:
            self.socket.sendall(stream)
        except:
            raise SocketRWError

    def __read_resp(self, stream, buflen):
        try:
            return self.socket.recv(buflen)
        except:
            raise SocketRWError


class Frame:
    actiontype = None
    clength = 0
    ml_size = 0
    respcode = None
    split_sequence = None

    def decode_metaline(self, line):
        """
        Initialize a frame with the metaline
        """
        size = len(list)
        indexes = [idx + 1 for idx, val in enumerate(line) if val == '!']
        res = [indexes[i: j] for i, j in zip(
            [0] + indexes, indexes + ([size] if indexes[-1] != size else []))]
        if len(res) != 4:
            raise InvalidResponseError
        if res[0] == ResponseType.PIPELINE:
            self.actiontype == ResponseType.PIPELINE
        elif res[0] == ResponseType.SIMPLE:
            self.actiontype == ResponseType.SIMPLE
        else:
            raise InvalidResponseError(
                "The response is not a simple/pipelined response. You may be using an incorrect driver version.")
        (res[1], res[2], res[3]) = (self.respcode, self.clength, self.ml_size)
