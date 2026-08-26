import os, json
from dotenv import load_dotenv
from openai import OpenAI
import subprocess

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# tools
def run_command(command):
    result = os.system(command=command)     
    return result

# available tools
avaiable_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt="""
You are an helpful AI coder who can write, build, code and develop website, mobile apps and lot's of things.
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution, based on the planning,
select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the observation from the tool call resolve the user query.

Rules:
- Follow the output JSON format
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Output JSON Format:
{{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "args": "The input parameter for the function",
}}

Available Tools:
- run_command: Takes a command as input to execute on system and returns ouput

Example:

User Query: What is the weather of new york?
Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "12 Degree Cel" }}
Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

"""

messages = [
    {"role":"system", "content":system_prompt}
]

while True:
    query = input("> ")
    
    if query == "bye" or query == "exit":
        print("Bye!")
        break
    messages.append({"role":"user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            response_format={"type":"json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)

        messages.append({"role":"assistant", "content": json.dumps(parsed_response)})

        if parsed_response["step"] != "output":
            print(f"> {parsed_response}")
            continue
        if parsed_response.get("step") == "plan":
            tool_name = parsed_response.get("function")
            tool_args = parsed_response.get("args")

            if avaiable_tools.get(tool_name, False) != False:
                # calling tool
                output = avaiable_tools[tool_name].get("fn")(tool_args)
                messages.append({"role":"assistant", "content": json.dumps(output)})
                continue
        else:
            print(f"> {parsed_response["content"]}")
            break