import streamlit as st

# Add title at the very top
st.title("أستاذ")  # Or any other title you want

# Apply more comprehensive RTL styling
st.markdown("""
<style>
.stChatInput {
    direction: rtl;
    text-align: right;
}
/* Target the input field directly */
.stChatInput input, .stChatInput textarea {
    direction: rtl;
    text-align: right;
}
/* Target any child elements of the chat input */
.stChatInput * {
    direction: rtl;
}
/* This might help with the button positioning */
.stChatInput div[data-testid="stChatInputSubmitButton"] {
    left: 0.5rem;
    right: auto;
}
</style>
""", unsafe_allow_html=True)

# Your chat input with Arabic placeholder
if prompt := st.chat_input("... اسألني شيئاً"):
    # Process the input
    st.write(f"You asked: {prompt}")