import ChatService from '@/services/ChatService'
import ChatMessage from '@/store/models/chat_message'

/*
 * State associated with chat_message model
 */
const state = {
}

const mutations = {
}

const getters = {
  messagesForEvent: (state) => (eventId) => {
    return ChatMessage.query().where('event_id', eventId).with('sender').get()
  }
}

const actions = {
  async sendMessage (context, payload) {
    const [data, error] = await ChatService.sendMessage(payload)

    if (data) {
      ChatMessage.insert({ data: data })
      return data
    } else {
      throw error
    }
  },
  async getMessagesForEvent (context, payload) {
    const [data, error] = await ChatService.getMessagesForEvent(payload.eventId, payload.page)
    if (data) {
      return ChatMessage.insert({ data: data.results })
    } else {
      throw error
    }
  },
  async getMessages (context, payload) {
    const [data, error] = await ChatService.getMessages()
    if (data) {
      const messages = data.map((event) => {
        return event.messages
      })
      ChatMessage.insert({ data: messages.flat() })
    } else {
      console.log('error occurred', error)
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
