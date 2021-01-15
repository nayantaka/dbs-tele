const initState = {
  title: 'Dashboard',
  breadcrumb: [
    {
      text: 'Dashboard',
      active: true
    }
  ]
}

export const state = () => initState

export const getters = {
  title (state) {
    return state.title
  },
  breadcrumb (state) {
    return state.breadcrumb
  }
}

export const mutations = {
  setTitle (state, payload) {
    state.title = _.isEmpty(payload) ? '' : payload
  },
  setBreadcrumb (state, payload) {
    state.breadcrumb = _.isEmpty(payload) ? [] : payload
  },
  setAll (state, payload) {
    const { title, breadcrumb } = payload
    state.title = _.isEmpty(title) ? '' : title
    state.breadcrumb = _.isEmpty(breadcrumb) ? [] : breadcrumb
  }
}
