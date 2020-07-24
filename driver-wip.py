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
from terrabasedb.driver import ConnectivityError
HOST = "localhost"
PORT = 2003


class Database:
    sock = None

    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except:
            raise ConnectivityError

    def write_query(self, query):
        self.sock.send(query)

    def read_response(self, bufsize):
        return str(self.sock.recv(bufsize).decode('UTF-8'))


class SimpleCommand:
    metaline = "*!"
    metalayout = ""
    dataframe = ""
    size_tracker = 0

    def __init__(self):
        pass

    def add_command(self, cmd):
        r = bytes(cmd, 'UTF-8')
        rlen = len(r)
        self.size_tracker += (rlen + 1)
        self.metalayout = self.metalayout + str(rlen) + "#"
        self.dataframe += cmd + "\n"

    def prepare_query(self):
        x = bytes("{0}{1}!{2}\n{3}\n{4}".format(self.metaline, self.size_tracker, len(
            self.metalayout), self.metalayout, self.dataframe), "UTF-8")
        return x


cmd = SimpleCommand()
cmd.add_command("get")
cmd.add_command("sayan")
q = cmd.prepare_query()
db = Database()
db.write_query(q)
print(db.read_response(1024))
