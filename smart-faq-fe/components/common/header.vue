<template>
  <b-navbar type="dark" variant="dark" fixed="top" class="header">
    <b-navbar-brand to="/" @click="clickBrandMobile">
      Smart FAQ
    </b-navbar-brand>
    <b-button class="header-bars order-1 order-lg-0" size="sm" variant="link" @click="clickBars">
      <fa-layers class="fa-fw">
        <fa-icon :icon="['fas', 'bars']" />
      </fa-layers>
    </b-button>
    <b-navbar-nav class="ml-auto">
      <b-nav-item-dropdown right>
        <template #button-content>
          {{ info.name }}
        </template>
        <b-dropdown-item to="/setting">
          Setting
        </b-dropdown-item>
        <b-dropdown-divider />
        <b-dropdown-item @click="clickLogout">
          Logout
        </b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    toggle: {
      type: Boolean,
      require: false
    }
  },
  computed: {
    ...mapGetters('authorization', {
      info: 'info'
    })
  },
  methods: {
    clickBars () {
      this.$emit('toggle-sidebar', !this.toggle)
    },
    clickBrandMobile () {
      const winWidth = $(window).width()
      if (winWidth <= 767) {
        if (this.toggle) {
          this.$emit('toggle-sidebar', false)
        }
      }
    },
    clickLogout () {
      this.$store.commit('authorization/setToken', '')
      this.$store.commit('authorization/setRefreshToken', '')
      this.$store.commit('authorization/setInfo', {})
      this.$router.push('/login')
    }
  }
}
</script>
