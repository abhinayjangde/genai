import asyncio
from ollama import AsyncClient, list, show

# async def chat():
#   message = {'role': 'user', 'content': 'who are you ?'}
#   response = await AsyncClient().chat(model='deepseek-r1:1.5b', messages=[message])
#   print(response.message.content)

# asyncio.run(chat())

print(show("deepseek-r1:1.5b"))