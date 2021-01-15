const axios = require('axios')
module.exports = async (question) => {
  try {
    const res = await axios.get(process.env.PREDICT_ENDPOINT, {
      params: {
        sentence: question
      },
      headers: {
        'x-api-key': process.env.API_KEY
      }
    })

    return res.data.result
  }
  catch (err) {
    return `Maaf terjadi kesalahan sistem`
  }
}
