/*
* State associated with weather model
*/
import Weather from '@/store/models/weather'

import ThirdPartyService from '@/services/ThirdPartyService'

const state = {

}

const mutations = {

}

const getters = {

}

/*
 * Each action will utilise the event service to perform CRUD requests.
 * The state will then be updated according to what is returned
 */
const actions = {
  async getWeather (context, payload) {
    const [data, error] = await ThirdPartyService.getWeather(payload.eventId, payload.lat, payload.long, payload.weatherDate)
    if (data) {
      return Weather.insert({ data: data })
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
