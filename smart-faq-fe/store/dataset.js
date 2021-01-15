const initState = {
  lists: [],
  pagination: {},
  category: [],
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
  category (state) {
    return state.category
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
  setCategory (state, payload) {
    state.category = _.isEmpty(payload) ? [] : payload
  },
  setInfo (state, payload) {
    state.info = _.isEmpty(payload) ? {} : payload
  }
}

export const actions = {
  async getAll ({ commit }, payload) {
    try {
      const { lists, pagination } = await this.$api.dataset.getAll(payload)
      commit('setLists', lists)
      commit('setPagination', pagination)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async getById ({ commit }, payload) {
    try {
      const data = await this.$api.dataset.getById(payload)
      commit('setInfo', data)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async category ({ commit }, payload) {
    try {
      const data = await this.$api.dataset.category(payload)
      commit('setCategory', data)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async create (_store, payload) {
    try {
      await this.$api.dataset.create(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async update (_store, payload) {
    try {
      await this.$api.dataset.update(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  },
  async delete (_store, payload) {
    try {
      await this.$api.dataset.delete(payload)
      return Promise.resolve()
    } catch (err) {
      return Promise.resolve()
    }
  }
}
