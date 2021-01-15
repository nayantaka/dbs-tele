import tools from '@/tools'

export default function (ctx, inject) {
  ctx.$tools = tools
  inject('tools', tools)
}
