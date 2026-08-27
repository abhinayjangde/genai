from ollama import chat, ChatResponse

stream: ChatResponse = chat(
    model="deepseek-r1:1.5b",
    messages=[
        {"role":"user", "content":"how many keys in keyboard ?"}
    ],
    stream=True
)

for chunk in stream:
    print(chunk.message.content, end="", flush=True )
