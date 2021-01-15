<template>
  <b-row>
    <b-col cols="12">
      <setting-profile />
    </b-col>
    <b-col cols="12">
      <setting-password />
    </b-col>
  </b-row>
</template>

<script>
export default {
  middleware: ['is-auth', 'is-refresh'],
  mounted () {
    this.setPageTitle()
  },
  methods: {
    setPageTitle () {
      this.$store.commit('page-title/setAll', {
        title: 'Setting',
        breadcrumb: [
          {
            text: 'Dashboard',
            to: '/'
          },
          {
            text: 'Setting',
            active: true
          }
        ]
      })
    }
  }
}
</script>
