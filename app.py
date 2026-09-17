import streamlit as st
# pyrefly: ignore [missing-import]
import groq as groq
from dotenv import load_dotenv 
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=api_key)

#sreamlit page conflict
st.set_page_config(
    page_title="GROQ AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* ---------------- Background ---------------- */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 45%,
        #1e3a8a 100%
    );
    color: #F8FAFC;
}

/* Hide Streamlit Menu */
#MainMenu, footer, header{
    visibility:hidden;
}

/* ---------------- Sidebar ---------------- */
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #111827,
        #0f172a
    );
    border-right:1px solid rgba(255,255,255,.08);
}

/* Sidebar Text */
section[data-testid="stSidebar"] *{
    color:#E2E8F0;
}

/* ---------------- Buttons ---------------- */
.stButton>button{
    width:100%;
    border-radius:12px;
    background:#2563EB;
    color:white;
    border:none;
    font-weight:600;
    transition:.25s;
}

.stButton>button:hover{
    background:#3B82F6;
}

/* ---------------- Select Box ---------------- */
div[data-baseweb="select"]{
    background:#1E293B;
    border-radius:12px;
}

/* ---------------- Slider ---------------- */
.stSlider{
    color:#60A5FA;
}

/* ---------------- Chat Messages ---------------- */
div[data-testid="stChatMessage"]{
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:14px;
}

/* ---------------- Chat Input ---------------- */
div[data-testid="stChatInput"]{
    background:#111827;
    border-radius:18px;
    border:1px solid rgba(59,130,246,.4);
}

/* Input Box */
textarea{
    color:white !important;
}

/* ---------------- Scrollbar ---------------- */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#3B82F6;
    border-radius:10px;
}

/* ---------------- Mobile ---------------- */
@media (max-width:768px){

    h1{
        font-size:28px !important;
    }

    .stButton>button{
        font-size:14px;
    }

    div[data-testid="stChatMessage"]{
        padding:10px;
        font-size:15px;
    }

}

</style>
""", unsafe_allow_html=True)

#sidebar
st.sidebar.markdown("# ⚙ AI Settings")
st.sidebar.markdown("---")
model = st.sidebar.selectbox(
    "choose Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 100, 2048, 1024)
if st.sidebar.button("class Chat"):
    st.session_state.messages =[]
if "messages" not in st.session_state:
        st.session_state.messages=[]
st.sidebar.markdown("---")

st.sidebar.success("🟢 Online")

st.sidebar.info(f"Model\n\n{model}")

st.sidebar.markdown(
"""
### ⚡ Powered By

Groq

### 🤖 Version

Llama 3
"""
)


#Display chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
prompt = st.chat_input("Ask Anything....")
if prompt:
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model, 
                messages = st.session_state.messages, 
                temperature = temperature, 
                max_tokens = max_tokens
            )

            reply= response.choices[0].message.content
            
            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            }
            )
st.markdown("""
<hr>

<center>

⚡ Powered by <b>Groq</b>



</center>
""", unsafe_allow_html=True)