<template>
  <div :class="['dashboard', toggle && 'toggle']">
    <common-header
      :toggle="toggle"
      @toggle-sidebar="toggleSidebar"
    />
    <div class="dashboard-container">
      <common-sidebar
        :toggle="toggle"
        @toggle-sidebar="toggleSidebar"
      />
      <div class="dashboard-content">
        <b-container fluid>
          <common-page-title />
          <nuxt />
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      toggle: false
    }
  },
  methods: {
    toggleSidebar (toggle) {
      this.toggle = toggle
    }
  }
}
</script>
