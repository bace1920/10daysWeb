# -*- coding: utf-8 -*-
from typing import Dict
from.exceptions import HttpException

from httptools import HttpRequestParser, HttpParserUpgrade

class Protocol:
    """
    The protocol for HttpRequestParser
    """

    def __init__(self) -> None:
        self.url: str = ''
        self.headers: Dict[str, str] = {}
        self.body: bytes = b''
        self.completed: bool = False

    def on_url(self, url: bytes) -> None:
        self.url = url.decode()

    def on_header(self, name: bytes, value: bytes) -> None:
        self.headers[name.decode()] = value.decode()

    def on_body(self, body: bytes) -> None:
        self.body += body

    def on_message_complete(self) -> None:
        self.completed = True


class Request:
    def __init__(self, method: str, url: str, version: str,
                 headers: Dict[str, str], content: str):
        self.method = method
        self.url = url
        self.version = version
        self.headers = headers
        self.content = content


    @classmethod
    def load_from_str(cls, data: str) -> 'Request':
        protocol = Protocol()
        parser = HttpRequestParser(protocol)

        try:
            parser.feed_data(data)

        except HttpParserUpgrade:
            raise HttpException(400)

        return cls(parser.get_method().decode(), protocol.url, parser.get_http_version(), protocol.headers, protocol.body)
