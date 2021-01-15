const files = require.context('.', false, /\.js$/)
const apis = {}

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
  apis[name] = files(fileName).default
})

export default apis
