require('dotenv').config()
const Telegraf = require('telegraf')
const getResponse = require('./response');

const TelegramBot = async () => {
  try {
    const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN)
    bot.on('message', async (ctx) => {
      const response = await getResponse(ctx.message.text)
      ctx.reply(response.response)
    })

    // Start webhook via launch (preffered)
    bot.launch({
      webhook: {
        domain: process.env.TELEGRAM_WEBHOOK_URL,
        port: 4000
      }
    })
  }
  catch (err) {
    return err
  }
}

module.exports = {
  TelegramBot
}
