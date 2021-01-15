import createPersistedState from 'vuex-persistedstate'
import SecureLS from 'secure-ls'

const ls = new SecureLS({ isCompression: true })

export default function ({ store }) {
  createPersistedState({
    key: 'smartfaq',
    paths: ['authorization.token', 'authorization.refresh_token', 'authorization.info'],
    storage: {
      getItem: key => ls.get(key),
      setItem: (key, value) => ls.set(key, value),
      removeItem: key => ls.remove(key)
    }
  })(store)
}
