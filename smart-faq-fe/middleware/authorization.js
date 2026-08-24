export default function ({ $axios }) {
  // Kredensial di-handle lewat HttpOnly cookie; pastikan axios mengirim cookie
  $axios.defaults.withCredentials = true
}