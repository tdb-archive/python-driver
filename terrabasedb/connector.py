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


class Connector:
    """
    A connector contains a persistent connection to a TerrabaseDB instance
    and provides the ability to run queries
    """
    con = None

    def __init__(self, host="127.0.0.1", port=2003):
        """
        Create a new `Connector`
        """
        self.con = Connection(host, port)

    def execute(self, query):
        """
        Execute a `Query`
        """
        print(query.metaline.decode('utf-8'), end="")
        print(query.metalayout.decode('utf-8'), end="")
        print(query.dataframe.decode('utf-8'), end="")
        self.con.write(query.metaline)
        self.con.write(query.metalayout)
        self.con.write(query.dataframe)
        print(self.con.read(1024))

    def __del__(self):
        if self.con is not None:
            self.con.close()


class Connection(Connector):
    """
    A connection is a wrapper around a socket. It provides primitives to read
    and write data to and from the socket.
    """
    sock = None

    def __init__(self, host="127.0.0.1", port=2003):
        """
        Initialize a connection
        """
        sock = socket.socket()
        sock.connect((host, port))
        self.sock = sock

    def write(self, bytes):
        """
        Write data to the socket
        """
        if self.sock is None:
            raise "Connection not established"
        self.sock.send(bytes)

    def read(self, numbytes):
        """
        Read data from the socket
        """
        if self.sock is None:
            raise "Connection not established"
        retval = self.sock.recv(numbytes)
        return retval

    def close(self):
        """
        Close the socket
        """
        self.sock.close()


class ActionGroup:
    """
    An `ActionGroup` is a datagroup in the dataframe as defined by the Terrapipe
    protocol. In simple terms, a datagroup contains all the arguments required
    to execute an action such as `GET` or `SET`
    """
    metalayout_ext = None
    dataframe_ext = None
    count = None

    def __init__(self):
        """
        Create a new datagroup
        """
        self.metalayout_ext = ""
        self.dataframe_ext = ""
        self.count = 0

    def add(self, arg):
        """
        Add a new item to the `ActionGroup`
        """
        self.count += 1
        st = str(arg)
        self.metalayout_ext += ('#' + (str(len(st))))
        self.dataframe_ext += st
        self.dataframe_ext += '\n'


class SimpleQuery:
    """
    A `SimpleQuery` object is capable of producing a complete "Simple Query Packet" as
    defined by the Terrapipe protocol.
    """
    metaline = None
    metalayout = None
    dataframe = None

    def __init__(self, actiongroup):
        """
        Create a new `Query` object with an `ActionGroup`
        """
        self.metaline = "*!"
        self.metalayout = ""
        self.dataframe = ""

        # Now add the `&n` item to the metalayout dataframe
        group_len_bytes = str(actiongroup.count)
        self.metalayout += '#' + str(len(group_len_bytes) + 1)
        self.dataframe += '&' + group_len_bytes + '\n'

        # Now add the remaining items to the dataframe
        self.dataframe += actiongroup.dataframe_ext
        # Now add the remaining items to the metalayout
        self.metalayout += actiongroup.metalayout_ext
        # Now add a newline to the `metalayout`
        self.metalayout += '\n'

        # Now prepare the metaline
        self.metaline += str(len(self.dataframe)) + '!'
        self.metaline += str(len(self.metalayout)) + '\n'

        # Add a newline to the dataframe
        self.dataframe += '\n'
        # Now turn them into bytes
        self.metaline = bytes(self.metaline, "utf-8")
        self.metalayout = bytes(self.metalayout, "utf-8")
        self.dataframe = bytes(self.dataframe, "utf-8")
