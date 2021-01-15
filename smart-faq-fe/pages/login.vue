<template>
  <b-col lg="5">
    <b-form class="card shadow-lg border-0 rounded-lg mt-5" @submit.prevent="submitLogin">
      <b-card-header>
        <h3 class="text-center font-weight-light my-4">
          Login
        </h3>
      </b-card-header>
      <b-card-body>
        <b-form-group
          label="Username"
          label-for="username"
          label-class="small"
        >
          <b-input
            id="username"
            v-model="$v.form.username.$model"
            placeholder="Username"
            :state="validData($v.form.username)"
          />
          <template v-if="validData($v.form.username) !== null && !validData($v.form.username)">
            <b-form-invalid-feedback v-if="!$v.form.username.required">
              Username harus di isi
            </b-form-invalid-feedback>
          </template>
        </b-form-group>
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
        <b-button type="submit" variant="primary" class="w-100">
          Login
        </b-button>
      </b-card-body>
      <b-card-footer class="text-center">
        <div class="small">
          <b-link to="/register">
            Need an account? Sign up!
          </b-link>
        </div>
      </b-card-footer>
    </b-form>
  </b-col>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

export default {
  middleware: ['isnt-auth', 'is-refresh'],
  layout: 'login-register',
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  validations: {
    form: {
      username: { required },
      password: { required }
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
    async submitLogin () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      try {
        await this.$store.dispatch('authorization/login', {
          username: this.form.username,
          password: this.form.password
        })
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil login'
        })
        this.$router.push('/')
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
