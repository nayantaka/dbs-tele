require('dotenv').config()
const getResponse = require('./response')
const {
  default: makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  Browsers,
  fetchLatestBaileysVersion,
  isJidGroup,
  getContentType
} = require('@whiskeysockets/baileys')

const WhatsappBot = async () => {
  try {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info')
    const { version, isLatest } = await fetchLatestBaileysVersion()
    console.log('using WhatsApp version', version.join('.'), '| is latest:', isLatest)

    const sock = makeWASocket({
      auth: state,
      printQRInTerminal: true,
      browser: Browsers.macOS('Smart FAQ'),
      version
    })

    sock.ev.on('creds.update', saveCreds)

    sock.ev.on('connection.update', (update) => {
      const { connection, lastDisconnect } = update
      if (connection === 'close') {
        const code = lastDisconnect &&
          lastDisconnect.error &&
          lastDisconnect.error.output &&
          lastDisconnect.error.output.statusCode
        console.log('connection closed due to:', code, code ? DisconnectReason[code] : '')
      } else if (connection === 'open') {
        console.log('whatsapp connected successfully')
      }
      console.log('connection status:', connection)
    })

    sock.ev.on('messages.upsert', async ({ messages, type }) => {
      if (type !== 'notify') return

      const message = messages[0]
      if (!message.message || message.key.fromMe) return

      const sender = message.key.remoteJid
      if (sender === 'status@broadcast' || isJidGroup(sender)) return

      // Abaikan pesan yang tidak punya teks yang bisa diolah
      const contentType = getContentType(message.message)
      let text = ''
      if (contentType === 'conversation') {
        text = message.message.conversation
      } else if (contentType === 'extendedTextMessage') {
        text = message.message.extendedTextMessage.text
      }

      if (!text || typeof text !== 'string') return

      const response = await getResponse(text)
      const reply = response && response.response ? response.response : 'Maaf terjadi kesalahan sistem'
      await sock.sendMessage(message.key.remoteJid, { text: reply })
    })
  } catch (err) {
    console.error('WhatsappBot error:', err)
    return err
  }
}

module.exports = {
  WhatsappBot
}