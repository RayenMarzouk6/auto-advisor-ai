import os
import time
import streamlit as st
from markdown_pdf import MarkdownPdf, Section
from langchain_google_genai import ChatGoogleGenerativeAI
from build_agents import run_auto_advisor, validate_business_idea, rephrase_business_idea

import warnings
warnings.filterwarnings("ignore")

# Configuration - Chargez depuis .env ou définissez ici
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ✅ SOLUTION CRITIQUE: Configuration pour CrewAI + LiteLLM
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY  # Pour CrewAI
os.environ["SERPER_API_KEY"] = ""

TEMPERATURE = 0.5


def run_crew(idea_input):
    with st.spinner("🤖 Génération du rapport stratégique en cours..."):
        final_report = run_auto_advisor(idea_input, llm)

    st.session_state["final_report"] = final_report.raw
    st.session_state["final_report_text"] = final_report.raw
    st.success("✅ Analyse terminée avec succès!")

    st.markdown("### 📄 Rapport Stratégique Final")
    with st.chat_message("assistant", avatar="🤖"):
        st.write_stream(stream_output(final_report.raw))

    file_name = export_pdf(final_report.raw)
    st.session_state["file_name"] = file_name


def download_report():
    if "final_report" in st.session_state and "file_name" in st.session_state:
        with open(f'reports/{st.session_state["file_name"]}', "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(
            type="primary",
            label="📥 Télécharger le Rapport PDF",
            data=PDFbyte,
            file_name=st.session_state["file_name"],
            mime='application/octet-stream',
            use_container_width=True
        )


def export_pdf(file, file_name='Rapport_Strategie_Business.pdf'):
    os.makedirs("reports", exist_ok=True)
    pdf = MarkdownPdf()
    pdf.meta["title"] = 'Rapport Business AI-Powered'
    pdf.add_section(Section(file, toc=False))
    pdf.save(f'reports/{file_name}')
    return file_name


def stream_output(report):
    for word in report.split(" "):
        yield word + " "
        time.sleep(0.02)


st.set_page_config(
    page_title="AutoAdvisor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background: #0f0f23; padding: 2rem; }
    .stApp { background: #0f0f23; }
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .custom-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    .custom-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 12px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    .custom-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    .feature-card:hover::before { transform: scaleX(1); }
    .feature-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    .feature-card h3 {
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    .feature-card p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        line-height: 1.6;
    }
    .input-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    .section-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        background: rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.2rem 2.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 1.2rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4) !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.5) !important;
    }
    .stAlert {
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin: 1.5rem 0 !important;
        border-left: 4px solid !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
    }
    .stSuccess {
        border-left-color: #10b981 !important;
        background: rgba(16, 185, 129, 0.1) !important;
    }
    .stWarning {
        border-left-color: #f59e0b !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }
    .stError {
        border-left-color: #ef4444 !important;
        background: rgba(239, 68, 68, 0.1) !important;
    }
    .stInfo {
        border-left-color: #3b82f6 !important;
        background: rgba(59, 130, 246, 0.1) !important;
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        color: white !important;
    }
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: white;
        backdrop-filter: blur(10px);
    }
    .info-box strong { color: #60a5fa; }
    .stSpinner > div { border-color: #667eea !important; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { color: white !important; }
    .main p { color: rgba(255, 255, 255, 0.9) !important; }
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 3rem;
        font-size: 0.95rem;
    }
    label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="custom-header">
        <h1>🧠 AutoAdvisor AI</h1>
        <p>Votre Assistant Stratégique Business propulsé par Gemini</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🎯 Analyse SWOT</h3>
            <p>Analyse complète des forces, faiblesses, opportunités et menaces de votre projet</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📊 Étude de Marché</h3>
            <p>Analyse concurrentielle approfondie et identification des tendances du marché</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>📄 Rapport PDF</h3>
            <p>Export professionnel de votre stratégie business au format PDF</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="input-container">', unsafe_allow_html=True)

api_key = GEMINI_API_KEY
if not api_key:
    st.error("🔑 Clé API Gemini manquante!")
    st.info("Configurez votre clé dans le fichier .env")
    st.stop()

try:
    # ✅ Configuration pour LangChain
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=TEMPERATURE,
        google_api_key=api_key
    )

    st.markdown('<div class="section-title">💡 Décrivez votre idée business</div>', unsafe_allow_html=True)

    user_idea = st.text_area(
        "Votre idée business",
        placeholder="Ex: Application mobile de coaching bien-être pour travailleurs à distance utilisant l'IA pour personnaliser les programmes...",
        height=150,
        key="user_idea"
    )

    if "last_idea" not in st.session_state:
        st.session_state["last_idea"] = user_idea

    if st.session_state["last_idea"] != user_idea:
        st.session_state["last_idea"] = user_idea
        st.session_state.corrected_idea = None
        st.session_state.original_invalid_idea = None
        st.session_state.final_report = None
        st.session_state.file_name = None

    if user_idea.strip():
        if validate_business_idea(user_idea, llm):
            if st.button("🚀 Générer la Stratégie Business"):
                run_crew(user_idea)
                download_report()
        else:
            if "corrected_idea" not in st.session_state or st.session_state.get("original_invalid_idea") != user_idea:
                corrected_idea = rephrase_business_idea(user_idea, llm)
                st.session_state["corrected_idea"] = corrected_idea
                st.session_state["original_invalid_idea"] = user_idea
            else:
                corrected_idea = st.session_state["corrected_idea"]

            if corrected_idea.lower() == "invalid":
                st.error("🚫 L'entrée n'est pas une idée business valide.")
            else:
                st.warning("⚠️ Votre entrée a été reformulée:")
                st.info(f"**💡 Idée Reformulée:** {corrected_idea}")

                if st.button("🚀 Générer la Stratégie Corrigée"):
                    run_crew(corrected_idea)
                    download_report()
    else:
        st.markdown("""
            <div class="info-box">
                💡 <strong>Astuce:</strong> Décrivez votre idée business de manière détaillée.
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Erreur: {str(e)}")
    st.code(f"Type: {type(e).__name__}: {str(e)}", language="python")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <p>✨ Propulsé par Google Gemini AI • 100% Gratuit</p>
    </div>
""", unsafe_allow_html=True)