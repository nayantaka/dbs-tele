const fs = require('fs')
require('dotenv').config()
const getResponse = require('./response')
const Baileys = require('@adiwajshing/baileys')

const WhatsappBot = async () => {
  try {
    const connection = new Baileys.WAConnection()
    connection.autoReconnect = Baileys.ReconnectMode.onAllErrors
    connection.connectOptions.maxRetries = 5
    connection.chatOrderingKey = Baileys.waChatKey(true)

    connection.on('credentials-updated', () => {
      const authInfo = connection.base64EncodedAuthInfo()
      fs.writeFileSync('./auth_info.json', JSON.stringify(authInfo, null, '\t'))
    })

    fs.existsSync('./auth_info.json') && connection.loadAuthInfo ('./auth_info.json')

    await connection.connect()

    connection.on('open', () => {
      console.log('whatsapp connected successfully')
      console.log(`welcome ${connection.user.name} (${connection.user.jid})`)
    })

    connection.on('close', (err) => {
      console.error(`connection was closed due ${err.reason}. reconnecting status: ${err.isReconnecting}`)
    })

    connection.on('CB:action,,battery', (json) => {
      let batteryLevel = json[2][0][1].value
      batterylevel = parseInt(batteryLevel)
      console.log('battery level: ' + batterylevel)
    })

    connection.on('connection-phone-change', (state) => {
      console.log(`connection was changed. connection status: ${state.connected}`)
    })

    connection.on('message-new', async (message) => {
      console.log(`new message received`)
      const messageStubType = Baileys.WA_MESSAGE_STUB_TYPES[message.messageStubType] ?
        Baileys.WA_MESSAGE_STUB_TYPES[message.messageStubType] : 'MESSAGE'

      const messageContent = message.message

      if (!messageContent) return

      if (message.key.fromMe) {
        console.log(`relayed my own message`)
        return
      }

      let sender = message.key.remoteJid

      if (sender == 'status@broadcast') return
      if (sender.includes('@g.us')) return

      const messageType = Object.keys(messageContent)[0]
      let text

      if (messageType == Baileys.MessageType.text) {
        text = message.message.conversation
      }
      else if (messageType == Baileys.MessageType.extendedText) {
        text = message.message.extendedTextMessage.text
        const quotedText = message.message
      }

      const response = await getResponse(text)
      await sendMessage(message, response.response)
    })

    const sendMessage = async (message, content) => {
      await connection.chatRead(message.key.remoteJid)
      await connection.updatePresence(message.key.remoteJid, Baileys.Presence.available)
      await connection.updatePresence(message.key.remoteJid, Baileys.Presence.composing)
      await connection.sendMessage(message.key.remoteJid, content, Baileys.MessageType.text)
    }
  }
  catch (err) {
    return err
  }
}

module.exports = {
  WhatsappBot
}
