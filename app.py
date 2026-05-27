import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Med-O",
    page_icon="🩺",
    layout="centered"
   
)

st.markdown("""
<style>

.stApp {
    background-color: #d1296f;
}

h1, h2, h3, p, div {
    color: black;
}

[data-testid="stSidebar"] {
    background-color: #f3b2d0;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

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


if menu == "Chat Kesehatan":

    system_prompt = """
Kamu adalah Med-O.

Kamu adalah AI kesehatan modern
yang membantu pengguna memahami
informasi kesehatan terbaru dengan bahasa
yang sederhana dan mudah dipahami.

Tugas kamu:
- menjawab pertanyaan kesehatan umum
- menjelaskan gejala dasar
- memberikan edukasi kesehatan
- mengetahui diagnosa umum
- memberikan saran umum untuk kondisi ringan

Penting:
- jangan mengklaim sebagai dokter
- jangan memberikan diagnosis pasti
- sarankan konsultasi tenaga medis
untuk kondisi serius
"""

elif menu == "Edukasi Penyakit":

    system_prompt = """
Kamu adalah Med-O bagian Edukasi Penyakit.

Tugas kamu adalah menjelaskan penyakit
secara edukatif dan terstruktur.

Saat menjelaskan penyakit, gunakan format:
1. Pengertian
2. Penyebab
3. Gejala
4. Pencegahan
5. Pengobatan umum

Gunakan bahasa sederhana dan mudah dipahami.

Penting:
- jangan memberikan diagnosis pasti
- jangan menggantikan dokter
"""

elif menu == "Tips Hidup Sehat":

    system_prompt = """
Kamu adalah Med-O bagian Tips Hidup Sehat.

Tugas kamu:
- memberikan tips hidup sehat
- membantu menjaga pola tidur
- memberikan saran pola makan sehat
- membantu menjaga kesehatan mental
- memberikan motivasi hidup sehat
- memberikan saran olahraga ringan yang sesuai untuk semua usia, kondisi fisik dan menyesuaikan dengan kebutuhan pengguna

Gunakan bahasa yang positif,
ringan, dan mudah dipahami.
"""


st.title("🩺 Med-O")

st.warning(
    "AI ini hanya untuk edukasi "
    "dan bukan pengganti diagnosis dokter."
)


if st.sidebar.button("🗑 Reset Chat"):

    st.session_state.chat_histories[menu] = []

    st.rerun()


if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {
        "Chat Kesehatan": [],
        "Edukasi Penyakit": [],
        "Tips Hidup Sehat": []
    }


for message in st.session_state.chat_histories[menu]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "Tulis pertanyaan kesehatan kamu..."
)

if prompt:

    
    st.session_state.chat_histories[menu].append(
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
                            "content": system_prompt
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                response = completion.choices[0].message.content

                st.markdown(response)

                
                st.session_state.chat_histories[menu].append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:
                st.error(f"Error: {e}")


st.markdown("---")
st.caption("Created with ❤️ by Ameliarndr")