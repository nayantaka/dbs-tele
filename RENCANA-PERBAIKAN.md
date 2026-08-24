# Rencana Perbaikan Codebase Smart FAQ

Dokumen ini merangkum hasil audit keamanan & kualitas kode terhadap tiga komponen
(`smartfaq-backend`, `bot`, `smart-faq-fe`) dan langkah perbaikan yang disarankan
secara bertahap.

## Status Pengerjaan

- **P0 — Keamanan: DITERAPKAN.** Secret diputar & di-untrack; `.gitignore` diperbarui;
  `pickle` → JSON; otorisasi `/user`, `/dataset/category`, `/response/category` diperbaiki.
- **P1 — Keandalan: DITERAPKAN.** Handler error unik; fix deref `None`; startup bot concurrency; guard pesan non-teks.
- **P2 — Pemadatan: DITERAPKAN.** Rate limiting; batas pagination; serialisasi `/train`;
  validasi input dataset/response; CORS whitelist; `DEBUG=False`.
- **P3 — Modernisasi: SEBAGIAN.** Bot: axios → 1.19.0 (terverifikasi). Frontend: bump lodash/jquery/vuex-persistedstate di manifest.
  **Belum diverifikasi (butuh runtime):** upgrade Flask/Werkzeug/TensorFlow, nuxt/moment/node-sass,
  penggantian `baileys@3` (abandoned), migrasi token → HttpOnly cookie, instal & build frontend
  (Node 24 tidak kompatibel dengan node-sass 5 / nuxt 2.14 — gunakan Node ≤14/16 untuk install/build).
- **P4 — Kualitas: DITERAPKAN.** Error handling frontend (store & halaman menampilkan error); kode mati
  bot dibersihkan (`batterylevel` typo, `===`); logging terstruktur di `response.js`; aksesibilitas
  (aria-label tombol ikon, `id` password duplikat dihapus).
- **P3.4 — migrasi token → HttpOnly cookie: DITERAPKAN (belum verifikasi runtime).** Backend set cookie
  (`set_access_cookies`/`set_refresh_cookies`, CSRF, `JWT_TOKEN_LOCATION`, `/auth/logout`, CORS credentials);
  frontend `withCredentials` + header CSRF, hapus persistensi `secure-ls` (token hanya di cookie),
  middleware berbasis `info`. **⚠️ Perlu uji runtime**: login/refresh/logout/CSRF lintas origin.
- **Penguatan tambahan (DITERAPKAN, terverifikasi bot):** seed admin tidak lagi hardcode `"secret"`
  (baca `SEED_ADMIN_*` dari env, fallback acak); `/predict` melarang kalimat kosong & >500 karakter;
  migrasi `@adiwajshing/baileys@3` (abandoned) → `@whiskeysockets/baileys@7` — **`npm audit` bot: 0
  vulnerabilities** (dari 21). **⚠️ `whatsapp.js` perlu uji koneksi WhatsApp** (API v7 `makeWASocket`).
- **Frontend toolchain (DITERAPKAN, build iya):** nuxt 2.14→2.18, `node-sass`→`sass` (dart-sass),
  lodash/jquery/vuex-persistedstate v3 (kompatibel Vue 2), dotenv v16, `@nuxtjs/eslint-module` dihapus.
  `npm run build` lulus. **`secure-ls`/`crypto-js` dihapus** (info non-sensitif kini di localStorage polos;
  token sudah di cookie) → kritikal turun 3→1. Sisa 62 vuln berasal dari **Nuxt 2 / Vue 2 / webpack4 /
  bootstrap (semua EOL)**; bersih total butuh migrasi Nuxt 3. **Catatan env:** mesin ini
  `npm config set omit dev`, jadi devDeps (sass/sass-loader) tidak terpasang kecuali pakai
  `npm install --include=dev`.

---

## Blocker: upgrade dependensi backend

