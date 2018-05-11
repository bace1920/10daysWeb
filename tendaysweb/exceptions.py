# -*- coding: utf-8 -*-

from .utils import STATUS_CODES

class HttpException(Exception):
    def __init__(self, errCode: int, err: str=''):
        self.errCode = errCode
        self.err = err if err else STATUS_CODES.get(errCode, 'Unknown Error')
