<template>
  <b-row>
    <b-col cols="12">
      <dataset-pencarian v-model="cari" />
    </b-col>
    <b-col cols="12">
      <b-card no-body class="mb-3">
        <b-card-header class="d-flex align-items-center ">
          Dataset Lists
          <b-button-group class="ml-auto" size="sm">
            <b-button variant="primary" :disabled="$fetchState.pending" @click="modal.tambah = true">
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
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle" />
              <strong>Loading...</strong>
            </div>
          </template>
          <template #cell(context)="{item}">
            {{ $tools.categoryNormalize(item.context) }}
          </template>
          <template #cell(intent)="{item}">
            {{ $tools.categoryNormalize(item.intent) }}
          </template>
          <template #cell(actions)="{item}">
            <b-button-group size="sm">
              <b-button variant="primary" @click="clickActions(item, 'edit')">
                <fa-layers class="fa-fw">
                  <fa-icon :icon="['fas', 'edit']" />
                </fa-layers>
              </b-button>
              <b-button variant="danger" @click="clickActions(item, 'delete')">
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
    <dataset-modal-tambah v-model="modal.tambah" @refetch="refetch" />
    <dataset-modal-edit v-model="modal.edit" @refetch="refetch" />
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  middleware: ['is-auth', 'is-refresh'],
  async fetch () {
    try {
      await this.$store.dispatch('dataset/category')
    } catch (err) {}
    try {
      await this.$store.dispatch('dataset/getAll', {
        ...this.cari,
        page: this.page,
        per_page: this.perpage
      })
    } catch (err) {}
  },
  data () {
    return {
      cari: {},
      page: 1,
      perpage: 10,
      modal: {
        tambah: false,
        edit: false
      }
    }
  },
  computed: {
    ...mapGetters('dataset', {
      lists: 'lists',
      pagination: 'pagination'
    }),
    fields () {
      return [
        'context',
        'intent',
        'paragraph',
        'actions'
      ]
    }
  },
  watch: {
    cari: {
      deep: true,
      async handler () {
        await this.refetch()
      }
    },
    async page () {
      await this.$fetch()
    }
  },
  mounted () {
    this.setPageTitle()
  },
  methods: {
    async refetch () {
      this.page = 1
      await this.$fetch()
    },
    setPageTitle () {
      this.$store.commit('page-title/setAll', {
        title: 'Dataset',
        breadcrumb: [
          {
            text: 'Dashboard',
            to: '/'
          },
          {
            text: 'Dataset',
            active: true
          }
        ]
      })
    },
    async clickActions (item, method = 'edit') {
      try {
        await this.$store.dispatch('dataset/getById', item)
        if (method === 'edit') {
          this.modal.edit = true
        } else {
          const res = await this.$swal({
            title: 'Yakin hapus?',
            text: 'Kamu tidak bisa restore data ini',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Hapus',
            cancelButtonText: 'Tidak'
          })
          if (res.value) {
            await this.$store.dispatch('dataset/delete', item)
            await this.refetch()
            this.$tools.notification({
              title: 'Success',
              type: 'success',
              message: 'Berhasil hapus data'
            })
          }
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
