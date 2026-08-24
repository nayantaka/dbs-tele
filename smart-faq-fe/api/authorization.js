export default {
  async changeProfile (data) {
    try {
      const { id, ...redata } = data
      const { result } = await this.$axios.$put(`/user/${id}`, redata)
      return result
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async refresh () {
    try {
      // Token diperbarui lewat HttpOnly cookie; tidak ada token di body
      await this.$axios.$post('/auth/refresh')
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async register (data) {
    try {
      await this.$axios.$post('/auth/register', data)
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async login (data) {
    try {
      // Token dikelola server lewat HttpOnly cookie; hanya data user yang dikembalikan
      const { result: { data: info } } = await this.$axios.$post('/auth/login', data)
      return {
        info
      }
    } catch (err) {
      return Promise.reject(err)
    }
  },
  async logout () {
    try {
      await this.$axios.$post('/auth/logout')
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  }
}
