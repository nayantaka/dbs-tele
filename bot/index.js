const { WhatsappBot } = require('./whatsapp')
const { TelegramBot } = require('./telegram')

process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Rejection:', reason)
})

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err)
})

;(async () => {
  // Jalankan kedua bot secara bersamaan agar satu tidak memblokir yang lain
  const results = await Promise.allSettled([WhatsappBot(), TelegramBot()])
  for (const result of results) {
    if (result.status === 'rejected') {
      console.error(result.reason)
    }
  }
})()