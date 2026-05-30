import streamlit as st
from openai import OpenAI
import fitz

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

st.sidebar.success(
    "🩺 Health Analysis Platform"
)


menu = st.sidebar.selectbox(
    "Pilih fitur",
    [
        "BMI Calculator",
        "Calorie Calculator",
        "Lab Interpretation",
        "AI Lab Analyzer"
    ]
)

st.sidebar.info(
    """
Med-O membantu pengguna:
• Menghitung BMI
• Menghitung kebutuhan kalori
• Menginterpretasikan hasil laboratorium
• Menganalisis laporan kesehatan berbasis AI
"""
)


if menu == "BMI Calculator":

    st.title("📏 BMI Calculator")

    berat = st.number_input(
        "Berat badan (kg)",
        min_value=1.0
    )

    tinggi = st.number_input(
        "Tinggi badan (cm)",
        min_value=1.0
    )

    if st.button("Hitung BMI"):

        bmi = berat / ((tinggi / 100) ** 2)

        st.subheader(f"BMI: {bmi:.2f}")

        if bmi < 18.5:
            st.warning("Berat badan kurang")

        elif bmi < 25:
            st.success("Berat badan normal")

        elif bmi < 30:
            st.warning("Kelebihan berat badan")

        else:
            st.error("Obesitas")

elif menu == "Calorie Calculator":

    st.title("🔥 Calorie Calculator")

    gender = st.selectbox(
        "Jenis Kelamin",
        ["Pria", "Wanita"]
    )

    umur = st.number_input(
        "Umur",
        min_value=1
    )

    berat = st.number_input(
        "Berat Badan (kg)",
        min_value=1.0,
        key="bb_kalori"
    )

    tinggi = st.number_input(
        "Tinggi Badan (cm)",
        min_value=1.0,
        key="tb_kalori"
    )

    aktivitas = st.selectbox(
        "Aktivitas",
        [
            "Sangat Ringan",
            "Ringan",
            "Sedang",
            "Berat"
        ]
    )

    if st.button("Hitung Kalori"):

        if gender == "Pria":

            bmr = (
                10 * berat +
                6.25 * tinggi -
                5 * umur + 5
            )

        else:

            bmr = (
                10 * berat +
                6.25 * tinggi -
                5 * umur - 161
            )

        faktor = {
            "Sangat Ringan": 1.2,
            "Ringan": 1.375,
            "Sedang": 1.55,
            "Berat": 1.725
        }

        kalori = bmr * faktor[aktivitas]

        st.success(
            f"Kebutuhan kalori harian sekitar {kalori:.0f} kkal"
        )

  elif menu == "Lab Interpretation":

    st.title("🧪 Lab Interpretation")

    hb = st.number_input(
        "Hemoglobin (g/dL)",
        min_value=0.0
    )

    gula = st.number_input(
        "Gula Darah Puasa (mg/dL)",
        min_value=0.0
    )

    kolesterol = st.number_input(
        "Kolesterol Total (mg/dL)",
        min_value=0.0
    )

    if st.button("Analisis"):

        if hb < 12:
            st.warning(
                "Hemoglobin rendah, dapat berkaitan dengan anemia."
            )

        else:
            st.success(
                "Hemoglobin dalam rentang normal."
            )

        if gula > 125:
            st.warning(
                "Gula darah lebih tinggi dari normal."
            )

        else:
            st.success(
                "Gula darah dalam rentang normal."
            )

        if kolesterol > 200:
            st.warning(
                "Kolesterol total tinggi."
            )

        else:
            st.success(
                "Kolesterol dalam rentang normal."
            )

  elif menu == "AI Lab Analyzer":

    st.title("📄 AI Lab Analyzer")

    uploaded_file = st.file_uploader(
        "Upload PDF hasil lab",
        type=["pdf"]
    )

    if uploaded_file:

        pdf_text = ""

        doc = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        for page in doc:
            pdf_text += page.get_text()

        st.success("PDF berhasil dibaca")

        if st.button("Analisis dengan AI"):

            with st.spinner(
                "Med-O sedang menganalisis..."
            ):

                completion = client.chat.completions.create(
                    model="openai/gpt-4o-mini",

                    messages=[
                        {
                            "role": "system",
                            "content": """
Kamu adalah analis hasil laboratorium medis.

Tugas:
- membaca hasil laboratorium
- menjelaskan parameter penting
- menandai nilai abnormal
- memberikan edukasi sederhana

Jangan memberikan diagnosis pasti.
"""
                        },
                        {
                            "role": "user",
                            "content": pdf_text
                        }
                    ]
                )

                hasil = completion.choices[0].message.content

                st.markdown(hasil)

st.title("🩺 Med-O")


st.info(
    "Med-O membantu memahami informasi kesehatan secara edukatif. Untuk diagnosis dan keputusan medis, konsultasikan dengan dokter atau tenaga kesehatan."
)


if st.sidebar.button("🗑 Reset Chat"):

    st.session_state.chat_histories[menu] = []

    st.rerun()


if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {
        "BMI Calculator": [],
        "Calorie Calculator": [],
        "Lab Interpretation": [],
        "AI Lab Analyzer": []
    }


for message in st.session_state.chat_histories[menu]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "Ask here to know..."
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

        with st.spinner("Analyzing..."):

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