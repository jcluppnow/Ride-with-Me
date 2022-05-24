/*
 * Connects to the back-end API with the AxiosService and returns the response
 * This contains the API routes associated with third party requests.
 */
import AxiosService from './AxiosService'

export default {
  async getWeather (eventId, lat, long, weatherDate) {
    return await AxiosService.postRequest('api/v1/weather', { eventId, lat, long, weatherDate })
  },
  async getTraffic (northEast, southWest) {
    return await AxiosService.getRequest('api/v1/traffic', { ne_lat: northEast[1], ne_long: northEast[0], sw_lat: southWest[1], sw_long: southWest[0] })
  }
}
