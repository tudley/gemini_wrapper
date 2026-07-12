from todo_types import TodoItem
from typing import Literal
import datetime
import inspect

class ToDoService:
    def __init__(self):
        self.list = []

    def add_item_to_list(
        self, 
        title: str,
        priority: Literal["high", "medium", "low"]
    ):
        """Adds an item to the user's todo list.

        Args:
            item: The todo item to add.

        Returns:
            Whether the operation succeeded.
        """

        item: TodoItem = {
            "title": title, 
            "priority": priority, 
            "created_at": datetime.now(),
            "completed": False
        }

        if item in self.list:
            return {
                "status": "fail",
                "text": f"list already contains item: {item['title']}"
            }
        self.list.append(item)
        return {
            "status": "success",
            "text": f"item {item} successfully added to list"
        }

    def add_multiple_items_to_list(self, items: list[TodoItem]):#
        """Adds an item to the user's todo list.

        Args:
            items: An array of strings to be added to the todo list

        Returns:
            Whether the operation succeeded.
        """
        for item in items:
            self.add_item_to_list(item)

    def add_item_to_list_metadata(self):
        method = self.add_item_to_list
        signature = inspect.signature(method)

        tool = {
            "name": method.__name__,
            "description": inspect.getdoc(method), # TODO: Split to only first line?
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }

        for key, val in signature.parameters.items():
            print("key: ", key)
            print("val: ", val)
        
            param_obj = {
                key: { # title
                "type": val, # dataType
                "description": val # derived from docstring
                }
            }
            tool['parameters'][key] = param_obj

        return tool


client = ToDoService()
# func = client.add_item_to_list
# sig = inspect.signature(func)
# for name, parameter in sig.parameters.items():
#     print(name)
#     print(parameter.annotation)
#     print(parameter.default)

# print(func.__name__)
# print(inspect.getdoc(func))
client.add_item_to_list_metadata()
