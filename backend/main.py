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

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input="Explain how AI works in a few words"
    )
    print(interaction.output_text)

if __name__ == "__main__":
    main()




