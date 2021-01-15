export default function ({ store, $axios, $tools }) {
  $axios.onError((err) => {
    err = $tools.error(err)
    if (err.message.includes('Token has expired')) {
      store.commit('authorization/setToken', '')
    } else if (err.message.includes('Bad Authorization header') || err.message.includes('Missing Authorization Header')) {
      store.commit('authorization/setToken', '')
      store.commit('authorization/setRefreshToken', '')
      store.commit('authorization/setInfo', {})
    }
    return Promise.reject(err)
  })
}
