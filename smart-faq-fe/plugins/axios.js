function readCookie (name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[1]) : ''
}

export default function ({ store, $axios }) {
  $axios.defaults.withCredentials = true

  // Kirim header CSRF (double-submit) untuk proteksi cookie-based auth
  $axios.onRequest((config) => {
    const isRefresh = /\/auth\/refresh/.test(config.url || '')
    const csrfToken = readCookie(isRefresh ? 'csrf_refresh_token' : 'csrf_access_token')
    if (csrfToken) {
      config.headers.common['X-CSRF-TOKEN'] = csrfToken
    }
  })

  $axios.onError((err) => {
    err = $tools.error(err)
    if (
      err.message.includes('Token has expired') ||
      err.message.includes('Bad Authorization header') ||
      err.message.includes('Missing Authorization Header')
    ) {
      store.commit('authorization/setInfo', {})
    }
    return Promise.reject(err)
  })
}