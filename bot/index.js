(async () => {
  const { WhatsappBot } = require('./whatsapp')
  await WhatsappBot().catch(err => console.log(err))

  const { TelegramBot } = require('./telegram')
  await TelegramBot().catch(err => console.log(err))
})()
