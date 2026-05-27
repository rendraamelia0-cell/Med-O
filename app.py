import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Med-O",
    page_icon="🩺",
    layout="centered"
)


api_key = st.secrets["OPENROUTER_API_KEY"]


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


st.sidebar.title("🩺 Med-O")

menu = st.sidebar.selectbox(
    "Pilih fitur",
    [
        "Chat Kesehatan",
        "Edukasi Penyakit",
        "Tips Hidup Sehat"
    ]
)

st.sidebar.info(
    "Med-O membantu pengguna "
    "memahami informasi kesehatan "
    "secara sederhana dan interaktif."
)


st.title("🩺 Med-O")

st.warning(
    "AI ini hanya untuk edukasi "
    "dan bukan pengganti diagnosis dokter."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "Apa keluhan kamu?"
)

if prompt:

    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):

        with st.spinner("Med-O sedang berpikir..."):

            try:

                completion = client.chat.completions.create(
                    model="openai/gpt-4o-mini",

                    messages=[
                        {
                            "role": "system",
                            "content": """
Kamu adalah Med-O.

Kamu adalah AI kesehatan modern
yang membantu pengguna memahami
informasi kesehatan dengan bahasa
yang sederhana dan mudah dipahami.

Tugas kamu:
- menjelaskan penyakit
- memberikan edukasi kesehatan
- membantu mahasiswa kesehatan belajar
- memberikan tips hidup sehat

Penting:
- jangan mengklaim sebagai dokter
- jangan memberikan diagnosis pasti
- sarankan konsultasi tenaga medis
untuk kondisi serius
"""
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                response = completion.choices[0].message.content

                st.markdown(response)

                
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:
                st.error(f"Error: {e}")


st.markdown("---")
st.caption("Created with ❤️ by Ameliarndr")
