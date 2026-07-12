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


    client = genai.Client(api_key=api_key)

    # Single interaction containing the whole response
    # interaction = client.interactions.create(
    #     model="gemini-3.5-flash",
    #     input="Explain how AI works in a few words"
    # )
    # print(interaction.output_text)


    # Stream of responses
    stream = client.interactions.create(
        model="gemini-3.5-flash",
        input="Explain how AI works in a few words",
        stream=True
    )

    for event in stream:
        print("event type: ", type(event))
        print("event dir: ", dir(event))
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




