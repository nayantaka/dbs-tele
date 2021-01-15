<template>
  <b-col lg="7">
    <b-form class="card shadow-lg border-0 rounded-lg mt-5" @submit.prevent="submitRegister">
      <b-card-header>
        <h3 class="text-center font-weight-light my-4">
          Register
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
        <b-form-row>
          <b-col md="6">
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
          </b-col>
          <b-col md="6">
            <b-form-group
              label="Nama"
              label-for="name"
              label-class="small"
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
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col md="6">
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
          </b-col>
          <b-col md="6">
            <b-form-group
              label="Konfirmasi Password"
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
                  Konfirmasi. Password harus sama dengan password
                </b-form-invalid-feedback>
              </template>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-button type="submit" variant="primary" class="w-100">
          Register
        </b-button>
      </b-card-body>
      <b-card-footer class="text-center">
        <div class="small">
          <b-link to="/login">
            Have an account? Go to login
          </b-link>
        </div>
      </b-card-footer>
    </b-form>
  </b-col>
</template>

<script>
import { required, sameAs, email } from 'vuelidate/lib/validators'

export default {
  middleware: ['isnt-auth', 'is-refresh'],
  layout: 'login-register',
  data () {
    return {
      form: {
        username: '',
        email: '',
        name: '',
        password: '',
        kon_password: ''
      }
    }
  },
  validations: {
    form: {
      username: { required },
      email: { required, email },
      name: { required },
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
    async submitRegister () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      try {
        await this.$store.dispatch('authorization/register', {
          username: this.form.username,
          name: this.form.name,
          email: this.form.email,
          password: this.form.password
        })
        this.$tools.notification({
          title: 'Success',
          type: 'success',
          message: 'Berhasil register'
        })
        this.$router.push('/login')
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
