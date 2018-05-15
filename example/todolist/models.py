# -*- coding: utf-8 -*-
from typing import List


class Todo():
    def __init__(self, uuid: str, title: str, content: bytes):
        self.uuid = uuid
        self.title = title
        self.content = content


class TodoList():
    def __init__(self):
        self._todo_list: List[Todo] = []

    def __iter__(self):
        for todo in self._todo_list:
            yield todo