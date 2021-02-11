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
