import streamlit as st
from chatbot import STORE_INFO, load_faq_data, initialize_model, create_prompt_template
from langchain_core.runnables import RunnablePassthrough

# Set up the page
st.set_page_config(
    page_title="R.O.M.E. Chatbot",
    page_icon="🤖"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display store info in sidebar
with st.sidebar:
    st.title(STORE_INFO['name'])
    st.write(STORE_INFO['history'])
    st.write(f"**Mission:** {STORE_INFO['mission']}")
    st.write("**Customer Support:**")
    st.write(f"- Email: {STORE_INFO['customer_support']['email']}")
    st.write(f"- Phone: {STORE_INFO['customer_support']['phone']}")
    st.write(f"- Hours: {STORE_INFO['customer_support']['working_hours']}")

# Main chat interface
st.title(f"Welcome to {STORE_INFO['name']} Support")
st.caption("How can I help you today?")

# Initialize the chatbot (only once)
if "chatbot_initialized" not in st.session_state:
    with st.spinner("Loading chatbot..."):
        faq_data = load_faq_data("Ecommerce_FAQ_Chatbot_dataset.json")
        llm = initialize_model()
        prompt_template = create_prompt_template(faq_data)
        
        # Create the chain
        chatbot_chain = (
            RunnablePassthrough.assign(faq_context=lambda x: faq_data)
            | prompt_template
            | llm
        )
        st.session_state.chatbot_chain = chatbot_chain
        st.session_state.chatbot_initialized = True

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chatbot_chain.invoke({"question": prompt})
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                error_msg = "Sorry, I encountered an error. Please try again or contact support."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})