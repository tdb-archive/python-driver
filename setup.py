#
# Created on Thu Jul 23 2020
#
# This file is a part of the Python TerrabaseDB driver
#
# Copyright (c) 2020, Sayan Nandan <ohsayan at outlook dot com>
# You may obtain a copy of the License at
# Licensed under the Apache License, Version 2.0 (the "License");
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

import setuptools

setuptools.setup(
    name="terrabasedb",
    version="0.1.0",
    author="Sayan Nandan",
    author_email="ohsayan@outlook.com",
    description="The official python driver for TerrabaseDB",
    url="https://github.com/terrabasedb/python-driver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Database :: Front-Ends",
    ],
    python_requires='>=3.6',
)
