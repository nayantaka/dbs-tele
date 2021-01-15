<template>
  <b-col lg="5">
    <b-form class="card shadow-lg border-0 rounded-lg mt-5" @submit.prevent="submitRefresh">
      <b-card-header>
        <h3 class="text-center font-weight-light my-4">
          Masuk Kembali
        </h3>
      </b-card-header>
      <b-card-body>
        <h5 class="text-center">
          {{ info.name }}
        </h5>
        <b-button type="submit" class="w-100" variant="primary">
          Silahkan Masuk Kembali
        </b-button>
      </b-card-body>
    </b-form>
  </b-col>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  middleware: ['isnt-refresh'],
  layout: 'login-register',
  computed: {
    ...mapGetters('authorization', {
      info: 'info'
    })
  },
  methods: {
    async submitRefresh () {
      try {
        await this.$store.dispatch('authorization/refresh')
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil masuk kembali'
        })
        this.$router.push('/')
      } catch (err) {
        this.$store.commit('authorization/setToken', '')
        this.$store.commit('authorization/setRefreshToken', '')
        this.$store.commit('authorization/setInfo', {})
        this.$tools.notification({
          title: 'Error',
          type: 'error',
          message: err.message
        })
        this.$router.push('/login')
      }
    }
  }
}
</script>
