
# prompts_config.py
# Contains a small set of prompt templates for Skripsi generator and helper function to create sample outputs.
# In production, templates will be more extensive (15-20 prompts) and Claude API will be used.

TEMPLATES = [
    {
        "id": "SKR-B1-V1",
        "title": "Bab 1 — Pendahuluan",
        "use_case": "Membuat outline dan contoh draf Bab 1 (Latar Belakang, Rumusan, Tujuan, Batasan, Manfaat)",
        "copy": (
            "Sebagai asisten akademik berbahasa Indonesia (tone tutor-friendly), buat outline Bab 1 untuk topik "
            "[working_title] pada bidang studi [bidang_studi]. Output dalam markdown dan harus memiliki bagian: "
            "Latar Belakang (3–4 paragraf alur masalah→gap→urgensi), Rumusan Masalah (3 pertanyaan terukur), Tujuan, "
            "Batasan, Manfaat, dan satu contoh draf paragraf 300–400 kata untuk Latar Belakang. Jangan menyertakan referensi nyata; "
            "jika referensi diperlukan, tampilkan query pencarian yang spesifik. Sertakan QC checklist 5 item di akhir."
        )
    },
    {
        "id": "SKR-B2-V1",
        "title": "Bab 2 — Tinjauan Pustaka",
        "use_case": "Menstrukturkan review literatur, gap identification, keyword search queries",
        "copy": (
            "Buat struktur Bab 2: Tinjauan Pustaka untuk topik [working_title] pada bidang [bidang_studi]. "
            "Sertakan saran sub-bab, model teoritik yang relevan, keyword search queries untuk Google Scholar, dan template kalimat pembuka per sub-bab. "
            "Jangan menyertakan kutipan nyata; sebutkan query pencarian spesifik untuk literature."
        )
    },
    {
        "id": "SKR-B3-V1",
        "title": "Bab 3 — Metodologi",
        "use_case": "Menjelaskan desain penelitian, populasi/sampel, instrumen, prosedur analisis",
        "copy": (
            "Buat Bab 3 Metodologi untuk topik [working_title]. Jelaskan: desain penelitian, populasi dan sampel, teknik sampling, "
            "instrumen (jika kuantitatif: kuesioner; jika kualitatif: pedoman wawancara), prosedur pengumpulan data, dan rencana analisis (statistik atau tematik). "
            "Tambahkan contoh format tabel instrumen dan checklist validitas/reliabilitas."
        )
    },
    {
        "id": "SKR-QC-V1",
        "title": "QC — Cek Judul & Rumusan Masalah",
        "use_case": "Quality check untuk memastikan judul dan rumusan masalah terukur dan relevan",
        "copy": (
            "Berikan checklist dan script penilaian untuk mengevaluasi apakah judul penelitian sudah fokus, rumusan masalah terukur, dan tujuan sesuai."
        )
    },
    {
        "id": "SKR-REV-V1",
        "title": "Revision Handler — Komentar Dosen Umum",
        "use_case": "Prompt untuk merevisi bab berdasarkan komentar dosen (10 tipe komentar umum)",
        "copy": (
            "Sediakan template respon dan langkah-langkah perbaikan untuk 10 komentar dosen umum (misal: metode kurang jelas, variabel tidak terukur, referensi lemah)."
        )
    }
]

def generate_example_output(prompt_id, input_example):
    # This function simulates an example output based on the template id and input.
    # In production, this would call the language model API (e.g., Claude) with the prompt.
    base = f"Contoh output untuk {prompt_id} - {input_example.get('working_title')}\n\n"
    if prompt_id.startswith('SKR-B1'):
        text = ("Latar Belakang:\n"
                "Perkembangan penggunaan platform e-learning di perguruan tinggi menunjukkan tren peningkatan, namun retensi belajar mahasiswa masih menjadi tantangan. "
                "Meskipun berbagai fitur gamifikasi diimplementasikan, bukti empiris mengenai dampaknya terhadap retensi pada konteks perguruan tinggi swasta masih terbatas. "
                "Penelitian ini bertujuan mengisi gap tersebut dengan mempelajari hubungan antara penerapan elemen gamifikasi dan indikator retensi belajar.\n\n"
                "Rumusan Masalah:\n1. Bagaimana pengaruh gamifikasi terhadap retensi belajar pada platform e-learning di perguruan tinggi swasta?\n"
                "2. Faktor apa saja yang memediasi hubungan tersebut?\n3. Bagaimana perbedaan dampak berdasarkan program studi?\n\n"
                "Tujuan:\nPenelitian ini bertujuan untuk...\n\n"
                "(Contoh draf latar belakang ~350 kata disingkat untuk demo.)\n")
        return base + text
    elif prompt_id.startswith('SKR-B2'):
        text = ("Bab 2 - Tinjauan Pustaka:\nSaran sub-bab: 1) Teori gamifikasi; 2) Retensi belajar; 3) Platform e-learning; 4) Studi terdahulu.\n"
                "Search queries: 'gamification retention e-learning 2016..2024'\n")
        return base + text
    elif prompt_id.startswith('SKR-B3'):
        text = ("Bab 3 - Metodologi:\nJenis penelitian: kuantitatif korelasional. Populasi: mahasiswa aktif. Sampel: stratified random sampling...\n"
                "Instrumen: kuesioner Likert 5-point (contoh item: ...). Rencana analisis: regresi linear berganda.\n")
        return base + text
    elif prompt_id.startswith('SKR-QC'):
        text = ("QC Checklist:\n- Judul fokus? (ya/tidak)\n- Rumusan masalah terukur?\n- Konsistensi antara tujuan dan metode?\n")
        return base + text
    else:
        return base + "Output contoh (template)."
