from google import genai
import json

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




