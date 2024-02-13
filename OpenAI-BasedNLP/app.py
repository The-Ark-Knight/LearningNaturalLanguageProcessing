import openai
import os
import streamlit as st
from tenacity import retry, wait_random_exponential

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def authenticate():
    # This is a basic authentication for the sake of this example.
    # Replace it with a proper authentication method in your application.
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if username == 'your_username' and password == 'your_password123@!':
        return True
    else:
        return False

@retry(wait=wait_random_exponential(multiplier=1, max=60))
def generate_response(prompt):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completion.choices[0].text

def main():
    if not authenticate():
        st.sidebar.error("Invalid credentials. Please try again.")
        return

    st.title("🤖 My First ChatBot")
    user_input = st.text_input("You: ", "")

    if st.button("Send"):
        if user_input:
            chat_history = st.session_state.get("chat_history", [])
            chat_history.append(f"User: {user_input}")
            response = generate_response(user_input)
            chat_history.append(f"Chatbot: {response}")
            st.session_state["chat_history"] = chat_history

    if st.session_state.get("chat_history"):
        for i, message in enumerate(st.session_state["chat_history"]):
            if i % 2 == 0:
                st.markdown(f"**{message}**", unsafe_allow_html=True)
            else:
                st.markdown(f"{message}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()