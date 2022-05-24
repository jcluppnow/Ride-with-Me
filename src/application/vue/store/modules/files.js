/*
 * State associated with uploaded files
 */

const state = {
  imageFile: null,
  routeFile: null
}

const getters = {
}

const mutations = {
  setImageFile (state, imageData) {
    state.imageFile = imageData
  },
  setRouteFile (state, routeData) {
    state.routeFile = routeData
  },
  clearRouteFile (state) {
    state.routeFile = null
  },
  clearImageFile (state) {
    state.imageFile = null
  }
}

const actions = {
  setImageFile (context, payload) {
    context.commit('setImageFile', payload)
  },
  setRouteFile (context, payload) {
    context.commit('setRouteFile', payload)
  },
  clearRouteFile (context, payload) {
    context.commit('clearRouteFile')
  },
  clearImageFile (context, payload) {
    context.commit('clearImageFile')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
