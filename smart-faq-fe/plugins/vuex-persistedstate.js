import createPersistedState from 'vuex-persistedstate'

export default function ({ store }) {
  createPersistedState({
    key: 'smartfaq',
    // Hanya info non-sensitif (nama/email) yang dipersistensikan di localStorage polos.
    // Token hidup di HttpOnly cookie, dan secure-ls/crypto-js (yang rentan) sudah tidak digunakan.
    paths: ['authorization.info']
  })(store)
}