export default {
  async start () {
    try {
      await this.$axios.$post('/train')
      return Promise.resolve()
    } catch (err) {
      return Promise.reject(err)
    }
  }
}
