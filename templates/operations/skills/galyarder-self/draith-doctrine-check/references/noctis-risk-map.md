# Reference: draith-doctrine-check

# Noctis Risk Map

## When to Use

Gunakan skill ini ketika:

- Galih mau ambil keputusan/projek yang punya downside nyata (uang, reputasi, waktu, kesehatan, relasi).
- Ada perasaan "takut sesuatu pecah" tapi belum jelas apa.
- Galyarder ingin merancang sistem yang tahan banting, bukan hanya yang optimal di skenario ideal.

Jangan gunakan skill ini untuk:

- hal kecil yang impact‑nya rendah,
- momen ketika Galih lagi sangat rapuh (biarkan Keiya/Galyarder stabilkan dulu).

---

## Procedure

1. Definisikan konteks dan horizon waktu

   - Ringkas:
     - apa rencana/keputusannya,
     - scope (berapa besar),
     - horizon: 3 bulan / 1 tahun / 3 tahun.

   - Jika tidak disebutkan, asumsikan horizon 6–12 bulan.

2. Identifikasi dimensi risiko utama

   Setidaknya pertimbangkan:

   - Finansial (cashflow, hutang, runway, exposure)
   - Waktu & energi (burnout, opportunity cost)
   - Reputasi (kepercayaan keluarga, partner, pasar)
   - Sistem (single point of failure, ketergantungan pada 1 orang/tools)
   - Legal / ethical (pelanggaran aturan atau nilai)

2a. Mode asymmetric opportunity / eksperimen disposable

   Gunakan mode ini ketika Galih menilai peluang dari ROI/asymmetry, terutama eksperimen lokal/no-cost/disposable atau area abu-abu/merah/hijau.

   - Jangan mulai dari moralizing atau ceramah ToS.
   - Mulai dari kalkulasi: upside, downside nyata, hidden cost, blast radius, reversibility, dan tail risk.
   - Bedakan “downside 0” yang benar-benar terkunci dari downside yang belum dihitung: waktu, credential, device utama, identity linkage, akun, reputasi, legal exposure, kebiasaan shortcut, dan opportunity cost.
   - Verdict operasional:
     - upside besar + downside terkunci + blast radius lokal → gas/test agresif,
     - upside kecil + downside lebih besar → buang,
     - upside besar tapi nyentuh identitas utama/reputasi/hukum/orang lain → isolate dulu atau tolak eksekusi.

3. Bangun peta worst‑case per dimensi

   Untuk tiap dimensi:

   - jelaskan worst‑case realistis (bukan skenario fantasi ekstrim),
   - sebutkan:
     - pemicu utama,
     - seberapa mungkin (kasar: rendah/sedang/tinggi),
     - seberapa parah efeknya.

4. Cari titik rapuh (fragility)

   - Identifikasi:
     - di mana ada single point of failure,
     - di mana Galih sendiri adalah bottleneck ekstrem,
     - di mana sesuatu bergantung pada asumsi yang belum diuji.

   - Tandai 3–5 titik paling kritikal.

5. Rancang langkah resilience yang kecil tapi signifikan

   Untuk tiap titik kritikal:

   - usulkan 1–3 langkah:
     - limit exposure (caps, batas komitmen),
     - spread risk (diversifikasi kecil),
     - tambah observability (monitoring/log/test),
     - buat writing-plans B minimal (fallback sederhana).

   Pastikan langkah-langkah ini bisa mulai dikerjakan dalam 1–7 hari.

6. Format output

   - ## Context – ringkasan writing-plans + horizon.  
   - ## Risk Dimensions – daftar dimensi + ringkasan.  
   - ## Worst-Case Scenarios – bullet per dimensi.  
   - ## Fragile Points – 3–5 titik kritis.  
   - ## Resilience Moves – list langkah dengan prioritas.  
   - ## Residual Risk – apa yang masih harus diterima apa adanya.

---

## Pitfalls

- Over‑dramatizing → bikin Galih paralysed, bukan lebih siap.
- Moralizing / ceramah ToS ketika Galih meminta kalkulasi ROI untuk eksperimen lokal/no-cost/disposable. Jawab dengan downside nyata, hidden cost, blast radius, dan batas external-harm saja.
- Ngasih list risiko panjang tanpa prioritas.
- Menyarankan mitigasi yang terlalu besar/abstrak sehingga tidak ada yang jalan.
- Melupakan bahwa sebagian risiko memang harus diterima, bukan dihapus.

---

## Verification

Skill dianggap bekerja jika:

- Galih bisa menunjuk 3–5 risiko utama dan bilang “sekarang gue tahu bentuknya”.
- Ada minimal 3 langkah resilience konkret yang bisa dieksekusi minggu ini.
- Perasaan takut berubah dari kabur → lebih spesifik dan bisa ditindaklanjuti.

Jika setelah pemetaan, fear hanya membesar tanpa ada rencana, ulangi dengan scope lebih kecil dan fokus ke langkah pertama saja.