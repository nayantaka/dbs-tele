const dateFIll = ['startDate', 'endDate', 'createAt', 'updateAt']

export default function (criteria) {
  const re = {}
  _.forEach(criteria, (val, key) => {
    if (_.includes(dateFIll, key)) {
      val = moment(val).format('DD-MM-YYYY')
    }
    re[key] = encodeURIComponent(val)
  })
  return re
}
