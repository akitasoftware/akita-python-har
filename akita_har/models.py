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

import datetime

from pydantic import BaseModel, validator
from typing import List, Optional, Union


class Number:
    """
    Type of a JSON 'number', which may be an int or float.
    """
    v: Union[int, float]

    def __init__(self, v: Union[int, float]):
        self.v = v

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if '.' in str(v):
            return float(v)
        return int(v)

    def __repr__(self):
        return str(self.v)


class Record(BaseModel):
    name: str
    value: str


class Timings(BaseModel):
    dns: Optional[Number]
    connect: Optional[Number]
    blocked: Optional[Number]
    send: Number
    wait: Number
    receive: Number
    ssl: Optional[Number]


class PostDataParam(BaseModel):
    name: str
    value: Optional[str]
    contentType: Optional[str]


class PostData(BaseModel):
    mimeType: str
    text: str
    params: Optional[List[PostDataParam]]


class ResponseContent(BaseModel):
    size: int
    mimeType: str
    text: str
    compression: Optional[int]
    encoding: Optional[str]


class Request(BaseModel):
    method: str
    url: str
    httpVersion: str
    cookies: List[Record]
    headers: List[Record]
    queryString: List[Record]
    postData: Optional[PostData]
    headersSize: int
    bodySize: int


class Response(BaseModel):
    status: int
    statusText: str
    httpVersion: str
    cookies: List[Record]
    headers: List[Record]
    content: ResponseContent
    redirectURL: str
    headersSize: int
    bodySize: int


class CacheEntry(BaseModel):
    expires: Optional[str]
    lastAccess: str
    eTag: str
    hitCount: int
    comment: Optional[str]


class Cache(BaseModel):
    beforeRequest: Optional[CacheEntry]
    afterRequest: Optional[CacheEntry]
    comment: Optional[str]


class Entry(BaseModel):
    startedDateTime: datetime.datetime
    time: Number
    request: Request
    response: Response
    cache: Cache
    timings: Timings

    @validator('startedDateTime')
    def datetime_must_have_timezone(cls, v: datetime.datetime):
        if v.tzinfo is None:
            raise ValueError('datetime must be timezone aware')
        return v


class Browser(BaseModel):
    name: str
    version: str
    comment: Optional[str]


class Creator(BaseModel):
    name: str
    version: str
    comment: Optional[str]


class HarLog(BaseModel):
    version: str
    creator: Creator
    browser: Optional[Browser]
    entries: List[Entry]
    comment: Optional[str]


class Har(BaseModel):
    log: HarLog
