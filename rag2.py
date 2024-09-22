from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import Any, Dict, List

from langchain import hub
from langchain.prompts import PromptTemplate  # Import PromptTemplate class
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Initialize embeddings and document search
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
docsearch = PineconeVectorStore(index_name="demo", embedding=embeddings)

# Initialize the chat model
chat = ChatOpenAI(verbose=True, temperature=0)

def read_static_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        static_data = json.load(file)  # Load the JSON content into a Python dictionary
    return static_data

# Example usage: Reading static data from the JSON file
static_data = read_static_data('raw_response.json')
# Define the static context you want to add to every prompt
static_context = json.dumps(static_data, indent=4)

static_context = static_context.replace("{", "").replace("}", "")
print(static_context)

# Create a proper PromptTemplate with both context and input
# 'context' will represent the documents retrieved, and 'input' is the user query
prompt_template = PromptTemplate(
    input_variables=["input", "context"],
    template=f"""According to this gathered information create an email to the targeted audience explaining to them about the product according to this context retrieved
    {static_context}

    Retrieved Documents:
    {{context}}

    User Query: {{input}}
    Assistant Response:
    """
)

# Pulling prompts from LangChain's hub
rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Now, create the stuff_documents_chain with the PromptTemplate
stuff_documents_chain = create_stuff_documents_chain(chat, prompt_template)

# Create the history-aware retriever
history_aware_retriever = create_history_aware_retriever(
    llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
)

# Create the QA chain with the modified prompt
qa = create_retrieval_chain(
    retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
)

def run_llm2(query: str):
# Invoke the chain with user input
    result = qa.invoke(input={"input":query})

# Print the result, which should include static context plus the user input
    return result["answer"]


