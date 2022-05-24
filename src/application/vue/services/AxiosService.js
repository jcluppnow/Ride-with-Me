/*
 * Contains the axios instance for the application and exposes functions to
 * send requests through the axios client
 */
import axios from 'axios'

const axiosClient = axios.create({
  // If defined, use MIX_APP_URL else localhost:8080
  baseURL: process.env.MIX_APP_URL || 'http://localhost:8080',
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: true
})

export default {
  axiosClient,
  bootstrap () {
    // Perform run time initialisation - csrf is only needed for this application
    axiosClient.get('/api/v1/csrf').then((response) => {
      axiosClient.defaults.headers.common['X-CSRFToken'] = response.data.token
    })
  },
  /*
   * Each request function will send the respective request type with
   * the given data attached. An array containing the data or error will
   * be returned.
   * On success, the first element will contain the response data or a default
   * empty object and have null as the second element.
   * If the request fails, the first element will be null and the second
   * element will contain the error
   */
  async getRequest (url, data = {}) {
    try {
      const response = await axiosClient.get(url, {
        params: data
      })
      return [response.data || {}, null]
    } catch (err) {
      return [null, err.response]
    }
  },
  async postRequest (url, data = {}) {
    try {
      const response = await axiosClient.post(url, data)
      return [response.data || {}, null]
    } catch (err) {
      return [null, err.response]
    }
  },
  async deleteRequest (url, data = {}) {
    try {
      const response = await axiosClient.delete(url, data)
      return [response.data || {}, null]
    } catch (err) {
      return [null, err.response]
    }
  },
  async putRequest (url, data = {}) {
    try {
      const response = await axiosClient.put(url, data)
      return [response.data || {}, null]
    } catch (err) {
      return [null, err.response]
    }
  },
  // eslint-disable-next-line
  async patchRequest (url, data = {}) {
    try {
      const response = await axiosClient.patch(url, data)
      return [response.data, null]
    } catch (err) {
      return [null, err.response]
    }
  }
}
