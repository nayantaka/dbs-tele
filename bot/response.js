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
    const status = err.response ? err.response.status : 'no-response'
    console.error(`[predict] call failed (status: ${status}):`, err.message)
    return `Maaf terjadi kesalahan sistem`
  }
}
