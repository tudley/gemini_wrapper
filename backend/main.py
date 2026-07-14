from gemini.gemini import Gemini 
from todo_service.ToDoService import ToDoService
import json


def main():

    secret_path = "./backend/secrets.json"

    with open(secret_path, 'r') as file:
        data = json.load(file)
        print("Data: ", data)
        api_key = data.get("api_key")
        if (not api_key):
            return

    todo_service = ToDoService()
    todo_tools = [todo_service.add_item_to_list_metadata()]
    gemini = Gemini(api_key=api_key, tools_metadata=todo_tools)
    gemini.basic_function_interact("Add cycling to my todo list.")


if __name__ == "__main__":
    main()
