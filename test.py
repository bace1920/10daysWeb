# -*- coding: utf-8 -*-
from tendaysweb import TenDaysWeb

testApp = TenDaysWeb('testApp')


@testApp.route('/', methods=['GET'])
async def hello_async():
    await 'async hello world'


@testApp.route('/sync', methods=['GET'])
def hello_sync():
    return 'snyc hello world!'


if __name__ == '__main__':
    testApp.run()