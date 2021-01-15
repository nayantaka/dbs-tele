export default function (value) {
  const valSplit = value.split('_').map((v) => {
    if (_.includes(['pmb', 'krs'], v)) {
      return v.toUpperCase()
    }
    return _.capitalize(v)
  })
  return valSplit.join(' ')
}
