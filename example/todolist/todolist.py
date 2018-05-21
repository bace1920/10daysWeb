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

SELECT_ALL_SQL = '''
SELECT * FROM todolist_wechat;
'''

SELECT_SQL = '''
SELECT * FROM todolist_wechat WHERE wechat_uuid=%s;\
'''

INSERT_SQL = '''INSERT INTO todolist_wechat(uuid, wechat_uuid, title, content) VALUES(%s, %s, %s, %s);
'''

DELETE_SQL = '''DELETE FROM todolist_wechat WHERE uuid=%s;'''


@app.signal(signal_type='run_before_start')
async def init_connection_pool(loop):
    """create a connection pool
    """
    global db_connection_pool
    db_connection_pool = await create_pool(
        host='data-jp-1.vedbs.link',
        port=3306,
        user='vedbs_1398',
        password='dC2ZEQ09Nd',
        db='vedbs_1398',
        loop=loop)


@app.signal(signal_type='run_after_close')
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
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(SELECT_ALL_SQL)
            res = await cur.fetchall()
    return Response(content='New Todo')


@app.route('/todos', methods=['POST'])
async def create_todo(request):
    """create a new todo instance store in db and return 
    the uuid of it in response body
    """
    todo_json = ujson.loads(request.content)
    new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'todo.cykrt.me')
    todo = Todo(
        str(new_uuid), todo_json['title'], todo_json['content'],
        todo_json['wechat_uuid'])
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(INSERT_SQL,
                              (str(new_uuid), todo_json['wechat_uuid'],
                               todo_json['title'], todo_json['content']))
        await conn.commit()
    return Response(content='POST')


@app.route('/todos', methods=['DELETE'])
async def create_todo(request):
    """create a new todo instance store in db and return 
    the uuid of it in response body
    """
    todo_json = ujson.loads(request.content)
    todo = Todo(
        str(new_uuid), todo_json['title'], todo_json['content'],
        todo_json['wechat_uuid'])
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(DELETE_SQL, (todo_json['uuid']))
        await conn.commit()
    return Response(content='Delete Todo')



@app.route('/todos/<id>', methods=['GET'])
async def get_todo_details(request, id):
    """get all info about a todo
    """
    async with db_connection_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(SELECT_SQL, (todo_json['wechat_uuid']))
            res = await cur.fetchall()
    return Response(content='acync hello world')


@app.error_handler(404)
async def not_found():
    return Response(content='nothing here')


if __name__ == '__main__':
    app.run()
