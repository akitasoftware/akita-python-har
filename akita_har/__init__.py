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

import datetime
import json
import queue
import time
import threading

import akita_har.models as M


__version__ = "0.0.2"


def _default_har_json_serialization(x):
    """
    Provides JSON serialization for HAR data structures that lack a default
    serialization.  For example, datetime elements need to be serialized as
    ISO 8601 strings.
    """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    else:
        return str(x)


class HarWriter:
    """
    Coordinates thread-safe request/response logging, encoded as an HTTP
    Archive (HAR) file.

    See http://www.softwareishard.com/har/viewer/ for the HAR formatting
    schema.
    """

    _creator = M.Creator(
        name="Akita HAR",
        version=__version__,
        comment="https://github.com/akitasoftware/akita-python-har"
    )
    _browser = M.Browser(name="", version="")
    _comment = 'null'

    def __init__(self, *args, creator=None, browser=None, comment=None):
        """
        Opens a file as specified by *args and starts a writer thread that writes
        entries to it as they are submitted through self.write_entry().

        The creator, browser, and comment fields are serialized to the corresponding
        fields in the HAR file.
        """
        self._creator = creator if creator is not None else self._creator
        self._browser = browser if browser is not None else self._browser
        self._comment = f'"{comment}"' if comment is not None else self._comment

        self.file = open(*args)
        self.finished = False
        self.first_entry = True
        self.queue = queue.Queue()

        # Write initial data to the HAR file.
        self._write_preamble()

        threading.Thread(name=f"HarWriter_{time.time}", target=self._writer).start()

    def write_entry(self, entry: M.Entry):
        """
        Write an entry to this HAR file.  This method is thread-safe.
        """
        sep = '' if self.first_entry else ', '
        self.first_entry = False

        self.queue.put(sep + json.dumps(entry.dict(exclude_defaults=True), default=_default_har_json_serialization))

    def close(self):
        """
        Finalize the HAR file formatting, close the writer thread, and close
        the HAR file.
        """
        self.queue.join()
        self.finished = True
        self._write_postscript()
        self.file.close()

    def _write_preamble(self):
        """
        Serialize the first parts of models.HarLog manually in order
        to write entries as they're given to us, rather than batching them
        in memory (e.g. in a models.Entries object) until all entries have
        been submitted.
        """
        self.file.write(f'''{{
            "log": {{
                "version": "1.2",
                "creator": {json.dumps(self._creator.dict())},
                "browser": {json.dumps(self._browser.dict())},
                "comment": {self._comment},
                "entries": [
        ''')

    def _write_postscript(self):
        """
        Terminate the entries array, log object, and enclosing HAR object.
        Assumes that self._write_preamble() has already been called.
        """
        self.file.write(']}}')

    def _writer(self):
        while not self.finished:
            try:
                entry = self.queue.get(True, 1)
            except queue.Empty:
                continue
            self.file.write(entry)
            self.queue.task_done()
