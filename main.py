import streamlit as st


if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

if "chat_history1" not in st.session_state:
        st.session_state["chat_history1"] = []


def intro():
    import streamlit as st
    from Backend.backendA import run_llm
    
    st.write("# أستاذ")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

   
    
    # Display chat messages from history
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in message_data["content"]):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{message_data["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("... اسألني شيئاً"):
        with st.chat_message("user"):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in prompt):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{prompt}</div>', unsafe_allow_html=True)
            else:
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
                # Check if the generated response contains Arabic characters and render it properly
                if any("\u0600" <= char <= "\u06FF" for char in generated_response):  # Check if Arabic
                    st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{generated_response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(generated_response)
            
            st.session_state.messages.append({"role": "assistant", "content": generated_response})


def generate_email():
    import streamlit as st
    from Backend.backendB import run_llm
    
    st.write("# أستاذ")
    
    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
    

    
    # Display chat messages from history
    for message_data in st.session_state.messages1:
        with st.chat_message(message_data["role"]):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in message_data["content"]):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{message_data["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("... اسألني شيئاً"):
        with st.chat_message("user"):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in prompt):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{prompt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(prompt)
        
        st.session_state.messages1.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history1"]
            )
            st.session_state["chat_history1"].append(("human", prompt))
            st.session_state["chat_history1"].append(("ai", generated_response))

            with st.chat_message("assistant"):
                # Check if the generated response contains Arabic characters and render it properly
                if any("\u0600" <= char <= "\u06FF" for char in generated_response):  # Check if Arabic
                    st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{generated_response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(generated_response)
            
            st.session_state.messages1.append({"role": "assistant", "content": generated_response})

        



with st.sidebar:
    
    st.sidebar.image("img/NabuX1.png", width=250) 

    page_names_to_funcs = {
    "أعرف": intro,
    "أفهم": generate_email
    
}
    disabled_status = True
    demo_name = st.sidebar.selectbox("### اختر المستوى", page_names_to_funcs.keys())#,disabled=disabled_status)
    
    #st.markdown("### ALI ChatBOT 🦜🔗")
    #st.markdown("<span style='color: red;'>New</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break
    st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

        # Create a single column layout
    col1, col2, col3 = st.columns([1, 2, 1])  # You can adjust the ratios

    with col2:  # The center column
        # Button for new chat
        if st.button("محادثة جديدة"):
            st.session_state.messages = []  # Clear chat history on new chat
            st.session_state.email_drafts = []
            st.session_state["chat_history"] = []

    # Sidebar footer for license activation
    st.markdown("---")
    st.write("© 2025 أستاذ. All rights reserved.")
    st.markdown(
        """
        <p>
        <a href="https://github.com/" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
        </a>
        <a href="https://t.me/telegram_channel" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png"/>
        </a>
        <a href="" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/email.png"/>
        </a>
        </p>
        """, unsafe_allow_html=True
    )



page_names_to_funcs[demo_name]()



