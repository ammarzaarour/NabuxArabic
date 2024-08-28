import streamlit as st
from streamlit_chat import message
from backend import run_llm


st.header("LangChain🦜🔗 ALI ChatBOT")



if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button(
    "Submit"
)



if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"]
        )

        

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(generated_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response))


# Display the chat history with unique keys
if st.session_state["chat_answers_history"]:
    for i, (generated_response, user_query) in enumerate(
        zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"])
    ):
        # Unique key for each user message
        message(user_query, is_user=True, key=f"user_msg_{i}")
        # Unique key for each AI response
        message(generated_response, key=f"ai_msg_{i}")
        
        