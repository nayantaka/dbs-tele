const initState = {
  // Info user non-sensitif dijadikan penanda "sudah login" untuk gating UI.
  // Kredensial asli (access/refresh token) hanya ada di HttpOnly cookie server.
  info: {}
}

export const state = () => initState

export const getters = {
  info (state) {
    return state.info
  }
}

export const mutations = {
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
      await this.$api.authorization.refresh()
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async login ({ commit }, payload) {
    try {
      const { info } = await this.$api.authorization.login(payload)
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
  },
  async logout ({ commit }) {
    try {
      await this.$api.authorization.logout()
      commit('setInfo', {})
      return Promise.resolve()
    } catch (err) {
      commit('setInfo', {})
      return Promise.reject(err)
    }
  }
}