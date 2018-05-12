# -*- coding: utf-8 -*-
from tendaysweb import TenDaysWeb, Response

app = TenDaysWeb('testApp')


@app.route('/', methods=['GET'])
async def index(request):
    return Response(content='acync hello world')


@app.route('/<name>', methods=['GET'])
async def show_name(request, name):
    return Response(content=f'hello {name}')


@app.error_handler(404)
async def not_found():
    return Response(content='not found')


if __name__ == '__main__':
    app.run()
