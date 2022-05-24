/*
 * State associated with user model
 */
import Event from '@/store/models/event'
import UserService from '@/services/UserService'
import LocationService from '@/services/LocationService'

const state = {
  authenticatedUser: null,
  location: null,
  hasShownDistanceAlert: false
}

const mutations = {
  setAuthenticatedUser (state, user) {
    state.authenticatedUser = user
  },
  setLocation (state, location) {
    state.location = location
  },
  setHasShownDistanceAlert (state, hasShownDistanceAlert) {
    state.hasShownDistanceAlert = hasShownDistanceAlert
  }
}

const getters = {
  isAuthenticated: (state) => {
    return state.authenticatedUser !== null
  },
  authenticatedUser: (state) => {
    return state.authenticatedUser
  },
  isOrganiserFor: (state, getters) => (eventId) => {
    if (getters.isAuthenticated) {
      return Event.find(eventId).organiser_id === state.authenticatedUser.id
    }
    return false
  },
  getLocation: (state) => {
    return state.location
  },
  getHasShownDistanceAlert: (state) => {
    return state.hasShownDistanceAlert
  }
}

/*
 * Each action will utilise the user service to perform CRUD requests.
 * The state will then be updated according to what is returned
 */
const actions = {
  async fetchAuthenticatedUser (context, payload) {
    const [data, error] = await UserService.getProfile()
    if (data) {
      context.commit('setAuthenticatedUser', data)
    } else {
      console.log('error occurred', error)
      context.commit('setAuthenticatedUser', null)
    }
  },
  async updateUserDetails (context, { full_name: fullName, email }) {
    const [data, error] = await UserService.updateProfile({ full_name: fullName, email })
    if (data) {
      context.commit('setAuthenticatedUser', data)
    } else {
      throw error
    }
  },
  async updateProfilePhoto (context, formData) {
    // update requires all fields, however we just want to update the profile picture
    formData.append('email', context.state.authenticatedUser.email)
    formData.append('full_name', context.state.authenticatedUser.full_name)

    const [data, error] = await UserService.updateProfile(formData)
    if (data) {
      context.commit('setAuthenticatedUser', data)
    } else {
      throw error
    }
  },
  async broadcastLocation (context, payload) {
    const [data, error] = await LocationService.sendLocation(payload)

    if (data) {
      return data
    } else {
      throw error
    }
  },
  setLocation (context, payload) {
    context.commit('setLocation', payload)
  },
  setHasShownDistanceAlert (context, payload) {
    context.commit('setHasShownDistanceAlert', payload)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
