from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    # Initialize chat model
    model = ChatOllama(model="mistral")
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a very knowledgeable chemist, you can answer difficult questions."),
        ("human", "{question}")
    ])
    
    # Create chain
    chain = prompt | model
    
    # Store chain in user session
    cl.user_session.set("chain", chain)

@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    msg = cl.Message(content="")
    
    # Start streaming response
    async for chunk in chain.astream({"question": message.content}):
        if chunk.content:
            await msg.stream_token(chunk.content)
    
    # Send final message
    await msg.send()