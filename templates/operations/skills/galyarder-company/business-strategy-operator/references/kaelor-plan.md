# Reference: business-strategy-operator

# Kaelor Plan

## When to Use

Gunakan skill ini ketika:

- Galih punya tujuan jelas (contoh: launch feature X, setup infra Y, bikin workflow Z) dan butuh rencana eksekusi konkret.
- Hasil dari Oryth Focus sudah ada, dan salah satu fokus perlu diturunin jadi langkah-langkah.
- Perlu dokumen rencana yang bisa dijalankan beberapa hari/minggu ke depan.

Jangan gunakan skill ini untuk:

- hal yang sangat kecil (cukup 1–2 langkah),
- hal yang masih murni eksplorasi tanpa intent eksekusi.

---

## Procedure

1. Definisikan Objective secara eksplisit

   - Tulis 1–3 kalimat:
     - apa yang mau selesai,
     - untuk siapa,
     - dalam horizon waktu berapa lama.

   Contoh:
   - "Dalam 3 minggu, punya versi pertama [X] yang bisa dipakai internal oleh Galih dan minimal 1 orang lain."

2. Gali constraint & context

   - Catat constraint utama:
     - waktu (jam/hari per minggu),
     - resource (uang, tools, infra),
     - dependency (orang lain, API, data),
     - standard (minimal quality yang diterima).

   - Jika tidak jelas, asumsikan constraint konservatif (waktu terbatas, resource ketat).

3. Pecah objektif jadi “workstreams”

   Biasanya 3–6 workstream, misalnya:

   - desain & spesifikasi,
   - implementasi backend / infra,
   - implementasi frontend / UX,
   - integrasi & ops (CI/CD, observability),
   - dokumentasi & onboarding,
   - brand/signal (landing, copy, announcement).

   Untuk tiap workstream:
   - jelaskan tujuan spesifik workstream,
   - sebutkan outcome konkret (apa yang dianggap “beres”).

4. Turunkan menjadi langkah-langkah

   Untuk setiap workstream:

   - buat 3–10 langkah bernomor,
   - urutkan secara logis (blocker duluan),
   - tandai jika ada langkah yang bisa paralel.

   Tulis langkah dengan gaya:
   - “Tentukan…”, “Buat…”, “Implementasikan…”, “Uji…”, “Refactor…”, “Tuliskan…”.

5. Identifikasi risiko & titik rapuh

   - Tulis 3–7 risiko utama:
     - dependency yang rentan,
     - bagian yang belum jelas,
     - hal yang kalau salah bisa mahal.

   - Tandai untuk setiap risiko:
     - mitigasi ringan,
     - atau keputusan sadar untuk menerima.

6. Definisikan milestone

   Buat 2–4 milestone:

   - M1 (awal): hal yang menandai rencana sudah benar-benar berjalan (contoh: spec final, repo siap).  
   - M2 (tengah): hal yang menunjukkan core system sudah hidup (contoh: alur utama bisa dieksekusi end-to-end).  
   - M3 (akhir): definisi jelas kapan objektif dianggap selesai (MVP, internal dogfooding, dsb).  
   - M4 (opsional): aftercare (hardening, dokumentasi, pengukuran).

   Untuk tiap milestone:
   - tulis kondisi “done” dalam 2–4 bullet.

7. Susun output terstruktur

   - ## Objective – pernyataan objektif.  
   - ## Constraints & Context – bullet constraint utama.  
   - ## Workstreams – list + deskripsi.  
   - ## Steps per Workstream – langkah bernomor.  
   - ## Risks & Fragility – risiko + mitigasi ringan.  
   - ## Milestones – M1–M3(+M4) dengan definisi done.

8. Optional: Next 3 Actions

   Di akhir, tambahkan:

   - ## Next 3 Actions (Today / This Week)  
     - 3 langkah paling kecil tapi paling leverage yang bisa mulai dikerjakan segera.

---

## Pitfalls

- Rencana terlalu high-level (cuma konsep, tidak actionable).
- Rencana terlalu granular (kayak to-do list detail tanpa struktur).
- Tidak menyebut constraint → rencana imajiner, bukan rencana untuk Galih nyata.
- Mengabaikan risiko, sehingga writing-plans terlihat indah tapi rapuh.

---

## Verification

Cek apakah:

- seseorang yang mengerti konteks bisa pakai writing-plans ini untuk mulai kerja tanpa tanya 1000 hal lagi,
- Galih bisa membaca writing-plans dan dengan jujur bilang:
  - “Gue tahu apa M1, M2, M3-nya,”
  - “Gue tahu 3 langkah pertama yang harus gue ambil.”

Jika tidak, perbaiki:
- Objective (terlalu kabur),
- Workstreams (tidak jelas),
- atau Next 3 Actions (tidak konkret).