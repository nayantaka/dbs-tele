<template>
  <div class="sidebar">
    <template v-for="(list, li) in lists">
      <div :key="li" class="sidebar-lists">
        <div class="sidebar-lists-title">
          {{ list.name }}
        </div>
        <div class="sidebar-menus">
          <template v-for="(menu, mi) in list.menus">
            <b-link
              :key="mi"
              class="sidebar-menus-link"
              :to="menu.to"
              @click="clickLink"
            >
              <fa-layers class="fa-fw">
                <fa-icon :icon="menu.icon" />
              </fa-layers>
              {{ menu.name }}
            </b-link>
          </template>
        </div>
      </div>
    </template>
    <div class="sidebar-lists">
      <div class="sidebar-lists-title">
        Training
      </div>
      <div class="sidebar-menus">
        <b-link class="sidebar-menus-link" @click.prevent="clickStartTraining">
          <fa-layers class="fa-fw">
            <fa-icon :icon="['fas', 'play']" />
          </fa-layers>
          Start Training
        </b-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    toggle: {
      type: Boolean,
      require: false
    }
  },
  computed: {
    lists () {
      return this.$tools.lists
    }
  },
  methods: {
    clickLink () {
      const winWidth = $(window).width()
      if (winWidth <= 767) {
        if (this.toggle) {
          this.$emit('toggle-sidebar', false)
        }
      }
    },
    async clickStartTraining () {
      try {
        await this.$api.train.start()
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Start Training'
        })
      } catch (err) {
        this.$tools.notification({
          title: 'Error',
          type: 'error',
          message: err.message
        })
      }
    }
  }
}
</script>
