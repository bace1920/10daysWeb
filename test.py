# -*- coding: utf-8 -*-
from tendaysweb import TenDaysWeb

testApp = TenDaysWeb('testApp')


@testApp.route('/', methods=['GET'])
def hello():
    return 'hello world'


if __name__ == '__main__':
    testApp.run()