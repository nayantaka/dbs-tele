// Token kini di-manage lewat HttpOnly cookie; refresh otomatis oleh interceptor axios.
// Middleware ini dipertahankan sebagai pass-through agar route yang menyarankannya tetap valid.
export default function () {
  return true
}