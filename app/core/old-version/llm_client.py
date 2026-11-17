
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

load_dotenv()

def ask_llm(question):

    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    messages = [
        SystemMessage(
            content="You are a helpful company AI assistant."
        ),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)

    return response.content


if __name__ == "__main__":

    question = "What is prompt injection?"

    answer = ask_llm(question)

    print("\nQuestion:", question)
    print("\nLLM Answer:", answer)
