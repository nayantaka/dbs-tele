import Vue from 'vue'

const typeToIcon = function typeToIcon (type) {
  switch (type) {
    case 'danger':
      return 'exclamation-circle'
    case 'warning':
      return 'exclamation-triangle'
    case 'success':
      return 'check'
    case 'info':
      return 'eye'
    default:
      return 'bell'
  }
}

export default function (opts) {
  switch (opts.type) {
    case 'error':
    case 'err':
      opts.type = 'danger'
      break
    case 'warn':
      opts.type = 'warning'
      break
  }
  const vm = new Vue()
  const icon = typeToIcon(opts.type)
  const titleNode = vm.$createElement('div', {
    class: 'd-flex align-items-center'
  }, [
    vm.$createElement('fa-layers', {
      class: 'fa-fw mr-1'
    }, [
      vm.$createElement('fa-icon', {
        attrs: {
          icon: ['fas', icon]
        }
      })
    ]), vm.$createElement('strong', {
      class: 'mr-auto'
    }, [opts.title])
  ])
  vm.$bvToast.toast(opts.message, {
    title: [titleNode],
    variant: opts.type,
    solid: true,
    toaster: 'b-toaster-bottom-right',
    appendToast: true,
    autoHideDelay: 1500
  })
}
