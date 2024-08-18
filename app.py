# WARNING: The following two lines are ONLY for Streamlit.
# Remove them from local install!!
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
import sys

# from embedchain import App
from embedchain.pipeline import Pipeline as App

from embedchain.loaders.github import GithubLoader

@st.cache_resource
def embedchain_bot():
    loader = GithubLoader(
    config={
        "token":st.secrets["GHPAT_TOKEN"]
        }
    )
    app = App.from_config(config_path="config.yaml")
    
    # Put any github repo you can then refer as templates!
    app.add("repo:goldzulu/coinweb-hello-world type:repo", data_type="github", loader=loader)
    app.add("repo:goldzulu/coinweb-string-processor type:repo", data_type="github", loader=loader)
    
    return app

# Add a sidebar
st.sidebar.title("Starter Templates")
st.sidebar.write("Hello World")
st.sidebar.write("String Processor")

st.title("AI Dapp Builder")
st.caption("A Coinweb Dapp Builder's Companion! 🚀")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are a Coinweb Blockchain Dapp Builder's companion\n
            You primary task is a Dapp builder assistant. You use Coinweb Hello World and String Processor template as a starting point when possible.\n\n
            When advising changes, try to make it easier by giving the file structure of the Dapp the user need to build.\n\n
            Describe any changes they need to do, with references to the original files if it is a change needed possible.\n
            """,
            "role": "assistant",
            "content": """
            Hi! I'm your Coinweb Dapp companion. I can help you build you next Coinweb Dapp.\n
            I currently the Hello World and String Processory Dapps.\n\n
            You can use these templates as a starting point for your Dapp\n\n
            Describe your Dapp and ask me what files you need to change from the templates.\n
            
            I can also learn new things regarding coinweb like a pdf, webpage, etc just type `/add <source>`.\n
            I will try my best to learn it and help you with it.\n
            """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):
    app = embedchain_bot()

    if prompt.startswith("/add"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
        prompt = prompt.replace("/add", "").strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Adding to knowledge base...")
            app.add(prompt)
            message_placeholder.markdown(f"Added {prompt} to knowledge base!")
            st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
            st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        for response in app.chat(prompt):
            msg_placeholder.empty()
            full_response += response

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
