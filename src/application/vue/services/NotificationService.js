/*
 * Connects to the back-end API with the AxiosService and returns the response
 * This contains the API routes associated with events
 */
import AxiosService from './AxiosService'
import WebSocketService from './WebSocketService'

export default {
  async getNotifications (event) {
    return await AxiosService.getRequest('api/v1/notifications')
  },
  async readNotification (notificationId) {
    return await AxiosService.deleteRequest(`api/v1/notifications/${notificationId}`)
  },
  async readAll () {
    return await AxiosService.deleteRequest('api/v1/notifications')
  },
  async registerPushNotification (statusType, subscription, browser) {
    return await AxiosService.postRequest('webpush/save_information', {
      status_type: statusType,
      subscription,
      browser
    })
  },
  async sendDistanceAlert (eventId) {
    return await WebSocketService.sendRequest('send_participant_alert', { event_id: eventId })
  }
}
