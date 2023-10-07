import openai
import os
import requests
import datetime
import base64
import time

# Define A function to open a file and return its contents as a string


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Define a function to save content to a file


def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)


# set the OpenAi API key
api_key = 'your openAi API key'

# stable diffusion api key
sd_api_key = 'your stable diffusion api key'

# Initialize two empty lists to store the conversations for each chatbot.
conversation1 = []
conversation2 = []

# Read the content of the files containing the chatbot's prompts
chatbot1 = open_file('chatbot1.txt')
chatbot2 = open_file('chatbot2.txt')

# Define a function to make an API call to the OpenAI Chatcompletion endpoint


def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.75,
            frequency_penalty=0.2, presence_penalty=0, max_retries=5):
    openai.api_key = api_key
    conversation.append({"role": "user", "content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])

    retries = 0
    while retries <= max_retries:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                messages=messages_input,
            )

            chat_response = completion['choices'][0]['message']['content']
            conversation.append(
                {"role": "assistant", "content": chat_response})
            return chat_response
        except openai.error.RateLimitError:
            print(f"Rate limit error, retrying in {2**retries} seconds...")
            time.sleep(2**retries)
            retries += 1
    raise Exception(
        "Failed to get a response from the API after multiple retries.")

# Define a function to generate images using the Stability API


def generate_image(api_key, text_prompt, height=512, width=512, cfg_scale=7,
                   clip_guidance_preset="FAST_BLUE", steps=50, samples=1):

    api_host = 'https://api.stability.ai'
    engine_id = "stable-diffusion-xl-beta-v2-2-2"

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_prompt
                }
            ],
            "cfg_scale": cfg_scale,
            "clip_guidance_preset": clip_guidance_preset,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    image_data = data["artifacts"][0]["base64"]

    # Save the generated image to a file with a unique name in the specified folder
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Read the output directory from a file
    with open("output_dir.txt", "r") as f:
        directory = f.read().strip()
    if not os.path.exists(directory):
        os.makedirs(directory)
    image_filename = os.path.join(
        directory, f"generated_image_{timestamp}.png")

    with open(image_filename, "wb") as f:
        f.write(base64.b64decode(image_data))

    return image_filename


num_turns = 10  # Number of turns for each chatbot (you can adjust this value)

# start the conversation with ChatBot1's first message
user_message = "Hello Agent007, I am agentX. How can i help you?"

# Update the loop where chatbot talk to each other.
for i in range(num_turns):
    print(f"AgentX: {user_message}\n\n")
    save_file("ChatLog.txt", "AgentX: " + user_message + "\n\n")
    response = chatgpt(api_key, conversation1, chatbot1, user_message)
    user_message = response

    if "generate_image:" in user_message:
        image_prompt = user_message.split("generate_image:")[1].strip()
        image_path = generate_image(sd_api_key, image_prompt)
        print(f"Generated image: {image_path}")

    print(f"Agent007: {user_message}\n\n")
    save_file("ChatLog.txt", "Agent007: " + user_message + "\n\n")
    response = chatgpt(api_key, conversation2, chatbot2, user_message)
    user_message = response

    if "generate_image:" in user_message:
        image_prompt = user_message.split("generate_image:")[1].strip()
        image_path = generate_image(sd_api_key, image_prompt)
        print(f"Generated image: {image_path}")


def get_output_dir():
    with open("output_dir.txt", "r") as f:
        return f.read().strip()


directory = get_output_dir()