Upgrade backend (Flask 2.x/Werkzeug 2.x/JWT-extended 4.x, TensorFlow) **tidak dapat diverifikasi di
lingkungan ini**:
- Virtualenv yang ter-commit rusak (path absolut Python 3.7 patah karena ikut di-commit) — perlu
  dibuat ulang.
- Python sistem = 3.12, sedangkan **TensorFlow 2.9.3 hanya mendukung 3.7–3.10**; upgrade TF penuh
  adalah migrasi besar (Keras 2 → `tf.keras`, numpy, dsb).
- Tidak ada MySQL untuk boot-test.

**Langkah yang disarankan (perlu mesin dengan Python 3.10 + MySQL):**
1. Buat venv baru (Python 3.10) — jangan commit.
2. Upgrade web stack: `Flask==2.2.5`, `Werkzeug==2.2.3`, `Flask-JWT-Extended==4.6.0` (kompatibel
   Python 3.7/3.10), `Flask-Migrate`, `Alembic`, `Flask-SQLAlchemy`, `Flask-Cors`. Kode yang dipakai
   (`set_access_cookies`, cookie migration) kompatibel dengan JWT-extended 4.x.
3. Pertahankan `tensorflow==2.9.3` (atau naikkan bersama Keras) sampai siap migrasi ML terpisah.
4. Jalankan `pip install -r requirements.txt`, uji `flask db upgrade` + boot dengan MySQL.

---

## Ringkasan Prioritas

| Prioritas | Area | Ringkas Masalah |
|-----------|------|-----------------|
| P0 | Keamanan | Rahasia live ter-commit, JWT dapat dipalsukan, pickle unsafe |
| P1 | Keandalan | Bug `errors.py`, bug `None` di PredictController, startup bot |
| P2 | Pemadatan | Rate limiting, batas pagination, validasi input, CORS |
| P3 | Modernisasi | Upgrade dependensi EOL/rentan, token di HttpOnly cookie |
| P4 | Kualitas | Error handling, aksesibilitas, kode mati, logging |

> **Catatan penting:** Poin P0 bernilai *memperbaiki dulu* karena menyangkut integritas
> sistem. Beberapa tindakan (putar secret) tidak bisa dibatalkan dan harus dilakukan
> dengan hati-hati.

---

## P0 — Keamanan (lakukan pertama)

### 0.1 Putar/revoke semua secret yang bocor
- **Status target:** secret lama tidak berlaku lagi.
- **Lokasi:** `bot/.env`, `smartfaq-backend/.env`, `smart-faq-fe/.env.example`, `smartfaq-backend/seeds/user.py`.
- **Langkah:**
  1. Revoke Telegram bot token via BotFather → buat token baru.
  2. Regenerate API key baru di backend (hapus key lama dari tabel `apikey`).
  3. Tidak lagi memakai URL ngrok yang di-hardcode.
  4. Ubah `JWT_SECRET` & `SECRET_KEY` ke nilai acak panjang.
  5. Uji ulang flow login, prediksi, dan Telegram setelah rotasi.
- **Kriteria selesai:** token lama tidak lagi diterima; proses login/predict/webhook berjalan dengan kredensial baru.

### 0.2 Hentikan commit rahasia
- **Status target:** tidak ada secret yang masuk ke git.
- **Lokasi:** `.gitignore` (root/backend/bot) + `git rm --cached`.
- **Langkah:**
  1. Tambahkan `.env` dan `*.pkl` (jika tidak wajib di-repo) ke `.gitignore` di `smartfaq-backend` dan `bot`.
  2. Jalankan `git rm --cached <file>` untuk `.env` yang sudah ter-track.
  3. Ganti nilai `.env.example` dengan placeholder (hindari URL ngrok live).
  4. Pertimbangkan `git-filter-repo` untuk membersihkan riwayat commit bila repo bersifat publik.
- **Kriteria selesai:** `git status` bersih tanpa `.env`; tidak ada secret di riwayat yang aktif dipakai.

