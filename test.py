# -*- coding: utf-8 -*-
from tendaysweb import TenDaysWeb

testApp = TenDaysWeb('testApp')


@testApp.route('/', methods=['GET'])
async def index(request):
    return 'acync hello world'


# @testApp.route('/sync', methods=['GET'])
# asyncdef hello_sync():
#     return 'snyc hello world!'


if __name__ == '__main__':
    testApp.run()