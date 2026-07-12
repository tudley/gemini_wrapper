from todo_types import TodoItem
from typing import Literal, get_origin, get_args
import datetime
import inspect
from docstring_parser import parse, Docstring

class ToDoService:
    def __init__(self):
        self.list = []

    def add_item_to_list(
        self, 
        title: str,
        priority: Literal["high", "medium", "low"],
        complete: bool = False
    ):
        """Adds an item to the user's todo list.

        Args:
            title: The title of the item to be added to the todo list
            priority: The priority of the item being added to the todo list

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


        docstring = inspect.getdoc(method)
        parsed_docstring = parse(docstring)

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

        for arg_title, parameter in signature.parameters.items():
            print("key: ", arg_title)
            print("val: ", parameter)
            arg_type = annotation_to_str(parameter.annotation)
            arg_description = get_arg_description(arg_title, parsed_docstring)
            required = True if parameter.default is inspect._empty else False
            if required:
                tool['parameters']['required'].append(arg_title)
            
        
            param_obj = {
                arg_title: { # title
                "type": arg_type, # dataType
                "description": arg_type # derived from docstring
                }
            }
            tool['parameters'][arg_title] = param_obj

        return tool

def annotation_to_str(annotation):
    if annotation == str:
        return "string"

    if annotation == int:
        return "integer"

    if annotation == bool:
        return "boolean"

    if get_origin(annotation) is Literal:
        values = list(get_args(annotation))
        return {
            "type": "string",
            "enum": values
        }

    return {"type": "object"}

    return "object"

def get_arg_description(
    arg_title: str, 
    parsed_docstring: Docstring
):
    for param in parsed_docstring.params:
        if param.arg_name == arg_title:
            return param.description

# def is_required(parsed_docstring: Docstring)

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
