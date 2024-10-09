import streamlit as st


if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


def intro():
    import streamlit as st
    from Backend.backend import run_llm
    

    st.write("### LangChain🦜🔗 ALI ChatBOT")
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.json_generated = False
    st.session_state.email_drafts = []
    
    # Display chat messages from history
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("Enter your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history"]
            )
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response))

            with st.chat_message("assistant"):
                st.markdown(generated_response)
            st.session_state.messages.append({"role": "assistant", "content": generated_response})


def generate_email():

    import streamlit as st

   

    run_json()
    st.write("### ALI ChatBOT 🦜🔗 Generate Email")

    if "email_drafts" not in st.session_state:
        st.session_state.email_drafts = []
    
    # Display chat messages from history
    for draft_data in st.session_state.email_drafts:
        with st.chat_message(draft_data["role"]):
            st.markdown(draft_data["content"])
    

    from Backend.rag2 import run_llm2

    if prompt := st.chat_input("Enter your product here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.email_drafts.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm2(
                query=prompt
            )

            with st.chat_message("assistant"):
                st.markdown(generated_response)
            st.session_state.email_drafts.append({"role": "assistant", "content": generated_response})

def run_json():

    from Backend.backend import run_json

    # Add a flag to ensure JSON is generated only once
    if "json_generated" not in st.session_state:
        st.session_state.json_generated = False

    # Check if JSON has not been generated yet
    if not st.session_state.json_generated:
        # Generate and save JSON
        
        json_output = run_json(chat_history=st.session_state["chat_history"])
        file_path = "Database/gathered.json"
        with open(file_path, "w") as file:
            file.write(json_output)
        st.success(f"JSON data has been saved to {file_path}.")
        
        # Set the flag to indicate that JSON has been generated
        st.session_state.json_generated = True
        st.session_state.messages = []  # Clear chat history on new chat
        st.session_state["chat_history"] = []
        



with st.sidebar:
    
    st.sidebar.image("img/ali.png", width=250) 

    page_names_to_funcs = {
    "Gather Information": intro,
    "Generate Email": generate_email
    
}
    disabled_status = True
    demo_name = st.sidebar.selectbox("### Choose a page", page_names_to_funcs.keys())#,disabled=disabled_status)
    
    #st.markdown("### ALI ChatBOT 🦜🔗")
    #st.markdown("<span style='color: red;'>New</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

        # Create a single column layout
    col1, col2, col3 = st.columns([1, 2, 1])  # You can adjust the ratios

    with col2:  # The center column
        # Button for new chat
        if st.button("New Chat"):
            st.session_state.messages = []  # Clear chat history on new chat
            st.session_state.email_drafts = []
            st.session_state["chat_history"] = []

    # Sidebar footer for license activation
    st.markdown("---")
    st.write("© 2024 Ali Chatbot. All rights reserved.")
    st.markdown(
        """
        <p>
        <a href="https://github.com/ammarzaarour/Chatbot-OpenAI-RAG" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
        </a>
        <a href="https://t.me/telegram_channel" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png"/>
        </a>
        <a href="ammar.rushdi.zaarour@gmail.com" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/email.png"/>
        </a>
        </p>
        """, unsafe_allow_html=True
    )



page_names_to_funcs[demo_name]()



