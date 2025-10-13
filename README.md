# TUGAS_BESAR – Aplikasi Nilai Mahasiswa

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com/)  
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Last Commit](https://img.shields.io/github/last-commit/rasidi3112/TUGAS_BESAR.svg)](https://github.com/rasidi3112/TUGAS_BESAR/commits/main)

---

## 🌟 Deskripsi
**TUGAS_BESAR** adalah aplikasi web **manajemen nilai mahasiswa** berbasis **Python Flask**. Sistem ini membantu dosen atau admin untuk:

- Menambahkan, melihat, dan menghapus data mahasiswa.  
- Menghitung grade huruf (A–E) dari nilai angka secara otomatis.  
- Menyajikan statistik lengkap: rata-rata, nilai tertinggi/rendah, jumlah lulus/tidak lulus, distribusi grade.  
- Menampilkan top mahasiswa, statistik per semester, dan per mata kuliah.  
- Mengekspor laporan ke **PDF** dan **Excel** secara profesional.  
- Menyediakan **API JSON** untuk integrasi dengan aplikasi lain.

**Ini adalah bagian dari project kami sebagai Tugas Besar UAS Semester 2 matkul Algoritma dan Struktur Data.**

Aplikasi ini ideal untuk **keperluan akademik sederhana** tanpa perlu database kompleks.

---

## 🎬 Demo GIF
![Demo Aplikasi](assets/demo.gif)  
> GIF ini menunjukkan proses menambahkan mahasiswa, melihat daftar nilai, dan export laporan.

---

## 📸 Screenshot
### Halaman Utama
![Index Page](assets/screenshot_index.png)

### Laporan Nilai Mahasiswa
![Report Page](assets/screenshot_report.png)

---

## ⚙️ Teknologi
- **Python 3.x** – Bahasa utama.  
- **Flask** – Web framework ringan.  
- **Pandas** – Analisis dan manipulasi data.  
- **PDFKit** – Export PDF laporan.  
- **OpenPyXL** – Export Excel laporan.  
- **JSON** – Database sederhana.

---

## 📂 Fitur Utama
1. **Manajemen Data Mahasiswa** – CRUD sederhana untuk data mahasiswa.  
2. **Grade Otomatis** – Konversi nilai angka ke A/B/C/D/E.  
3. **Statistik Lengkap** – Rata-rata, tertinggi, terendah, jumlah mahasiswa, distribusi grade, per semester, per mata kuliah.  
4. **Export Laporan** – PDF & Excel siap pakai dengan ringkasan statistik.  
5. **API JSON** – Ambil dan hapus data mahasiswa melalui API.

---

## 🚀 Instalasi & Cara Menjalankan
1. **Clone repository**  
```bash
git clone https://github.com/rasidi3112/TUGAS_BESAR.git
cd TUGAS_BESAR
