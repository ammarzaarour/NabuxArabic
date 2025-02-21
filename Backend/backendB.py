from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableMap
from typing import Any, Dict, List

# Load environment variables from .env file
load_dotenv()


template = """
 You are a helpful teacher called AI Teacher (استاذ الذكاء الاصطناعي الخاص), your task is to teach AI to people who know few things about AI. Give sophisticated examples
        with equations and real data examples.
          . reply to users in Arabic. With only 12 to 15 sentences.
        Answer according to this chat history {chat_history}

   when the user asks about algorithms in AI, answer it and link it to how we can use AI in the real example.

Important: Don't answer anything not related to AI.
Don’t answer anything about the code. If the user asks you, you reply that this feature will be available later at a higher request level.  

   Question: {question}

"""


prompt = ChatPromptTemplate.from_template(template)

# Initialize the Gemini model using LangChain integration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

# Function to handle user input
# Function to handle user input and invoke the chain
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    chain = RunnableMap({
    "chat_history": lambda x: x["chat_history"],
    "question": lambda x: x["question"]
}) | prompt | llm

    result = chain.invoke(input={"question": query, "chat_history": chat_history})
    return result.content
    
