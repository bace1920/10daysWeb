# -*- coding: utf-8 -*-
from typing import List, Dict


class Todo():
    def __init__(self, uuid: str,
                 title: str,
                 content: bytes,
                 wechat_uuid: str):
        self.uuid = uuid
        self.title = title
        self.content = content
        self.wechat_uuid = wechat_uuid


class TodoList():
    def __init__(self):
        self._todo_list: Dict[str, Todo] = {}

    def __iter__(self):
        for todo in self._todo_list:
            yield todo

    def __getitem__(self, key: str):
        return self._todo_list[key]

    def __setitem__(self, key: str, todo: Todo):
        self._todo_list[key] = todo
