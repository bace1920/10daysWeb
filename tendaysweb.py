# -*- coding: utf-8 -*-
import asyncio
import httptools
from typing import Callable, List, AnyStr

from aiohttp import web

HTTP_METHODS = [
    'OPTIONS',
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'TRACE',
    'CONNECT',
]


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

        def decorator(f):
            self._rule_list.append(Rule(url, methods, f, **options))
            return f

        return decorator

    async def handler(self, reader, writer):
        """
        The handler handling each request
        :param request: the Request instance
        :return: The Response instance
        """
        data = await reader.read(2048)
        url = data.decode().split(' ')[1]
        content = ''
        for rule in self._rule_list:
            if rule._url == url:
                content = rule.get_endpoint()()
        response: bytes = f'HTTP/1.1 200 OK\r\n'.encode()
        response += b'\r\n'
        response += content.encode()

        #send payload
        writer.write(response)
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
            loop.run_forever()
        except KeyboardInterrupt:
            loop.close()

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

    def get_url(self) -> AnyStr:
        return self._url

    def get_endpoint(self)-> Callable:
        return self._endpoint