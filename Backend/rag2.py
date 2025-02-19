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


def run_llm2(query: str):

    # Create a proper PromptTemplate with both context and input
    # 'context' will represent the documents retrieved, and 'input' is the user query
    prompt_template = PromptTemplate(
        input_variables=["input", "context"],
        template=f"""You are a helpful teacher called Nabux (نبو إكس), you task is to teach AI for people who know AI. Give examples
        with equations and real data examples.
          . reply to users in arabic.
          {{context}}

   when the user asks about algorithm about AI, answer it and link it to how we can use in AI in real example


Important: Don't answer anything not related to AI.

    Question: {{input}}
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


