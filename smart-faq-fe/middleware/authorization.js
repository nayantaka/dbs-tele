export default function ({ store, $axios }) {
  const token = store.getters['authorization/token']
  const refresh_token = store.getters['authorization/refresh_token']
  if (_.isEmpty(refresh_token)) {
    if (!_.isEmpty(token)) {
      store.commit('authorization/setToken', '')
    }
    store.commit('authorization/setInfo', {})
    $axios.setToken(null)
  } else if (_.isEmpty(token) && !_.isEmpty(refresh_token)) {
    $axios.setToken(refresh_token, 'Bearer')
  } else {
    $axios.setToken(token, 'Bearer')
  }
}
