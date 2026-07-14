from google import genai
from google.genai import types
import json
from todo_service.ToDoService import ToDoService


class Gemini:
    def __init__(
        self, 
        api_key: str, 
        tools_metadata: list[types.ToolDict],
    ):

        self.api_key = api_key
        self.models = {
            # "2.5": "gemini-2.5-flash",
            "3.1": "gemini-3.1-flash-lite",
            "3.5": "gemini-3.5-flash"
        }
        self.active_model = self.models.get("3.1")
        self.tools = [tool for tool in tools_metadata]
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            print("Error instantiating client, please check API_KEY")
            return {
                "status": "fail",
                "text": f"Error instantiating client: {e}"
            }

    def build_tool(self, tool: dict):
        return {
            "type": "function",
            "name": metadata["name"],
            "description": metadata["description"],
            "parameters": metadata["parameters"],
        }

    # add_todo_tool = {
    #     "type": "function",
    #     "name": "add_todo",
    #     "description": "Adds an item to the user's todo list.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "item": {
    #                 "type": "string",
    #                 "description": "The todo item"
    #             }
    #         },
    #         "required": ["item"]
    #     }
    # }



    def basic_interact(input: str):
        # Single interaction containing the whole response
        interaction = self.client.interactions.create(
            model=self.active_model,
            input="Add cycling to my todo list",
            tools=[add_todo_tool]
        )
        return interaction

    def stream_interact(input):
        # Stream of responses
        stream = self.client.interactions.create(
            model=self.active_model,
            input="Explain how AI works in a few words",
            stream=True
        )

        for event in stream:
            print("event type: ", type(event))
            print("event dir: ", dir(event))
        for event in stream:

            match event.event_type:

                case "interaction.created":
                    print("Started")

                case "step.delta":
                    if hasattr(event.delta, "text"):
                        print(event.delta.text, end="")

                case "interaction.completed":
                    print()
                    print(event.interaction.usage)

        print(interaction.output_text)
        return stream

    def basic_function_interact(self, input: str):
        print(json.dumps(self.tools, indent=2))
        interaction = self.client.interactions.create(
            model=self.active_model,
            input=input,
            tools=self.tools
        )
        
        function_call_step = next(s for s in interaction.steps if s.type == "function_call")
        name = function_call_step.name
        id = function_call_step.id
        if name == "add_item_to_list":
            print("'add_item_to_list' called args:")
            arguments = function_call_step.arguments
            print(arguments)
            todo_service = ToDoService()
            result = todo_service.add_item_to_list(**arguments)
        
        payload = [{
                "type": "function_result",
                "name": name,
                "call_id": id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            }]
        print(payload)
        interaction_2 = self.client.interactions.create(
            model=self.active_model,
            input=payload,
            tools=self.tools,
            previous_interaction_id=interaction.id,
        ) 


    def interact(
        input: any, 
        stream: bool = False, 
        tool_names: list[str] = []
    ):

        match function:
            case False:
                match stream:
                    case True:
                        self.stream_interact(input=input)
                    case False:
                        self.basic_interact(input=input)
            case True:
                match stream:
                    case False:
                        self.basic_tool_interact(input=input, tools=tool_names)
                    case True:
                        print("Not implemented yet")
        



def main():
    secret_path = "./backend/secrets.json"

    with open(secret_path, 'r') as file:
        data = json.load(file)
        print("Data: ", data)
        api_key = data.get("api_key")
        if (not api_key):
            return

    todos = ["Shower"]

    def add_todo(item: str):
        todos.append(item)
        return {
            "success": True
        }



    add_todo_tool = {
        "type": "function",
        "name": "add_todo",
        "description": "Adds an item to the user's todo list.",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The todo item"
                }
            },
            "required": ["item"]
        }
    }


    client = genai.Client(api_key=api_key)

    print("Original todos: ", todos)
    # Single interaction containing the whole response
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input="Add cycling to my todo list",
        tools=[add_todo_tool]
    )
    
    function_call_step = next(s for s in interaction.steps if s.type == "function_call")
    name = function_call_step.name
    id = function_call_step.id
    if name == "add_todo":
        print("add_todo called args:")
        argument = function_call_step.arguments.get("item")
        print(argument)
        result = add_todo(argument)
    
    payload = [{
            "type": "function_result",
            "name": name,
            "call_id": id,
            "result": [{"type": "text", "text": json.dumps(result)}],
        }]
    print(payload)
    interaction_2 = client.interactions.create(
        model="gemini-3.5-flash",
        input=payload,
        tools=[add_todo_tool],
        previous_interaction_id=interaction.id,
    ) 

    print("final output text: ", interaction_2.output_text)
    print("updated todos: ", todos)


    # Stream of responses
    # stream = client.interactions.create(
    #     model="gemini-3.5-flash",
    #     input="Explain how AI works in a few words",
    #     stream=True
    # )

    # for event in stream:
    #     print("event type: ", type(event))
    #     print("event dir: ", dir(event))
    # for event in stream:

    #     match event.event_type:

    #         case "interaction.created":
    #             print("Started")

    #         case "step.delta":
    #             if hasattr(event.delta, "text"):
    #                 print(event.delta.text, end="")

    #         case "interaction.completed":
    #             print()
    #             print(event.interaction.usage)

    # print(interaction.output_text)

if __name__ == "__main__":
    main()




