/*
 * Connects to the back-end using the WebSocketService and AxiosService, returning
 * the response for a given request
 * This contains the API and websocket routes associated with the Chat model
 */
import WebSocketService from './WebSocketService'

export default {
  async sendLocation (location) {
    console.log(location)
    return await WebSocketService.sendRequest('send_location', location)
  }
}
