
# Streamlit Prompt Skripsi Generator — MVP

Ini adalah prototype Streamlit app untuk menghasilkan prompt skripsi siap pakai (Bahasa Indonesia, tone tutor-friendly).
Tool ini masih prototype dan menggunakan simulated outputs. Untuk produksi, sambungkan ke API LLM (mis. Claude/Anthropic).

Files:
- main.py — Streamlit app UI (entrypoint)
- prompts_config.py — Template prompt dan helper generator (simulated)
- guardrails.py — Automated checks (PII, placeholder, absolutes, fabricated citations)
- export_handler.py — CSV & ZIP export helpers
- claude_integration.py — Stub untuk integrasi LLM (implement di produksi)
- requirements.txt — Dependencies minimal

Deploy cepat ke Streamlit Cloud:
1. Fork / upload repo ke GitHub.
2. Login ke https://share.streamlit.io dan hubungkan repo GitHub Anda.
3. Set main file path ke `main.py`, branch `main`.
4. Deploy — app akan live dalam 1-2 menit.

Security & Compliance:
- Jangan masukkan API key ke file yang di-push ke repo publik. Simpan key di Secrets/Env vars di platform hosting Anda.
- Periksa automated guardrails sebelum publish.
- Sertakan disclaimer akademik pada paket distribusi final.

Disclaimer:
Produk ini hanya template dan panduan. Pengguna wajib melakukan verifikasi sumber dan memastikan kepatuhan akademik.

