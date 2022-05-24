/*
 * Connects to the back-end API with the AxiosService and returns the response
 * This contains the API routes associated with users
 */
import AxiosService from './AxiosService'

export default {
  async getProfile () {
    return await AxiosService.getRequest('/api/v1/profile')
  },
  async updateProfile (user) {
    return await AxiosService.putRequest('/api/v1/profile', user)
  },
  async getUserProfile (userId) {
    return await AxiosService.deleteRequest(`api/v1/users/${userId}`)
  }
}