### 0.3 Ganti penggunaan `pickle` yang tidak aman
- **Status target:** tidak ada deserialisasi `pickle` dari data yang bisa dipengaruhi user.
- **Lokasi:** `smartfaq-backend/app/service/IntentClassifier/Predict.py:9`, `Preprocessing.py:73`.
- **Langkah:**
  1. Simpan tokenizer/label dalam format aman (JSON) alih-alih `pickle`.
  2. Jika tetap perlu `pickle`, simpan di path terproteksi dan validasi ulang isi saat load.
  3. Tetapkan ulang pipeline training untuk menghasilkan file format baru.
- **Kriteria selesai:** tidak ada `pickle.load` pada data turunan DB; pipeline prediksi tetap menghasilkan jawaban yang sama.

### 0.4 Perbaiki otorisasi endpoint
- **Status target:** semua endpoint sensitif mengharuskan autentikasi.
- **Lokasi:** `app/controller/UserController.py` (`store`), `app/routes.py`.
- **Langkah:**
  1. Beri `@jwt_required` pada `UserController.store()`.
  2. Proteksi `GET /dataset/category` dan `GET /response/category` dengan JWT atau API key yang sah.
  3. Hapus/hapuskan penggunaan `/user` POST publik jika pendaftaran publik hanya lewat `/auth/register`.
- **Kriteria selesai:** kunjungan tanpa token ke endpoint tersebut ditolak (401/403).

---

## P1 — Keandalan (bug yang menyebabkan salah status/error)

### 1.1 Perbaiki handler error yang saling menimpa
- **Status target:** setiap kode status dikembalikan dengan benar.
- **Lokasi:** `smartfaq-backend/app/errors.py`.
- **Langkah:**
  1. Beri nama fungsi unik tiap `@app.errorhandler` (mis. `handle_not_found`, `handle_duplicate`, `handle_password_not_match`, `handle_apikey`, `handle_validation`).
  2. Ubah handler top-level `Exception` agar mengembalikan objek `(response, status)` yang valid, bukan dict polos.
  3. Pastikan urutan registrasi tidak saling menimpa.
- **Kriteria selesai:** request yang memicu `NotFoundException`, `DuplicateException`, `PasswordNotMatch` mengembalikan 404/409/401 (bukan 500).

### 1.2 Perbaiki dereferensi `None` di prediksi
- **Status target:** `/predict` tidak crash saat model mengembalikan `None`.
- **Lokasi:** `smartfaq-backend/app/controller/PredictController.py:28-30`.
- **Langkah:**
  1. Jika `result is None`, kembalikan respons intent `unknown` atau pesan fallback tanpa mengakses `result['intent']`.
  2. Tambahkan log untuk kasus model gagal menghasilkan prediksi.
- **Kriteria selesai:** input apa pun tidak menghasilkan `TypeError`; fallback dikembalikan.

### 1.3 Perbaiki startup bot agar kedua layanan berjalan
- **Status target:** Telegram dan WhatsApp berjalan bersamaan tanpa saling memblokir.
- **Lokasi:** `bot/index.js`.
- **Langkah:**
  1. Ganti `await` berurutan (yang ke-blok oleh koneksi WhatsApp yang tak pernah return) dengan peluncuran independen / `Promise.allSettled`.
  2. Tambah guard `unhandledRejection` dan `uncaughtException` di level proses.
- **Kriteria selesai:** kedua bot terdaftar dan menerima pesan saat proses berjalan.

### 1.4 Guard pesan non-teks di bot
- **Status target:** bot tidak crash saat menerima foto/voice/sticker.
- **Lokasi:** `bot/telegram.js:8-11`, `bot/whatsapp.js:63-71`.
- **Langkah:**
  1. Cek `typeof ctx.message.text === 'string'` sebelum memanggil `getResponse`.
  2. Pada WhatsApp, hanya proses saat `text` terdefinisi (bukan hanya `conversation`/`extendedTextMessage`).
- **Kriteria selesai:** berkas non-teks di-abaikan tanpa error ke user.

---

## P2 — Pemadatan & Perlindungan Resource

