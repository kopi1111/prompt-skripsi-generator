
import streamlit as st
import pandas as pd
from prompts_config import TEMPLATES, generate_example_output
from guardrails import run_guardrails_checks
from export_handler import save_csv, create_zip_download_link

st.set_page_config(page_title='Prompt Skripsi Generator', layout='wide')

st.title("Prompt Skripsi Generator — MVP (Tutor‑Friendly, Bahasa Indonesia)")
st.write("Tool ini adalah prototype Streamlit untuk generate prompt skripsi. "
         "Untuk integrasi penuh dengan Claude API, isi klausa API di file claude_integration.py")

with st.sidebar:
    st.header("Pengaturan")
    bidang = st.selectbox("Pilih Bidang Studi:", ["Teknik Informatika", "Psikologi", "Ekonomi",
                                                  "Hukum", "Pendidikan", "Manajemen Bisnis", "Lainnya"])
    if bidang == "Lainnya":
        bidang = st.text_input("Sebutkan bidang studi lain:")
    sitasi = st.selectbox("Format Sitasi:", ["APA", "IEEE", "Harvard"])
    tone = st.selectbox("Tone:", ["Tutor-Friendly", "Formal Akademik", "Casual Mahasiswa"])
    jumlah = st.selectbox("Jumlah prompt yang mau dibuat:", [5, 10, 15, 20])
    st.markdown("---")
    st.info("Catatan: Ini adalah prototype. Untuk produksi silakan hubungkan ke Claude API.")

st.header("Konfirmasi Cepat (Preview)")
st.write("Bidang studi:", bidang)
st.write("Format sitasi:", sitasi)
st.write("Tone:", tone)

if st.button("Generate Prompts"):
    st.info("Generating... (simulated outputs for MVP).")
    results = []
    for i in range(jumlah):
        # rotate through templates
        tpl = TEMPLATES[i % len(TEMPLATES)]
        # prepare input example
        input_example = {
            "bidang_studi": bidang,
            "working_title": f"Contoh Judul {i+1} - {bidang}",
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "prefer_format": sitasi,
            "tone": tone
        }
        prompt_text = tpl["copy"]
        example_output = generate_example_output(tpl["id"], input_example)
        # run guardrails
        issues = run_guardrails_checks(prompt_text + "\n\n" + example_output)
        status = "✓ QC Pass" if len(issues)==0 else "⚠ Issues"
        results.append({
            "No": i+1,
            "PromptID": tpl["id"],
            "PromptName": tpl["title"],
            "UseCase": tpl["use_case"],
            "CopyPastePrompt": prompt_text,
            "InputExample": json.dumps(input_example, ensure_ascii=False),
            "OutputExample": example_output,
            "QCStatus": status,
            "QCIssues": "; ".join(issues)
        })
    df = pd.DataFrame(results)
    st.success("Selesai generate. Periksa preview di bawah.")
    st.dataframe(df[["No","PromptID","PromptName","QCStatus"]])

    with st.expander("Tampilkan semua prompts (detail)"):
        for idx,row in df.iterrows():
            st.subheader(f"{row['No']}. {row['PromptName']} ({row['PromptID']}) — {row['QCStatus']}")
            st.markdown("**Prompt (copy-paste):**")
            st.code(row["CopyPastePrompt"])
            st.markdown("**Contoh Input:**")
            st.code(row["InputExample"])
            st.markdown("**Contoh Output (sample):**")
            st.write(row["OutputExample"])
            if row["QCStatus"] != "✓ QC Pass":
                st.warning("Issue detected: " + row["QCIssues"])
            st.markdown("---")

    # Export options
    csv_path = save_csv(df, base_filename='generated_prompts')
    zip_path = create_zip_download_link(base_dir, zip_name='streamlit_prompt_generator_export.zip')
    st.markdown(f"[Download CSV file]({csv_path})")
    st.markdown(f"[Download full export ZIP]({zip_path})")
else:
    st.info("Tekan tombol 'Generate Prompts' untuk mulai generate (simulated)." )
