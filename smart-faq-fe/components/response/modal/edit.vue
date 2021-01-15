<template>
  <b-modal
    v-model="modal"
    title="Ganti Response"
    @show="setData"
    @hidden="resetModal"
    @ok="submitSave"
  >
    <b-form @submit.prevent="submitSave">
      <b-form-group
        label="Intent"
        label-for="intent"
        label-class="small"
      >
        <b-select
          id="intent"
          v-model="$v.form.intent.$model"
          :options="categoryOpts"
          :state="validData($v.form.intent)"
        />
        <template v-if="validData($v.form.intent) !== null && !validData($v.form.intent)">
          <b-form-invalid-feedback v-if="!$v.form.intent.required">
            Intent harus di isi
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
      <b-form-group
        label="Response"
        label-for="response"
        label-class="small"
      >
        <b-textarea
          id="response"
          v-model="$v.form.response.$model"
          placeholder="Paragraph"
          :state="validData($v.form.response)"
        />
        <template v-if="validData($v.form.response) !== null && !validData($v.form.response)">
          <b-form-invalid-feedback v-if="!$v.form.response.required">
            Response harus di isi
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import { mapGetters } from 'vuex'

export default {
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      form: {
        intent: '',
        response: ''
      }
    }
  },
  computed: {
    ...mapGetters('response', {
      categorys: 'category',
      info: 'info'
    }),
    categoryOpts () {
      const re = [
        {
          value: '', text: 'Silahkan Pilih'
        }
      ]
      if (_.isEmpty(this.categorys)) { return re }
      this.categorys.forEach((c) => {
        re.push({
          value: c,
          text: this.$tools.categoryNormalize(c)
        })
      })
      return re
    },
    modal: {
      set (val) {
        this.$emit('input', val)
      },
      get () {
        return this.value
      }
    }
  },
  validations: {
    form: {
      intent: { required },
      response: { required }
    }
  },
  methods: {
    setData () {
      this.form = {
        intent: this.info.intent,
        response: this.info.response
      }
    },
    resetModal () {
      this.form = {
        intent: '',
        response: ''
      }
      this.$nextTick(() => {
        this.$v.$reset()
      })
    },
    validData (name) {
      const { $dirty, $error } = name
      if ($dirty) {
        return !$error
      }
      return null
    },
    async submitSave () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      try {
        await this.$store.dispatch('response/update', {
          id: this.info.id,
          ...this.form
        })
        this.modal = false
        this.$emit('refetch')
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil ganti response'
        })
      } catch (err) {
        this.modal = false
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
