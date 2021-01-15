import api from '@/api'

export default function (ctx, inject) {
  const { $axios, $tools } = ctx
  _.forEach(api, (val) => {
    val.$axios = $axios
    val.$tools = $tools
  })
  ctx.$api = api
  inject('api', api)
}
