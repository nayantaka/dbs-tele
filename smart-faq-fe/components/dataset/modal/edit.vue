<template>
  <b-modal
    v-model="modal"
    title="Ganti Dataset"
    @show="setData"
    @hidden="resetModal"
    @ok="submitSave"
  >
    <b-form @submit.prevent="submitSave">
      <b-form-group
        label="Context"
        label-for="context"
        label-class="small"
      >
        <b-input
          id="context"
          v-model="$v.form.context.$model"
          placeholder="Context"
          :state="validData($v.form.context)"
        />
        <template v-if="validData($v.form.context) !== null && !validData($v.form.context)">
          <b-form-invalid-feedback v-if="!$v.form.context.required">
            Context harus di isi
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
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
        label="Paragraph"
        label-for="paragraph"
        label-class="small"
      >
        <b-textarea
          id="paragraph"
          v-model="$v.form.paragraph.$model"
          placeholder="Paragraph"
          :state="validData($v.form.paragraph)"
        />
        <template v-if="validData($v.form.paragraph) !== null && !validData($v.form.paragraph)">
          <b-form-invalid-feedback v-if="!$v.form.paragraph.required">
            Paragraph harus di isi
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
        context: '',
        intent: '',
        paragraph: ''
      }
    }
  },
  computed: {
    ...mapGetters('dataset', {
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
      context: { required },
      intent: { required },
      paragraph: { required }
    }
  },
  methods: {
    setData () {
      this.form = {
        context: this.info.context,
        intent: this.info.intent,
        paragraph: this.info.paragraph
      }
    },
    resetModal () {
      this.form = {
        context: '',
        intent: '',
        paragraph: ''
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
        await this.$store.dispatch('dataset/update', {
          id: this.info.id,
          ...this.form
        })
        this.modal = false
        this.$emit('refetch')
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil ganti dataset'
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
