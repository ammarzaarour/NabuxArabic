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
docsearch = PineconeVectorStore(index_name="geozar", embedding=embeddings)

# Initialize the chat model
chat = ChatOpenAI(verbose=True, temperature=0)

def read_static_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        static_data = json.load(file)  # Load the JSON content into a Python dictionary
    return static_data





def run_llm2(query: str):
    # Example usage: Reading static data from the JSON file
    static_data = read_static_data('Database/gathered.json')
    # Define the static context you want to add to every prompt
    gathered_info = json.dumps(static_data, indent=4)

    gathered_info = gathered_info.replace("{", "").replace("}", "")
    #print("static one"+gathered_info)

    # Create a proper PromptTemplate with both context and input
    # 'context' will represent the documents retrieved, and 'input' is the user query
    prompt_template = PromptTemplate(
        input_variables=["input", "context"],
        template=f"""If the user query is relevant to the context, create an email. Otherwise, return a message indicating that the query does not match the context.

    If the user query does not fit the context:

        - Return a response like: "The query is not related to the product or context provided. Please provide a product-related query."

    Else:

        - According to this gathered information {gathered_info}, create an email to the targeted audience explaining the product according to this context retrieved.
        - Use this gathered info in email generation.
        Retrieved Documents:
        {{context}}

        Don't make up information. If the user query does not fit the context, provide feedback instead.

        User Query: {{input}}
        Assistant Response:
        """
    )


    # Now, create the stuff_documents_chain with the PromptTemplate
    stuff_documents_chain = create_stuff_documents_chain(chat, prompt_template)


    # Create the history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=prompt_template
    )


    # Create the QA chain with the modified prompt
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    # Invoke the chain with user input
    result = qa.invoke(input={"input":query})
    #print(result)
    # Print the result, which should include static context plus the user input
    return result["answer"]


