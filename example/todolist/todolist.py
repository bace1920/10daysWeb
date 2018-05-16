# -*- coding: utf-8 -*-
# This app use json format in http body
import uuid

import ujson
from tendaysweb import TenDaysWeb, Response, HttpException
from aiomysql import create_pool

from models import TodoList, Todo

db_connection_pool = None

app = TenDaysWeb('todolist')
todolist = TodoList()

SELECT_SQL = '''
SELECT * FROM TABLE todolist_wechat WHERE wechat_uuid='%s'
'''

INSERT_SQL = '''
INSERT INTO TABLE 
todolist_wechat(uuid, wechat_uuid, title, content) 
values('%s', '%s', '%s', '%s', '%s');
'''


@app.signal(type='run_before_start')
async def init_connection_pool(loop):
    """create a connection pool
    """
    global db_connection_pool
    db_connection_pool = await create_pool(
        host='server_address',
        port=3306,
        user='user',
        password='password',
        db='db_name',
        loop=loop)


@app.signal(type='run_after_close')
async def close_connection_pool(self):
    """close a connection pool
    """
    global db_connection_pool
    db_connection_pool.close()
    await db_connection_pool.wait_closed()


@app.route('/todos', methods=['GET'])
async def get_todos_list(request):
    """get all todo's uuid and title
    """
    todo_json = ujson.load(request.content)
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(SELECT_SQL, (todo_json['wechat_uuid']))
            print(cur.description)
            (r,) = await cur.fetchone()
            assert r == 42
    return Response(content='New Todo')


@app.route('/todos', methods=['POST'])
async def create_todo(request):
    """create a new todo instance store in db and return 
    the uuid of it in response body
    """
    todo_json = ujson.load(request.content)
    new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'todo.cykrt.me')
    todo = Todo(new_uuid, todo_json['title'], todo_json['content'], todo_json['wehcat_uuid'])
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(INSERT_SQL, (todo_json['uuid']))
            print(cur.description)
            (r, ) = await cur.fetchone()
            assert r == 42
    return Response(content='New Todo')


@app.route('/todos/<id>', methods=['GET'])
async def get_todo_details(request, id):
    """
    """
    return Response(content='acync hello world')


@app.error_handler(404)
async def not_found():
    return Response(content='nothing here')


if __name__ == '__main__':
    app.run()
