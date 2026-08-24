# Security Policy

## Reporting a Vulnerability

Kerentanan pada Smart FAQ (backend, bot, atau frontend) dapat dilaporkan lewat
jalur berikut:

1. **GitHub Security Advisory (disarankan)** — lihat tab *Security → Advisories →
   *Report a vulnerability*. Informasi ini hanya terlihat oleh maintainer.
2. **Issue GitHub** — boleh untuk masalah yang bukan kerahasiaan kredensial.
   **Jangan pernah** sertakan secret (token, API key, password, JWT) di issue atau form
   publik.

Mohon sertakan hal-hal berikut agar cepat ditindaklanjuti:
- Deskripsi singkat kerentanan dan dampaknya.
- Langkah repro (sebaiknya tanpa mengekspos data produksi/secret).
- Komponen yang terdampak (`smartfaq-backend`, `bot`, atau `smart-faq-fe`) + versi/commit.
- Bukti konsep (PoC) jika ada.

## Scope

Yang termasuk dalam cakupan:
- `smartfaq-backend/` — Flask API, autentikasi (JWT/cookie), prediksi ML, authz endpoint.
- `bot/` — Telegram & WhatsApp bot, komunikasi ke backend.
- `smart-faq-fe/` — Nuxt admin frontend, penanganan token, CSRF.

Di luar cakupan (tidak menerima laporan):
- Dependensi pihak ketiga yang sudah memiliki advisory publik tersendiri — laporkan ke
  upstream masing-masing.
- Bug pada versi yang sudah tidak didukung.

## Supported Versions

Saat ini belum ada rilis bertanda versi. Commit terbaru di branch `master` dianggap
sebagai versi yang didukung.

## Tindakan setelah menerima laporan

1. Maintainer akan membalas dalam waktu 72 jam untuk konfirmasi penerimaan.
2. Perbaikan dan rilis/push patch akan diupayakan secepat mungkin sesuai tingkat risiko.
3. Informasi dibuka ke publik setelah patch tersedia, kecuali ada alasan untuk menunda.

## Catatan kredensial penting

Repositori ini pernah menampung secret (Telegram bot token, API key, `JWT_SECRET`) di
riwayat git. Jika Anda menarik/menyalin riwayat lama, anggap secret tersebut
**sudah bocor** dan jangan menggunakannya. Putar semua kredensial produksi secara rutin.