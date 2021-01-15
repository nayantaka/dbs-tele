const initState = {
  token: '',
  refresh_token: '',
  info: {}
}

export const state = () => initState

export const getters = {
  token (state) {
    return state.token
  },
  refresh_token (state) {
    return state.refresh_token
  },
  info (state) {
    return state.info
  }
}

export const mutations = {
  setToken (state, payload) {
    state.token = _.isEmpty(payload) ? '' : payload
  },
  setRefreshToken (state, payload) {
    state.refresh_token = _.isEmpty(payload) ? '' : payload
  },
  setInfo (state, payload) {
    state.info = _.isEmpty(payload) ? {} : payload
  }
}

export const actions = {
  async changeProfile ({ commit }, payload) {
    try {
      const info = await this.$api.authorization.changeProfile(payload)
      commit('setInfo', info)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async refresh ({ commit }, _payload) {
    try {
      const { token } = await this.$api.authorization.refresh()
      commit('setToken', token)
      return token
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async login ({ commit }, payload) {
    try {
      const { token, refresh_token, info } = await this.$api.authorization.login(payload)
      commit('setToken', token)
      commit('setRefreshToken', refresh_token)
      commit('setInfo', info)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async register (_store, payload) {
    try {
      await this.$api.authorization.register(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  }
}
