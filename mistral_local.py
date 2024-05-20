from openai import OpenAI
import base64


def mistral_complete(prompt_text):
    gpt_response = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        messages=[{"role": "system",
                   "content":   "Du bist ein hilfreicher assistent."},
                  {"role": "user", "content": prompt_text}])
    return gpt_response.choices[0].message.content


def mistral_chat():
    history = [
        {"role": "system",
         "content": "You are an intelligent assistant. You always provide well-reasoned answers that are "
                    "both correct and helpful."},
        {"role": "user",
         "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]

    while True:
        completion = client.chat.completions.create(
            model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}

        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)

        # Uncomment to see chat history
        # import json
        # gray_color = "\033[90m"
        # reset_color = "\033[0m"
        # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        # print(json.dumps(history, indent=2))
        # print(f"\n{'-'*55}\n{reset_color}")
        history.append({"role": "user", "content": input("> ")})


def mistral_vision():
    # Ask the user for a path on the filesystem:
    path = input("Enter a local filepath to an image: ")

    # Read the image and encode it to base64:
    base64_image = ""
    path.replace("\\", "\\\\")
    try:
        image = open(path.replace("'", ""), "rb").read()
        base64_image = base64.b64encode(image).decode("utf-8")
    except Exception as e:
        print(e)
        print("Couldn't read the image. Make sure the path is correct and the file exists.")
        exit()

    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        messages=[
            {
                "role": "system",
                "content": "This is a chat between a user and an assistant. "
                           "The assistant is helping the user to describe an image.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
        stream=True
    )

    for chunk in completion:
        print(chunk)
        a = input()
        """
        debugging in progress
        need to load vision modell
        
        """
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == '__main__':
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    #print(mistral_complete(input()))
    #mistral_chat()
    #mistral_vision()
    #print(mistral_embedding("the color yellow"))