### 2.1 Rate limiting
- **Status target:** `/predict` dan `/auth/login` kebal brute-force/DoS.
- **Lokasi:** `smartfaq-backend` (dependency baru, mis. Flask-Limiter).
- **Langkah:**
  1. Terapkan rate limit per IP pada `POST /auth/login`.
  2. Terapkan rate limit per API key pada `GET /predict`.
- **Kriteria selesai:** permintaan melebihi batas ditolak (429) dengan pesan ramah.

### 2.2 Batasi pagination
- **Status target:** tidak ada memory exhaustion lewat `per_page`.
- **Lokasi:** semua controller yang membaca `per_page` (`DatasetController.py:36`, `ResponseController.py:36`, `UserController.py:35`, `ApikeyController.py:29`).
- **Langkah:**
  1. Validasi `per_page` (mis. cap maksimal 100) dan `page >= 1`.
  2. Tangani `ValueError` dari konversi `int(...)` dengan respons 400.
- **Kriteria selesai:** permintaan `per_page` raksasa / non-numerik ditolak dengan 400.

### 2.3 Serialisasi training
- **Status target:** `/train` tidak bisa dipakai untuk DoS.
- **Lokasi:** `smartfaq-backend/app/service/Daemon/TrainModel.py`, `app/controller/TrainController.py`.
- **Langkah:**
  1. Gunakan lock/flag sehingga hanya satu proses training aktif.
  2. Tolak permintaan `/train` ketika training sudah berjalan (409/423).
- **Kriteria selesai:** hanya satu training berjalan; request berlebih ditolak.

### 2.4 Validasi input pada CRUD
- **Status target:** tidak ada `KeyError` → 500 dan data tidak valid tidak tersimpan.
- **Lokasi:** `DatasetController`, `ResponseController`, `UserController.update`.
- **Langkah:**
  1. Terapkan skema `flask-expects-json`/`marshmallow` untuk dataset & response.
  2. Batasi panjang string sesuai kolom model; validasi tipe.
- **Kriteria selesai:** input tidak sah dikembalikan 400 dengan pesan jelas.

### 2.5 Sempitkan CORS
- **Status target:** hanya origin frontend yang diizinkan.
- **Lokasi:** `smartfaq-backend/app/__init__.py:16`.
- **Langkah:**
  1. Ganti `CORS(app)` dengan daftar `origins` whitelist dari konfigurasi.
- **Kriteria selesai:** permintaan dari origin tak dikenal tidak punya akses cross-origin.

### 2.6 Matikan `DEBUG` di produksi
- **Lokasi:** `smartfaq-backend/.env`.
- **Langkah:** set `DEBUG=False` (atau ambil dari env). Jangan pernah aktif saat produksi.

---

## P3 — Modernisasi Dependensi & Token

### 3.1 Upgrade dependensi backend
- **Lokasi:** `smartfaq-backend/requirements.txt`.
- **Langkah:**
  1. Flask → versi stabil terbaru (≥2.x), Werkzeug ikut naik.
  2. Flask-JWT-Extended → versi terbaru.
  3. Upgrade PyYAML & paket NLP bila memungkinkan; catat kebutuhan khusus TensorFlow 2.x.
- **Kriteria selesai:** tidak ada CVE kritis yang diketahui pada dependensi inti; aplikasi tetap berjalan.

### 3.2 Upgrade dependensi bot
- **Lokasi:** `bot/package.json`.
- **Langkah:**
  1. axios → ≥0.21.2 atau 1.x.
  2. telegraf → versi 4.x terbaru.
  3. Evaluasi pengganti `@adiwajshing/baileys@3.x` (empty/unmaintained) dengan versi yang masih didukung.
  4. Tetapkan versi (pin exact) dan `engines` Node.
- **Kriteria selesai:** `npm audit` tanpa temuan kritis yang bisa dihindari.

