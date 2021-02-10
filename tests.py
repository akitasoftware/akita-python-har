# 3-Clause BSD License
#
# Copyright (c) 2009, Boxed Ice <hello@boxedice.com>
# Copyright (c) 2010-2016, Datadog <info@datadoghq.com>
# Copyright (c) 2020-present, Akita Software <info@akitasoftware.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
