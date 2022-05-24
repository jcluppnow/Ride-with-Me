/*
 * Connects to the back-end API with the AxiosService and returns the response
 * This contains the API routes associated with events
 */
import AxiosService from './AxiosService'
import WebSocketService from './WebSocketService'

export default {
  async createEvent (event) {
    return await AxiosService.postRequest('api/v1/events/', event)
  },
  async getAttendingEvents () {
    return await AxiosService.getRequest('api/v1/events/attending')
  },
  async getOrganisingEvents () {
    return await AxiosService.getRequest('api/v1/events/organising')
  },
  async getNearbyBox (northEast, southWest) {
    return await AxiosService.getRequest('api/v1/events/nearby', { ne_lat: northEast[1], ne_long: northEast[0], sw_lat: southWest[1], sw_long: southWest[0] })
  },
  async getNearbyLocation (lat, long, distance = 50000) {
    return await AxiosService.getRequest('api/v1/events/nearby', { lat, long, distance })
  },
  async searchEvents (query) {
    return await AxiosService.getRequest('api/v1/events/search', { search_text: query })
  },
  async getEventDetails (eventId) {
    return await AxiosService.getRequest(`api/v1/events/${eventId}`)
  },
  async getEventGpx (eventId) {
    return await AxiosService.postRequest(`api/v1/events/${eventId}.gpx`)
  },
  async updateEvent (eventId, event) {
    return await AxiosService.putRequest(`api/v1/events/${eventId}/`, event)
  },
  async startEvent (eventId) {
    return await AxiosService.postRequest(`api/v1/events/${eventId}/start`)
  },
  async finishEvent (eventId) {
    return await AxiosService.postRequest(`api/v1/events/${eventId}/finish`)
  },
  async deleteEvent (eventId) {
    return await AxiosService.deleteRequest(`api/v1/events/${eventId}/`)
  },
  async attendEvent (eventId) {
    return await AxiosService.postRequest(`api/v1/events/${eventId}/participate`)
  },
  async leaveEvent (eventId) {
    return await AxiosService.deleteRequest(`api/v1/events/${eventId}/participate`)
  },
  async checkInEvent (eventId) {
    return await AxiosService.postRequest(`api/v1/events/${eventId}/check_in`)
  },
  // Websocket requests
  async broadcastAttend (eventId) {
    return await WebSocketService.sendRequest('attend_event', { event_id: eventId })
  },
  async broadcastLeave (eventId) {
    return await WebSocketService.sendRequest('leave_event', { event_id: eventId })
  }
}
