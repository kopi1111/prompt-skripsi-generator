
import streamlit as st
import json
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

# Streamlit page config
st.set_page_config(
    page_title="Prompt Skripsi Generator",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 Prompt Skripsi Generator")
st.markdown("Bantuan untuk membuat prompt yang efektif untuk penelitian skripsi Anda")

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    field_of_study = st.selectbox(
        "Pilih Bidang Studi:",
        ["Teknik Informatika", "Teknik Elektro", "Sistem Informasi", "Ilmu Komputer", "Lainnya"]
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

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Data Skripsi")
    
    title = st.text_input(
        "Judul Skripsi:",
        placeholder="Contoh: Implementasi Machine Learning untuk Klasifikasi Sentimen"
    )
    
    keywords = st.text_area(
        "Kata Kunci (pisahkan dengan koma):",
        placeholder="Contoh: machine learning, klasifikasi, NLP, dataset Indonesia",
        height=80
    )
    
    description = st.text_area(
        "Deskripsi Singkat Penelitian:",
        placeholder="Jelaskan secara singkat tujuan, metodologi, dan kontribusi penelitian Anda",
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
    
    st.info(
        "ℹ️ Konfigurasi di atas akan digunakan untuk generate prompts yang sesuai dengan kebutuhan Anda."
    )

# Generate button
if st.button("🚀 Generate Prompts", type="primary", use_container_width=True):
    
    # Validate input
    if not title or not keywords or not description:
        st.error("❌ Mohon isi semua field terlebih dahulu!")
    else:
        with st.spinner("⏳ Sedang membuat prompts..."):
            
            # Prepare the prompt for Claude
            system_prompt = f"""Anda adalah expert dalam membuat prompt berkualitas tinggi untuk penelitian akademik skripsi.
Buatkan {num_prompts} prompt yang berbeda dan beragam untuk membantu dalam penelitian skripsi.

Konteks:
- Bidang Studi: {field_of_study}
- Format Sitasi: {citation_format}
- Tone: {tone}
- Judul Skripsi: {title}
- Kata Kunci: {keywords}
- Deskripsi: {description}

Berikan prompt yang:
1. Spesifik dan actionable
2. Sesuai dengan bidang studi dan tone yang dipilih
3. Mempertimbangkan kata kunci yang relevan
4. Mendukung proses penelitian dan penulisan skripsi
5. Menggunakan format sitasi yang tepat

Format output: Berikan dalam format JSON dengan key "prompts" yang berisi list of objects. Setiap object memiliki:
- "judul": judul singkat prompt
- "isi": isi prompt lengkap
- "tipe": tipe prompt (literature_review, methodology, analysis, writing, dll)"""

            user_message = f"Buatkan {num_prompts} prompts berkualitas tinggi untuk skripsi saya dengan judul: '{title}'"
            
            try:
                # Call Claude API
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                
                # Extract response
                response_text = response.content[0].text
                
                # Try to parse JSON from response
                try:
                    # Find JSON in response
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start != -1 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        prompts_data = json.loads(json_str)
                    else:
                        prompts_data = {"prompts": [{"judul": "Response", "isi": response_text, "tipe": "general"}]}
                except json.JSONDecodeError:
                    prompts_data = {"prompts": [{"judul": "Response", "isi": response_text, "tipe": "general"}]}
                
                # Display results
                st.success("✅ Prompts berhasil dibuat!")
                
                st.subheader("📌 Generated Prompts")
                
                if "prompts" in prompts_data:
                    for idx, prompt in enumerate(prompts_data["prompts"], 1):
                        with st.expander(f"**{idx}. {prompt.get('judul', 'Prompt')}** - {prompt.get('tipe', 'general')}", expanded=False):
                            st.markdown(prompt.get('isi', 'N/A'))
                            
                            # Copy button
                            st.code(prompt.get('isi', 'N/A'), language="text")
                
                # Download option
                st.subheader("📥 Download Results")
                
                json_output = json.dumps(prompts_data, ensure_ascii=False, indent=2)
                
                st.download_button(
                    label="📄 Download sebagai JSON",
                    data=json_output,
                    file_name="prompts_skripsi.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Pastikan API key Anthropic sudah tersetting dengan benar.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>© 2024 Prompt Skripsi Generator | Dibuat dengan ❤️ menggunakan Streamlit & Claude AI</small>
</div>
""", unsafe_allow_html=True)
