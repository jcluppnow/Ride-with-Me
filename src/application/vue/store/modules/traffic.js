/* State associated with traffic model.
 */
import Traffic from '@/store/models/traffic'

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
  async getTraffic (context, payload) {
    const [data, error] = await ThirdPartyService.getTraffic(payload.ne, payload.sw)
    if (data) {
      const normalisedTraffic = data.map((traffic) => {
        return { ...traffic, traffic_id: traffic.traffic_id }
      })

      Traffic.insert({ data: normalisedTraffic })
    } else {
      console.log('error occurred', error)
    }
  },
  async removeNearbyTraffic (context, payload) {
    // Delete all traffic data.
    Traffic.delete((traffic) => {
      if (payload.selected_id && (traffic.traffic_id === payload.selected_id)) {
        return false
      }

      return true
    })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
