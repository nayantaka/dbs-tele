export default {
  async getAll (data = {}) {
    try {
      const { perpage = 10, page = 1, ...redata } = data
      const { result: { data: lists, pagination } } = await this.$axios.$get('/dataset', {
        params: {
          ...this.$tools.parseCriteria(redata),
          page,
          per_page: perpage
        }
      })
      return {
        lists,
        pagination
      }
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async getById (data) {
    try {
      const { id } = data
      const { result } = await this.$axios.$get(`/dataset/${id}`)
      return result
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async create (data) {
    try {
      await this.$axios.$post('/dataset', data)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async update (data) {
    try {
      const { id, ...redata } = data
      await this.$axios.$put(`/dataset/${id}`, redata)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async delete (data) {
    try {
      const { id } = data
      await this.$axios.$delete(`/dataset/${id}`)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async category () {
    try {
      const { result } = await this.$axios.$get('/dataset/category')
      return result
    } catch (err) {
      return Promise.reject(err)
    }
  }
}