### 3.3 Upgrade dependensi frontend
- **Lokasi:** `smart-faq-fe/package.json`.
- **Langkah:**
  1. lodash → ≥4.17.21; jquery → ≥3.5.2 (atau hapus bila hanya untuk cek lebar layar).
  2. `node-sass` → `sass` (dart-sass).
  3. muat upgrade Nuxt 2.x patch; pertimbangkan Nuxt 3 bila budget memungkinkan.
  4. Ganti `moment` → `dayjs`; pin `vuex-persistedstate` ke rilis stabil.
- **Kriteria selesai:** build lulus; `npm audit` bersih dari CVE yang relevan.

### 3.4 Pindahkan token ke HttpOnly cookie
- **Status target:** JWT/refresh tidak bisa dibaca script client (XSS tidak dapat mencuri kredensial).
- **Lokasi (backend):** `config.py`, `app/__init__.py`, `app/controller/AuthController.py`, `.env`.
- **Lokasi (frontend):** `nuxt.config.js`, `plugins/axios.js`, `plugins/vuex-persistedstate.js`, `store/authorization.js`, `middleware/authorization.js`, `middleware/is-auth.js`, `api/authorization.js`, `pages/refresh.vue`.
- **Langkah backend:**
  1. `config.py`: tambah opsi JWT cookie — `JWT_TOKEN_LOCATION=['cookies']`, `JWT_ACCESS_COOKIE_NAME='access_token_cookie'`, `JWT_REFRESH_COOKIE_NAME='refresh_token_cookie'`, `JWT_COOKIE_SECURE=True` (saat HTTPS), `JWT_COOKIE_CSRF_PROTECT=True`, `JWT_ACCESS_COOKIE_PATH`, `JWT_REFRESH_COOKIE_PATH`.
  2. `AuthController.login()`: alih-alih mengembalikan token di body, panggil `set_access_cookies(resp, access_token)` dan `set_refresh_cookies(resp, refresh_token)`, lalu `jsonify_unset_jwt_cookies(resp)` pada logout/error. Cookie otomatis berflag `HttpOnly`.
  3. `AuthController.refresh()`: gunakan `set_refresh_cookies`/`set_access_cookies` (token diambil dari cookie oleh `@jwt_refresh_token_required`).
  4. Tambah endpoint/logout yang memanggil `unset_jwt_cookies`.
  5. CORS: pastikan `supports_credentials=True` dan origin frontend terdaftar di `CORS_ORIGINS`.
- **Langkah frontend:**
  1. `nuxt.config.js` / `plugins/axios.js`: `axios.withCredentials = true` agar cookie terkirim cross-origin.
  2. `plugins/vuex-persistedstate.js`: hapus `authorization.*` dari daftar `paths` (jangan persist token di localStorage/secure-ls).
  3. `store/authorization.js`: `setToken`/`setRefreshToken` tidak lagi menyimpan nilai token; cukup flag boolean `is_authenticated`.
  4. `api/authorization.js`: `login()` tidak perlu membaca `access_token`/`refresh_token` dari body (cookie otomatis). Kirim header `X-CSRF-TOKEN` dari token CSRF jika `JWT_COOKIE_CSRF_PROTECT=True`.
  5. `middleware/authorization.js` & `is-auth.js`: ganti pengecekan `store.token`/`store.refresh_token` dengan `is_authenticated` (atau panggil endpoint `/auth/me` untuk validasi sesi).
  6. `pages/refresh.vue` & `plugins/axios.js`: pada 401 karena token kadaluarsa, panggil `/auth/refresh` otomatis (bukan rely pada refresh_token di localStorage).
- **Kriteria selesai:** tidak ada token di localStorage; XSS tidak bisa mengekstrak kredensial; logout menghapus cookie; refresh otomatis berjalan.
- **⚠️ Perlu runtime testing** (backend+DB+dua origin): pastikan login, refresh, logout, dan CSRF bekerja di lingkungan yang sebenarnya. Inisiasi `JWT_TOKEN_LOCATION` di banyak tempat bisa mengubah perilaku `@jwt_required` — uji semua endpoint terlindungi.

