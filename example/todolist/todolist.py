# -*- coding: utf-8 -*-
import uuid

from tendaysweb import TenDaysWeb, Response
from aiomysql import create_pool

from models import TodoList, Todo

db_connection_pool = None

app = TenDaysWeb('todolist')
todolist = TodoList()


@app.run_before()
async def init_connection_pool(loop):
    global db_connection_pool
    db_connection_pool = await create_pool(
        host='server_address',
        port=3306,
        user='user',
        password='password',
        db='db_name',
        loop=loop)


@app.route('/todos', methods=['POST'])
async def create_todo(request):
    todo = Todo(uuid)
    return Response(content='New Todo')


@app.route('/todos/<id>', methods=['GET'])
async def get_todo_details(request, id):
    return Response(content='acync hello world')


@app.error_handler(404)
async def not_found():
    return Response(content='nothing here')


if __name__ == '__main__':
    app.run()
