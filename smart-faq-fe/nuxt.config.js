import webpack from 'webpack'

require('dotenv').config()

export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'Smart FAQ',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  loading: {
    color: 'white'
  },

  router: {
    middleware: ['authorization']
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ['@/assets/styles/app.scss'],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '@/plugins/tools',
    '@/plugins/api',
    '@/plugins/moment',
    '@/plugins/vuex-persistedstate',
    '@/plugins/axios',
    '@/plugins/vue-fragment',
    '@/plugins/vuelidate',
    '@/plugins/vue-select',
    '@/plugins/vue-sweetalert2'
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: {
    dirs: [
      '~/components',
      {
        path: '~/components/common/',
        prefix: 'Common'
      },
      {
        path: '~/components/setting/',
        prefix: 'Setting'
      },
      {
        path: '~/components/dataset/',
        prefix: 'Dataset'
      },
      {
        path: '~/components/dataset/modal',
        prefix: 'DatasetModal'
      },
      {
        path: '~/components/response/',
        prefix: 'Response'
      },
      {
        path: '~/components/response/modal',
        prefix: 'ResponseModal'
      }
    ]
  },

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module'
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/fontawesome',
    'vue-sweetalert2/nuxt'
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    baseURL: process.env.BE_CONNECTION
  },

  bootstrapVue: {
    bootstrapCSS: false,
    bootstrapVueCSS: false
  },

  fontawesome: {
    component: 'fa',
    suffix: true,
    icons: {
      solid: true,
      regular: true,
      brands: true
    }
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        _: 'lodash',
        moment: 'moment'
      })
    ]
  }
}
