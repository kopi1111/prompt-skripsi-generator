
import streamlit as st
import json
import google.generativeai as genai

# Configure Gemini API with embedded key
GEMINI_API_KEY = "AIzaSyDgAQ.Ab8RN6LJArtk9dS_wZF5KfcSMXmG9f-cCncIv6U0oizK50wWVQ"
genai.configure(api_key=GEMINI_API_KEY)

# Page config
st.set_page_config(
    page_title="Prompt Skripsi Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize model
@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# Title
st.title("📚 Prompt Skripsi Generator")
st.markdown("Bantuan membuat prompt berkualitas untuk penelitian skripsi Anda")

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    field_of_study = st.selectbox(
        "Pilih Bidang Studi:",
        ["Teknik Informatika", "Teknik Elektro", "Sistem Informasi", "Ilmu Komputer", "Bisnis", "Desain", "Lainnya"]
    )
    
    citation_format = st.selectbox(
        "Format Sitasi:",
        ["APA", "Harvard", "Chicago", "IEEE"]
    )
    
    tone = st.selectbox(
        "Tone:",
        ["Formal Akademik", "Semi-formal", "Teknis"]
    )
    
    num_prompts = st.slider(
        "Jumlah prompt yang mau dibuat:",
        min_value=1,
        max_value=10,
        value=5
    )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Data Skripsi")
    
    title = st.text_input(
        "Judul Skripsi:",
        placeholder="Contoh: Implementasi Machine Learning untuk Klasifikasi Sentimen"
    )
    
    keywords = st.text_area(
        "Kata Kunci (pisahkan dengan koma):",
        placeholder="Contoh: machine learning, klasifikasi, NLP, sentiment analysis",
        height=80
    )
    
    description = st.text_area(
        "Deskripsi Singkat Penelitian:",
        placeholder="Jelaskan tujuan, metodologi, dan kontribusi penelitian",
        height=120
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
    
    st.info("ℹ️ Konfigurasi di atas akan digunakan untuk generate prompts yang sesuai.")

# Generate button
if st.button("🚀 Generate Prompts", type="primary", use_container_width=True):
    
    # Validate input
    if not title or not keywords or not description:
        st.error("❌ Mohon isi semua field terlebih dahulu!")
    else:
        with st.spinner("⏳ Sedang membuat prompts dengan Gemini AI..."):
            try:
                # Prepare system prompt
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

                # Call Gemini API
                response = model.generate_content(system_message)
                response_text = response.text
                
                # Extract JSON from response
                try:
                    # Find JSON block
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    
                    if json_start != -1 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        prompts_data = json.loads(json_str)
                    else:
                        # Fallback if JSON not found
                        prompts_data = {
                            "prompts": [{
                                "nomor": 1,
                                "judul": "Response",
                                "isi": response_text,
                                "tipe": "general",
                                "use_case": "General guidance"
                            }]
                        }
                except json.JSONDecodeError as e:
                    st.error(f"⚠️ Error parsing JSON: {str(e)}")
                    st.code(response_text, language="json")
                    prompts_data = None
                
                if prompts_data:
                    # Display success
                    st.success("✅ Prompts berhasil dibuat!")
                    
                    st.subheader("📌 Generated Prompts")
                    
                    if "prompts" in prompts_data:
                        for prompt in prompts_data["prompts"]:
                            col_num, col_content = st.columns([0.1, 0.9])
                            
                            with col_num:
                                st.metric("No.", prompt.get('nomor', ''))
                            
                            with col_content:
                                with st.expander(
                                    f"**{prompt.get('judul', 'Prompt')}** — {prompt.get('tipe', 'general')}",
                                    expanded=False
                                ):
                                    st.markdown(f"**Isi Prompt:**")
                                    st.markdown(prompt.get('isi', 'N/A'))
                                    
                                    st.markdown(f"**Kapan Digunakan:**")
                                    st.info(prompt.get('use_case', 'General use'))
                                    
                                    st.code(prompt.get('isi', 'N/A'), language="text")
                    
                    # Download section
                    st.divider()
                    st.subheader("📥 Download & Export")
                    
                    col_json, col_txt = st.columns(2)
                    
                    with col_json:
                        json_output = json.dumps(prompts_data, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📄 Download JSON",
                            data=json_output,
                            file_name=f"prompts_{title[:20]}.json",
                            mime="application/json"
                        )
                    
                    with col_txt:
                        # Convert to text format
                        txt_output = "=== PROMPT SKRIPSI ===\n\n"
                        txt_output += f"Judul: {title}\n"
                        txt_output += f"Bidang: {field_of_study}\n"
                        txt_output += f"Format Sitasi: {citation_format}\n"
                        txt_output += f"Kata Kunci: {keywords}\n"
                        txt_output += "\n" + "="*50 + "\n\n"
                        
                        for prompt in prompts_data["prompts"]:
                            txt_output += f"PROMPT {prompt.get('nomor', '')}: {prompt.get('judul', '')}\n"
                            txt_output += f"Tipe: {prompt.get('tipe', '')}\n"
                            txt_output += f"Gunakan untuk: {prompt.get('use_case', '')}\n"
                            txt_output += "-" * 50 + "\n"
                            txt_output += f"{prompt.get('isi', '')}\n"
                            txt_output += "\n" + "="*50 + "\n\n"
                        
                        st.download_button(
                            label="📝 Download TXT",
                            data=txt_output,
                            file_name=f"prompts_{title[:20]}.txt",
                            mime="text/plain"
                        )
                    
                    # Statistics
                    st.divider()
                    st.subheader("📊 Statistik")
                    
                    stats_col1, stats_col2, stats_col3 = st.columns(3)
                    
                    with stats_col1:
                        st.metric("Total Prompts", len(prompts_data.get("prompts", [])))
                    
                    with stats_col2:
                        prompt_types = [p.get('tipe', 'general') for p in prompts_data.get("prompts", [])]
                        st.metric("Jenis Prompt", len(set(prompt_types)))
                    
                    with stats_col3:
                        total_chars = sum(len(p.get('isi', '')) for p in prompts_data.get("prompts", []))
                        st.metric("Total Karakter", f"{total_chars:,}")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.warning("Cek koneksi internet dan pastikan API key valid.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>© 2024 Prompt Skripsi Generator | Powered by Google Gemini 1.5 Flash</small>
</div>
""", unsafe_allow_html=True)
