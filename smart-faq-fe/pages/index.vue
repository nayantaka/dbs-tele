<template>
  <b-row>
    <b-col cols="12">
      <b-jumbotron header="Smart FAQ" lead="Aplikasi Smart FAQ" />
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
        title: 'Dashboard',
        breadcrumb: [
          {
            text: 'Dashboard',
            active: true
          }
        ]
      })
    }
  }
}
</script>
