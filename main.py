import streamlit as st
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_AVAILABLE = False
model = None

def init_gemini():
    global GEMINI_AVAILABLE, model
    try:
        import google.generativeai as genai
        GEMINI_API_KEY = "AIzaSyDgAQ.Ab8RN6LJArtk9dS_wZF5KfcSMXmG9f-cCncIv6U0oizK50wWVQ"
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        GEMINI_AVAILABLE = True
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Config error: {e}")
        return False

st.set_page_config(page_title="Prompt Skripsi Generator", page_icon="📚", layout="wide")
st.title("📚 Prompt Skripsi Generator")
st.markdown("**Bantuan membuat prompt berkualitas untuk penelitian skripsi Anda**")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Pengaturan")
    field_of_study = st.selectbox("Pilih Bidang Studi:", ["Teknik Informatika", "Teknik Elektro", "Sistem Informasi", "Ilmu Komputer", "Bisnis", "Desain", "Manajemen", "Lainnya"])
    citation_format = st.selectbox("Format Sitasi:", ["APA", "Harvard", "Chicago", "IEEE"])
    tone = st.selectbox("Tone Penulisan:", ["Formal Akademik", "Semi-formal", "Teknis"])
    num_prompts = st.slider("Jumlah prompt yang mau dibuat:", 1, 10, 5)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input Data Skripsi")
    title = st.text_input("Judul Skripsi:", placeholder="Contoh: Implementasi Machine Learning untuk Klasifikasi Sentimen")
    keywords = st.text_area("Kata Kunci (pisahkan dengan koma):", placeholder="Contoh: machine learning, klasifikasi, NLP, sentiment analysis", height=80)
    description = st.text_area("Deskripsi Singkat Penelitian:", placeholder="Jelaskan tujuan, metodologi, dan kontribusi penelitian", height=120)

with col2:
    st.subheader("👀 Preview Konfigurasi")
    config_preview = {"Bidang Studi": field_of_study, "Format Sitasi": citation_format, "Tone": tone, "Jumlah Prompt": num_prompts}
    st.json(config_preview)

st.divider()

if st.button("🚀 Generate Prompts", type="primary", use_container_width=True):
    if not title or not keywords or not description:
        st.error("❌ Mohon isi semua field terlebih dahulu!")
    else:
        with st.spinner("⏳ Initializing Gemini AI..."):
            if not init_gemini():
                st.error("❌ Tidak bisa mengakses Gemini API!")
                st.error("Pastikan google-generativeai sudah terinstall")
            elif model is None:
                st.error("❌ Model tidak tersedia!")
            else:
                with st.spinner("⏳ Sedang membuat prompts..."):
                    system_message = f"""Anda adalah expert dalam membuat prompt berkualitas tinggi untuk penelitian akademik skripsi.
Buatkan {num_prompts} prompt yang berbeda untuk membantu penelitian skripsi dengan judul: {title}

Kata kunci: {keywords}
Bidang studi: {field_of_study}
Format sitasi: {citation_format}
Deskripsi: {description}

OUTPUT: JSON format ONLY:
{{"prompts": [{{"nomor": 1, "judul": "...", "isi": "...", "tipe": "...", "use_case": "..."}}]}}"""
                    
                    try:
                        response = model.generate_content(system_message)
                        response_text = response.text
                        
                        json_start = response_text.find('{')
                        json_end = response_text.rfind('}') + 1
                        
                        if json_start != -1 and json_end > json_start:
                            json_str = response_text[json_start:json_end]
                            prompts_data = json.loads(json_str)
                            
                            st.success("✅ Prompts berhasil dibuat!")
                            st.divider()
                            st.subheader("📌 Generated Prompts")
                            
                            for prompt in prompts_data.get("prompts", []):
                                with st.expander(f"**{prompt.get('judul', 'Prompt')}** — {prompt.get('tipe', 'general')}"):
                                    st.markdown(f"**📋 Isi Prompt:**")
                                    st.write(prompt.get('isi', 'N/A'))
                                    st.markdown(f"**💡 Kapan Digunakan:**")
                                    st.info(prompt.get('use_case', 'General use'))
                            
                            st.divider()
                            json_output = json.dumps(prompts_data, ensure_ascii=False, indent=2)
                            st.download_button("📄 Download JSON", json_output, f"prompts_{title[:20]}.json", "application/json")
                    except json.JSONDecodeError as e:
                        st.error(f"❌ JSON parse error: {e}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

st.divider()
st.markdown("<div style='text-align: center'><small>© 2024 Prompt Skripsi Generator | Powered by Google Gemini 1.5 Flash</small></div>", unsafe_allow_html=True)
