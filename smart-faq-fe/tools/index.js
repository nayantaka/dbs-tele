const files = require.context('.', false, /\.js$/)
const tools = {}

files.keys().forEach((fileName) => {
  if (fileName === './index.js') {
    return
  }
  const name = (() => {
    const fileNameArray = fileName.replace(/(\.\/|\.js)/g, '').split('-')
    return fileNameArray.map((n, i) => {
      if (i > 0) {
        return _.capitalize(n)
      }
      return n
    }).join('')
  })()
  tools[name] = files(fileName).default
})

export default tools
