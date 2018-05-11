# -*- coding: utf-8 -*-
import asyncio
import inspect
import logging
import functools
from typing import Callable, List, AnyStr, Dict

import httptools

from .request import Request
from .response import Response
from .exceptions import HttpException
from .utils import HTTP_METHODS


logger = logging.getLogger('tendaysweb')



class TenDaysWeb():
    def __init__(self, application_name):
        """
        TenDaysWeb allow user create multi instace in one application.
        :param application_name: just name your TenDaysWeb Instance
        """
        self._app_name = application_name
        self._rule_list = []
        pass

    def route(self, url: str, methods: List = HTTP_METHODS, **options):
        """
            A decorator that is used to register a view function for a
        given URL rule.  Example::

            @app.route('/')
            def index():
                return 'Hello World'
        """

        def decorator(func):
            self._rule_list.append(Rule(url, methods, func, **options))
            return func

        return decorator

    async def handler(self, reader, writer):
        """
        The handler handling each request
        :param request: the Request instance
        :return: The Response instance
        """
        request: Request = await TenDaysWeb.read_http_message(reader)
        response: Response = Response()

        handle = None
        for rule in self._rule_list:
            if request.url == rule._url and request.method in rule._methods:
                handle = rule._endpoint

        if not callable(handle):
            pass
        else:
            response.content = await handle(request)  # Response.construct_response()

        #send payload
        writer.write(response.to_payload())

        await writer.drain()
        writer.close()

    async def start_server(self,
                           http_handler: Callable,
                           websocket_handler=None,
                           address: str = 'localhost',
                           port: int = 8000):
        """
        start server
        """
        return await asyncio.start_server(http_handler, address, port)

    def run(self,
            host: str = "localhost",
            port: int = 8000,
            debug: bool = False):
        """
        start the http server
        :param host: The listening host
        :param port: The listening port
        :param debug: whether it is in debug mod or not
        """
        self.debug = debug
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.start_server(self.handler, None, host, port))
            logger.info(f'Start listening {host}:{port}')
            loop.run_forever()
        except KeyboardInterrupt:
            loop.close()

    @staticmethod
    async def read_http_message(
            reader: asyncio.streams.StreamReader) -> Request:
        """
        this funciton will reading data cyclically until recivied a complete http message
        :param reqreaderuest: the asyncio.streams.StreamReader instance
        :return The Request instance
        """
        protocol = ParseProtocol()
        parser = httptools.HttpRequestParser(protocol)
        while True:
            data = await reader.read(2 ** 16)

            try:
                parser.feed_data(data)
            except httptools.HttpParserUpgrade:
                raise HttpException(400)

            if protocol.completed:
                request: Request = Request.load_from_parser(parser, protocol)
                break
            if data == b'':
                return None
        return request


class Rule():
    def __init__(self, url: AnyStr, methods: List, endpoint: Callable,
                 **options):
        """
        A rule describes a url is expected to be handled and how to handle it.
        :param url: url to be handled
        :param method: a list of HTTP method to specify which methods should be handled
        :param endpoint: the actual function/class process this request
        """
        self._url = url
        self._methods = methods
        self._options = options
        self._endpoint = endpoint


class ParseProtocol:
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