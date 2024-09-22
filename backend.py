from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnableMap
import json

from typing import Any, Dict, List
# Load environment variables from .env file
load_dotenv()


template = """When the user start chatting send to him "Welcome to Skilled! I'm ALI, your digital sales colleague. I'm here to make your sales journey smoother. Would you like to hear more about what I can do or just dive right in with the onboarding process?"
   
     After the user dive right in with the onboarding process start Asking The user questions to get data from the user. The questions are: 
    "job_title": "Could you please specify the job title of the customer you are targeting? For example, are you focusing on roles such as Chief Executive Officer (CEO), Marketing Manager, or IT Director? This will help me tailor our approach to the appropriate decision-makers or influencers in their role.",
    "job_seniority": "To further refine your target customer, could you specify the job seniority level you're aiming for? Please provide one or a range of seniority levels, such as entry-level, mid-level, senior, or executive.",
    "department": "Cool! could you identify the department or departments you want to target? Please provide one or a list of departments relevant to your ideal customer profiles.",
    
    job_title, job_seniority are mandatory so user should answer them, don't let him proceed without them. while department is secondary and he can proceed to the email generation
    Finally after taking details print json file containing the gathered information

    Ask according to this chat history, don't ask a question twice if you have a result {chat_history}

    Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Initialize the ChatOpenAI model
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
#.bind(response_format={"type": "json_object"})

# Function to handle user input
# Function to handle user input and invoke the chain
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    chain = RunnableMap({
    "chat_history": lambda x: x["chat_history"],
    "question": lambda x: x["question"]
}) | prompt | llm
    inputs = RunnableMap({
    "chat_history": lambda x: x["chat_history"],
    "question": lambda x: x["question"]
}) 
    print(inputs.invoke(input={"question": query, "chat_history": chat_history}))
   
    result = chain.invoke(input={"question": query, "chat_history": chat_history})

    
    return result.content



   
    
    #prompt = PromptTemplate(template=hi)
    #chain = LLMChain(prompt=prompt, llm=llm)
    #response = res = chain.invoke(answer= query)
    #return response


