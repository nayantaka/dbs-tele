<template>
  <b-row>
    <b-col cols="12">
      <b-card no-body class="mb-3">
        <b-card-header class="d-flex align-items-center ">
          Api Key Lists
          <b-button-group class="ml-auto" size="sm">
            <b-button variant="primary" :disabled="$fetchState.pending" @click="createApi">
              <fa-layers class="fa-fw">
                <fa-icon :icon="['fas', 'plus']" />
              </fa-layers>
            </b-button>
            <b-button variant="info" :disabled="$fetchState.pending" @click="refetch">
              <fa-layers class="fa-fw">
                <fa-icon :icon="['fas', 'sync']" spin />
              </fa-layers>
            </b-button>
          </b-button-group>
        </b-card-header>
        <b-table
          responsive
          class="mb-0"
          :fields="fields"
          :items="lists"
          :busy="$fetchState.pending"
        >
          <template #cell(actions)="{item}">
            <b-button-group size="sm">
              <b-button variant="primary" @click="copyFile(item)">
                <fa-layers class="fa-fw">
                  <fa-icon :icon="['fas', 'copy']" />
                </fa-layers>
              </b-button>
              <b-button variant="danger" @click="clickActions(item)">
                <fa-layers class="fa-fw">
                  <fa-icon :icon="['fas', 'trash']" />
                </fa-layers>
              </b-button>
            </b-button-group>
          </template>
        </b-table>
        <b-card-footer>
          <b-pagination
            v-model="page"
            :total-rows="pagination.total_record"
            :per-page="perpage"
            class="mb-0"
          />
        </b-card-footer>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import * as clipboard from 'clipboard-polyfill/text'

export default {
  async fetch () {
    try {
      await this.$store.dispatch('apikey/getAll')
    } catch (err) {}
  },
  data () {
    return {
      page: 1,
      perpage: 10
    }
  },
  computed: {
    ...mapGetters('apikey', {
      lists: 'lists',
      pagination: 'pagination'
    }),
    fields () {
      return [
        'key',
        'actions'
      ]
    }
  },
  watch: {
    async page () {
      await this.$fetch()
    }
  },
  mounted () {
    this.setPageTitle()
  },
  methods: {
    async createApi () {
      try {
        await this.$store.dispatch('apikey/create')
        await this.$fetch()
      } catch (err) {
        this.$tools.notification({
          title: 'Error',
          type: 'error',
          message: err.message
        })
      }
    },
    async refetch () {
      this.page = 1
      await this.$fetch()
    },
    async copyFile (item) {
      try {
        await clipboard.writeText(item.key)
      } catch (err) {
        this.$tools.notification({
          title: 'Error',
          type: 'error',
          message: err.message
        })
      }
    },
    setPageTitle () {
      this.$store.commit('page-title/setAll', {
        title: 'Api Key',
        breadcrumb: [
          {
            text: 'Dashboard',
            to: '/'
          },
          {
            text: 'Api Key',
            active: true
          }
        ]
      })
    },
    async clickActions (item) {
      try {
        await this.$store.dispatch('apikey/getById', item)
        const res = await this.$swal({
          title: 'Yakin hapus?',
          text: 'Kamu tidak bisa restore data ini',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Hapus',
          cancelButtonText: 'Tidak'
        })
        if (res.value) {
          await this.$store.dispatch('apikey/delete', item)
          await this.refetch()
          this.$tools.notification({
            title: 'Success',
            type: 'success',
            message: 'Berhasil hapus data'
          })
        }
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