---

## P4 — Kualitas Kode

### 4.1 Perbaiki penanganan error frontend
- **Lokasi:** `store/dataset.js`, `store/response.js`, `store/apikey.js`, halaman terkait.
- **Langkah:**
  1. Hapus pola `catch (err) { return Promise.resolve() }` → propagate atau tampilkan notifikasi.
  2. Ganti `catch (err) {}` kosong di halaman dengan feedback ke user.
- **Kriteria selesai:** kegagalan API terlihat oleh user dan tidak dianggap sukses.

### 4.2 Bersihkan kode mati di bot
- **Lokasi:** `bot/whatsapp.js:33,68`.
- **Langkah:** deklarasikan `batteryLevel` dengan benar; hapus `quotedText` yang tak terpakai; hindari `==` (gunakan `===`).

### 4.3 Tambah logging terstruktur
- **Lokasi:** `bot/response.js`, `smartfaq-backend`.
- **Langkah:** log kegagalan dengan konteks (tanpa memuat pesan user sensitif di operator-facing log secara berlebihan), bukan menelan error jadi string statis.

### 4.4 Aksesibilitas frontend
- **Lokasi:** tabel dataset/response/api-key, `components/setting/password.vue`, `pages/register.vue`.
- **Langkah:** tambah `aria-label` pada tombol ikon; perbaiki `id="password"` duplikat.

---

## Pembersihan riwayat git (secret lama)

**Mengapa:** `bot/.env` dan `smartfaq-backend/.env` (berisi Telegram bot token, API key,
`JWT_SECRET`, dsb.) pernah ter-commit. `git rm --cached` hanya berhenti melacak ke depan;
**secret masih ada di riwayat commit** dan akan bocor siapa pun yang menarik riwayat lama.

**⚠️ Operasi ini irreversible:** menulis ulang semua hash commit dan membutuhkan force-push.
Semua orang yang sudah clone harus re-clone. Jangan jalankan tanpa koordinasi dengan tim.

**Langkah (jalankan di mesin Anda, bukan otomatis oleh asisten):**
1. Cadangkan remote/riwayat dulu (opsional): `git push origin master:backup-before-clean`.
2. Instal filter (sekali): `pip install git-filter-repo`.
3. Hapus path secret dari seluruh riwayat:
   ```bash
   git filter-repo --invert-paths \
     --path bot/.env \
     --path smartfaq-backend/.env \
     --path smartfaq-backend/seeds/user.py
   ```
   (Tambahkan path lain bila ada file rahasia lain yang pernah ter-commit.)
4. Tandai ulang `origin` (`git filter-repo` menghapus remote):
   `git remote add origin https://github.com/nayantaka/dbs-tele.git`
5. Force-push semua branch & tag:
   ```bash
   git push --force --all
   git push --force --tags
   ```
6. Semua klon lain harus diminta re-clone (`git fetch` tidak cukup — riwayat berubah).
7. **Putar semua secret** yang pernah ada di riwayat (Telegram bot token via BotFather,
   regenerate API key di DB, ganti password admin) — anggap semuanya sudah bocor.

**Kontrol:** pastikan secret benar-benar hilang:
```bash
git grep -iE "1382696353|b-9Jvv|unisbank" $(git rev-list --all) || echo "bersih"
```

---

## Kriteria Penerimaan Umum

- [ ] Tidak ada secret live di working tree / git history (`git grep -i "unicbank\|1382696353\|b-9Jvv"`).
- [ ] Semua endpoint CRUD & `/predict` memerlukan auth yang sah (401/403 bila tidak).
- [ ] Tidak ada `pickle.load` pada data yang berasal dari input user.
- [ ] `/tests` (atau smoke test manual) untuk: login, prediksi, CRUD dataset/responses, training, dan kedua bot.
- [ ] Build frontend lulus (`npm run build`).
- [ ] Backend tidak mengembalikan 500 pada input tidak valid (harus 400/422).