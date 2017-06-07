"""
.. Copyright 2017 EMBL-European Bioinformatics Institute
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
   
       http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import random
import pytest

from dmp import dmp

def test_files_by_user():

    users = ["adam", "ben", "chris", "denis", "eric"]

    da = dmp(test=True)

    for u in users:
        results = da.get_files_by_user(u)
        print(u, len(results))
        assert type(results) == type([])
