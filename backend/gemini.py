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
    for step in interaction.steps:
        if step.type == "function_call":
            print("Function call found")
            if step.name == "add_todo":
                print("add_todo called args:")
                argument = step.arguments.get("item")
                print(argument)
                add_todo(argument)

    print("output text: ", interaction.output_text)
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




