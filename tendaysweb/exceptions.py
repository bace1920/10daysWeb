# -*- coding: utf-8 -*-
class HttpException(Exception):
    def __init__(self, errCode: int, err: str='', content=''):
        self.errCode = errCode
        self.err = err
        self.content = content