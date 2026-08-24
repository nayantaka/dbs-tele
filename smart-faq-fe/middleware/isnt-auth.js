export default function ({ store, redirect }) {
  const info = store.getters['authorization/info']
  if (!_.isEmpty(info)) {
    return redirect('/')
  }
}