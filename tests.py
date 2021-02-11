# Copyright 2021 Akita Software, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pydantic
import unittest

import akita_har.models as har

from akita_har import _default_har_json_serialization


class TestHar(unittest.TestCase):
    def test_parsing_marshalling(self):
        test_files = [
            'testdata/trace_1.har',
            'testdata/trace_2.har',
        ]

        for test in test_files:
            with open(test, 'r') as f:
                har_json = json.load(f)
            har_json_str = json.dumps(har_json, sort_keys=True)

            har_pydantic = pydantic.parse_obj_as(har.Har, har_json)
            har_pydantic_json_str = json.dumps(
                har_pydantic.dict(exclude_unset=True),
                default=_default_har_json_serialization,
                sort_keys=True
            )

            self.assertEqual(har_pydantic_json_str, har_json_str, test)


if __name__ == '__main__':
    unittest.main()
