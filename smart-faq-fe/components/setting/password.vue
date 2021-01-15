<template>
  <b-form class="card" @submit.prevent="submitProfile">
    <b-card-header>
      Setting Password
    </b-card-header>
    <b-card-body>
      <b-form-group
        label="Password"
        label-for="password"
        label-class="small"
      >
        <b-input
          id="password"
          v-model="$v.form.password.$model"
          type="password"
          placeholder="Password"
          :state="validData($v.form.password)"
        />
        <template v-if="validData($v.form.password) !== null && !validData($v.form.password)">
          <b-form-invalid-feedback v-if="!$v.form.password.required">
            Password harus di isi
          </b-form-invalid-feedback>
        </template>
      </b-form-group>
      <b-form-group
        label="Kon. Password"
        label-for="kon_password"
        label-class="small"
      >
        <b-input
          id="password"
          v-model="$v.form.kon_password.$model"
          type="password"
          placeholder="Kon. Password"
          :state="validData($v.form.kon_password)"
        />
        <template v-if="validData($v.form.kon_password) !== null && !validData($v.form.kon_password)">
          <b-form-invalid-feedback v-if="!$v.form.password.sameAs">
            Kon. Password harus sama dengan password
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
import { required, sameAs } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      form: {
        password: '',
        kon_password: ''
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
      password: { required },
      kon_password: { sameAs: sameAs('password') }
    }
  },
  methods: {
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
          password: this.form.password
        })
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil ganti password'
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
