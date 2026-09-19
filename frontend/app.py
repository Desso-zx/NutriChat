import streamlit as st

from api_client import ask_question, check_backend_health

st.set_page_config(page_title="NutriChat", page_icon="🥗")

st.title("🥗 NutriChat")
st.caption("Ask a question about nutrition and healthy eating — answers are grounded in official USDA/WHO guidance.")

if not check_backend_health():
    st.error("Backend is not reachable. Make sure it's running: `uvicorn app.main:app --reload` in the backend/ folder.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

question = st.chat_input("Ask a nutrition question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = ask_question(question)
                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)
                if sources:
                    st.caption("Sources: " + ", ".join(sources))

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })
            except Exception as e:
                error_msg = "Sorry, something went wrong answering that. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})