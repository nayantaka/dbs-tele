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
      const { result: { access_token } } = await this.$axios.$post('/auth/refresh')
      return {
        token: access_token
      }
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
      const { result: { access_token, refresh_token, data: info } } = await this.$axios.$post('/auth/login', data)
      return {
        token: access_token,
        refresh_token,
        info
      }
    } catch (err) {
      return Promise.reject(err)
    }
  }
}
