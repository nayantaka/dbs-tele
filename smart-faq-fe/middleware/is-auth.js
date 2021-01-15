export default function ({ store, redirect }) {
  const token = store.getters['authorization/token']
  const refresh_token = store.getters['authorization/refresh_token']
  if (_.isEmpty(token) && _.isEmpty(refresh_token)) {
    return redirect('/login')
  }
}
