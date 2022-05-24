/*
 * Connects to the back-end using the WebSocketService and AxiosService, returning
 * the response for a given request
 * This contains the API and websocket routes associated with the Chat model
 */
import WebSocketService from './WebSocketService'
import AxiosService from './AxiosService'

export default {
  async sendMessage (message) {
    return await WebSocketService.sendRequest('send_message', message)
  },
  async getMessagesForEvent (eventId, page) {
    return await AxiosService.getRequest(`api/v1/events/${eventId}/chat`, { page })
  },
  async getMessages () {
    return await AxiosService.getRequest('api/v1/events/chat')
  }
}
