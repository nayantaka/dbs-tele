const initState = {
  lists: [],
  pagination: {},
  info: {}
}

export const state = () => initState

export const getters = {
  lists (state) {
    return state.lists
  },
  pagination (state) {
    return state.pagination
  },
  info (state) {
    return state.info
  }
}

export const mutations = {
  setLists (state, payload) {
    state.lists = _.isEmpty(payload) ? [] : payload
  },
  setPagination (state, payload) {
    state.pagination = _.isEmpty(payload) ? {} : payload
  },
  setInfo (state, payload) {
    state.info = _.isEmpty(payload) ? {} : payload
  }
}

export const actions = {
  async getAll ({ commit }, payload) {
    try {
      const { lists, pagination } = await this.$api.apikey.getAll(payload)
      commit('setLists', lists)
      commit('setPagination', pagination)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async getById ({ commit }, payload) {
    try {
      const data = await this.$api.apikey.getById(payload)
      commit('setInfo', data)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async create (_store, payload) {
    try {
      await this.$api.apikey.create(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async update (_store, payload) {
    try {
      await this.$api.apikey.update(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async delete (_store, payload) {
    try {
      await this.$api.apikey.delete(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  }
}
