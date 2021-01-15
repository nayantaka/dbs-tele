<template>
  <b-form class="card mb-3" @submit.prevent="submitProfile">
    <b-card-header>
      Setting Profile
    </b-card-header>
    <b-card-body>
      <b-form-group
        label="Email"
        label-for="email"
        label-class="small"
      >
        <b-input
          id="email"
          v-model="$v.form.email.$model"
          type="email"
          placeholder="Email"
          :state="validData($v.form.email)"
        />
        <template v-if="validData($v.form.email) !== null && !validData($v.form.email)">
          <b-form-invalid-feedback v-if="!$v.form.email.required">
            Email harus di isi
          </b-form-invalid-feedback>
          <b-form-invalid-feedback v-if="!$v.form.email.email">
            Format email salah
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
      <b-form-group
        label="Nama"
        label-for="name"
        label-class="small"
        class="mb-0"
      >
        <b-input
          id="name"
          v-model="$v.form.name.$model"
          placeholder="Nama"
          :state="validData($v.form.name)"
        />
        <template v-if="validData($v.form.name) !== null && !validData($v.form.name)">
          <b-form-invalid-feedback v-if="!$v.form.name.required">
            Nama harus di isi
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
    </b-card-body>
    <b-card-footer>
      <b-button type="submit" variant="primary">
        Save
      </b-button>
    </b-card-footer>
  </b-form>
</template>

<script>
import { mapGetters } from 'vuex'
import { required, email } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      form: {
        email: '',
        name: ''
      }
    }
  },
  computed: {
    ...mapGetters('authorization', {
      info: 'info'
    })
  },
  validations: {
    form: {
      email: { required, email },
      name: { required }
    }
  },
  mounted () {
    this.setDefault()
  },
  methods: {
    setDefault () {
      this.form = {
        email: this.info.email,
        name: this.info.name
      }
    },
    validData (name) {
      const { $dirty, $error } = name
      if ($dirty) {
        return !$error
      }
      return null
    },
    async submitProfile () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      try {
        await this.$store.dispatch('authorization/changeProfile', {
          id: this.info.id,
          name: this.form.name,
          email: this.form.email
        })
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil ganti profile'
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
