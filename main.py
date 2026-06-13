
import streamlit as st
import json
import logging
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError as e:
    logger.error(f"Google Generative AI not available: {e}")
    GEMINI_AVAILABLE = False

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyDgAQ.Ab8RN6LJArtk9dS_wZF5KfcSMXmG9f-cCncIv6U0oizK50wWVQ"

if GEMINI_AVAILABLE:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        GEMINI_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Prompt Skripsi Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stExpander {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_gemini_model():
    """Initialize and cache Gemini model"""
    if not GEMINI_AVAILABLE:
        return None
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Failed to get model: {e}")
        return None

def validate_inputs(title: str, keywords: str, description: str) -> bool:
    """Validate user inputs"""
    if not title or not title.strip():
        st.error("❌ Judul Skripsi tidak boleh kosong!")
        return False
    if not keywords or not keywords.strip():
        st.error("❌ Kata Kunci tidak boleh kosong!")
        return False
    if not description or not description.strip():
        st.error("❌ Deskripsi Penelitian tidak boleh kosong!")
        return False
    return True

def generate_prompts(
    model,
    title: str,
    keywords: str,
    description: str,
    field_of_study: str,
    citation_format: str,
    tone: str,
    num_prompts: int
) -> Optional[Dict]:
    """Generate prompts using Gemini API"""
    
    system_message = f"""Anda adalah expert dalam membuat prompt berkualitas tinggi untuk penelitian akademik skripsi.
Buatkan {num_prompts} prompt yang berbeda dan beragam untuk membantu dalam penelitian skripsi.

KONTEKS PENELITIAN:
- Bidang Studi: {field_of_study}
- Format Sitasi: {citation_format}
- Tone Penulisan: {tone}
- Judul Skripsi: {title}
- Kata Kunci: {keywords}
- Deskripsi Singkat: {description}

KRITERIA PROMPT:
1. Spesifik dan actionable - prompt harus jelas dan dapat langsung dieksekusi
2. Sesuai bidang studi - relevan dengan konteks {field_of_study}
3. Mempertimbangkan kata kunci - gunakan kata kunci yang sudah disediakan
4. Mendukung proses penelitian - membantu literature review, methodology, analysis, atau writing
5. Format sitasi {citation_format} - jika relevan dengan tipe prompt

OUTPUT FORMAT:
Berikan HANYA dalam format JSON valid seperti ini (tanpa markdown, tanpa ```json):
{{
  "prompts": [
    {{
      "nomor": 1,
      "judul": "Judul Prompt Singkat",
      "isi": "Isi lengkap prompt yang siap pakai...",
      "tipe": "literature_review|methodology|analysis|writing|editing|research_design",
      "use_case": "Kapan dan bagaimana menggunakan prompt ini"
    }}
  ]
}}

Pastikan output adalah JSON valid yang bisa di-parse langsung."""

    try:
        response = model.generate_content(system_message)
        response_text = response.text
        
        # Extract JSON
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            prompts_data = json.loads(json_str)
            return prompts_data
        else:
            logger.warning("JSON not found in response")
            return {
                "prompts": [{
                    "nomor": 1,
                    "judul": "Response",
                    "isi": response_text,
                    "tipe": "general",
                    "use_case": "General guidance"
                }]
            }
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        st.error(f"⚠️ Error parsing response: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Generation error: {e}")
        st.error(f"❌ Error generating prompts: {str(e)}")
        return None

def export_to_text(title: str, keywords: str, field_of_study: str, 
                   citation_format: str, prompts_data: Dict) -> str:
    """Convert prompts data to text format"""
    txt_output = "=== PROMPT SKRIPSI ===\n\n"
    txt_output += f"Judul: {title}\n"
    txt_output += f"Bidang: {field_of_study}\n"
    txt_output += f"Format Sitasi: {citation_format}\n"
    txt_output += f"Kata Kunci: {keywords}\n"
    txt_output += "\n" + "="*50 + "\n\n"
    
    for prompt in prompts_data.get("prompts", []):
        txt_output += f"PROMPT {prompt.get('nomor', '')}: {prompt.get('judul', '')}\n"
        txt_output += f"Tipe: {prompt.get('tipe', '')}\n"
        txt_output += f"Gunakan untuk: {prompt.get('use_case', '')}\n"
        txt_output += "-" * 50 + "\n"
        txt_output += f"{prompt.get('isi', '')}\n"
        txt_output += "\n" + "="*50 + "\n\n"
    
    return txt_output

# ============================================================================
# MAIN UI
# ============================================================================

# Title
st.title("📚 Prompt Skripsi Generator")
st.markdown("**Bantuan membuat prompt berkualitas untuk penelitian skripsi Anda**")
st.markdown("---")

# Check API availability
if not GEMINI_AVAILABLE:
    st.error("❌ **ERROR**: Google Generative AI module tidak tersedia!")
    st.info("Pastikan requirements.txt sudah diupdate dengan `google-generativeai`")
    st.stop()

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    field_of_study = st.selectbox(
        "Pilih Bidang Studi:",
        [
            "Teknik Informatika",
            "Teknik Elektro",
            "Sistem Informasi",
            "Ilmu Komputer",
            "Bisnis",
            "Desain",
            "Manajemen",
            "Lainnya"
        ]
    )
    
    citation_format = st.selectbox(
        "Format Sitasi:",
        ["APA", "Harvard", "Chicago", "IEEE"]
    )
    
    tone = st.selectbox(
        "Tone Penulisan:",
        ["Formal Akademik", "Semi-formal", "Teknis"]
    )
    
    num_prompts = st.slider(
        "Jumlah prompt yang mau dibuat:",
        min_value=1,
        max_value=10,
        value=5
    )
    
    st.divider()
    st.markdown("### 📊 Info")
    st.info("Generator menggunakan Google Gemini 1.5 Flash untuk hasil optimal dan cepat.")

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input Data Skripsi")
    
    title = st.text_input(
        "Judul Skripsi:",
        placeholder="Contoh: Implementasi Machine Learning untuk Klasifikasi Sentimen",
        help="Judul penelitian Anda"
    )
    
    keywords = st.text_area(
        "Kata Kunci (pisahkan dengan koma):",
        placeholder="Contoh: machine learning, klasifikasi, NLP, sentiment analysis",
        height=80,
        help="Kata kunci utama penelitian Anda"
    )
    
    description = st.text_area(
        "Deskripsi Singkat Penelitian:",
        placeholder="Jelaskan tujuan, metodologi, dan kontribusi penelitian",
        height=120,
        help="Deskripsi singkat namun detail tentang penelitian Anda"
    )

with col2:
    st.subheader("👀 Preview Konfigurasi")
    
    config_preview = {
        "Bidang Studi": field_of_study,
        "Format Sitasi": citation_format,
        "Tone": tone,
        "Jumlah Prompt": num_prompts
    }
    
    st.json(config_preview)
    
    st.info("ℹ️ Konfigurasi di atas akan digunakan untuk generate prompts yang sesuai dengan kebutuhan Anda.")

st.divider()

# Generate button
if st.button("🚀 Generate Prompts", type="primary", use_container_width=True):
    
    # Validate input
    if not validate_inputs(title, keywords, description):
        st.stop()
    
    model = get_gemini_model()
    if not model:
        st.error("❌ Tidak bisa mengakses Gemini API. Cek konfigurasi!")
        st.stop()
    
    with st.spinner("⏳ Sedang membuat prompts dengan Gemini AI..."):
        prompts_data = generate_prompts(
            model=model,
            title=title,
            keywords=keywords,
            description=description,
            field_of_study=field_of_study,
            citation_format=citation_format,
            tone=tone,
            num_prompts=num_prompts
        )
        
        if prompts_data:
            # Display success
            st.success("✅ Prompts berhasil dibuat!")
            st.divider()
            
            st.subheader("📌 Generated Prompts")
            
            if "prompts" in prompts_data:
                for prompt in prompts_data["prompts"]:
                    col_num, col_content = st.columns([0.08, 0.92])
                    
                    with col_num:
                        st.metric("No.", prompt.get('nomor', ''))
                    
                    with col_content:
                        with st.expander(
                            f"**{prompt.get('judul', 'Prompt')}** — `{prompt.get('tipe', 'general')}`",
                            expanded=False
                        ):
                            st.markdown(f"**📋 Isi Prompt:**")
                            st.write(prompt.get('isi', 'N/A'))
                            
                            st.markdown(f"**💡 Kapan Digunakan:**")
                            st.info(prompt.get('use_case', 'General use'))
                            
                            st.code(prompt.get('isi', 'N/A'), language="text")
            
            # Export section
            st.divider()
            st.subheader("📥 Download & Export")
            
            col_json, col_txt = st.columns(2)
            
            with col_json:
                json_output = json.dumps(prompts_data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_output,
                    file_name=f"prompts_{title[:20].replace(' ', '_')}.json",
                    mime="application/json"
                )
            
            with col_txt:
                txt_output = export_to_text(title, keywords, field_of_study, citation_format, prompts_data)
                st.download_button(
                    label="📝 Download TXT",
                    data=txt_output,
                    file_name=f"prompts_{title[:20].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            
            # Statistics
            st.divider()
            st.subheader("📊 Statistik")
            
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            
            with stats_col1:
                st.metric("Total Prompts", len(prompts_data.get("prompts", [])))
            
            with stats_col2:
                prompt_types = [p.get('tipe', 'general') for p in prompts_data.get("prompts", [])]
                st.metric("Jenis Prompt", len(set(prompt_types)))
            
            with stats_col3:
                total_chars = sum(len(p.get('isi', '')) for p in prompts_data.get("prompts", []))
                st.metric("Total Karakter", f"{total_chars:,}")
            
            with stats_col4:
                avg_chars = total_chars // len(prompts_data.get("prompts", [])) if prompts_data.get("prompts") else 0
                st.metric("Rata-rata Karakter", f"{avg_chars:,}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center'>
    <small>© 2024 Prompt Skripsi Generator | Powered by Google Gemini 1.5 Flash | v1.1</small>
</div>
""", unsafe_allow_html=True)
