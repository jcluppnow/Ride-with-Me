/*
 * State associated with event model
 */
import Event from '@/store/models/event'
import User from '@/store/models/user'
import Participates from '@/store/models/participates'

import EventService from '@/services/EventService'

const state = {
  distance: [0, 300],
  duration: [0, 10],
  speed: [0, 50],
  organiserLocation: null,
  currentEvent: null,
  newEvent: {
    route_coordinates: { type: 'LineString', coordinates: [] },
    starting_location: { type: 'Point', coordinates: [] },
    name: '',
    description: '',
    starting_time: '',
    average_speed: 1,
    max_participants: 1,
    is_private: false
  },
  errors: {}
}

const mutations = {
  setDistance (state, distance) {
    state.distance = distance
  },
  setDuration (state, duration) {
    state.duration = duration
  },
  setSpeed (state, speed) {
    state.speed = speed
  },
  setOrganiserLocation (state, location) {
    state.organiserLocation = location
  },
  removeCurrentEvent (state) {
    state.currentEvent = null
  },
  setCurrentEvent (state, eventId) {
    state.currentEvent = eventId
  },
  addNewRouteCoordinates (state, coordinates) {
    state.newEvent.route_coordinates.coordinates = [...state.newEvent.route_coordinates.coordinates, coordinates]
  },
  insertNewRouteCoordinates (state, payload) {
    state.newEvent.route_coordinates.coordinates.splice(payload.index, 0, payload.coordinates)
  },
  removeFromNewRouteCoordinates (state, index) {
    state.newEvent.route_coordinates.coordinates.splice(index, 1)
  },
  updateNewEvent (state, details) {
    for (const key in details) {
      state.newEvent[key] = details[key]
    }
  },
  setNewEvent (state, event) {
    state.newEvent = event
  },
  resetNewEvent (state) {
    state.newEvent = {
      route_coordinates: { type: 'LineString', coordinates: [] },
      starting_location: { type: 'Point', coordinates: [] },
      name: '',
      description: '',
      starting_time: '',
      average_speed: 1,
      max_participants: 1,
      is_private: false
    }
  },
  resetErrors (state) {
    state.errors = {}
  },
  removeError (state, field) {
    delete state.errors[field]
  },
  setErrors (state, errors) {
    state.errors = errors
  },
  addError (state, payload) {
    console.log(payload)
    state.errors[payload.field] ? state.errors[payload.field].push(payload.value) : state.errors[payload.field] = [payload.value]
  }
}

const getters = {
  getSpeed: (state) => {
    return state.speed
  },
  getDuration: (state) => {
    return state.duration
  },
  getDistance: (state) => {
    return state.distance
  },
  organiserLocation: (state) => {
    return state.organiserLocation
  },
  nearbyEvents: (state) => (relationships = [], excludes = []) => {
    return Event.query().where('attending', false).where(event => !excludes.includes(event.event_id)).with(relationships).get()
  },
  myEvents: (state) => (relationships = []) => {
    const user = User.getters('authenticatedUser')
    if (user) {
      return Event.query().orWhere('organiser_id', user.id).where('attending', true).orWhere('checked_in', true).with(relationships).get()
    }
    return []
  },
  attendingEvents: (state) => (relationships = []) => {
    const user = User.getters('authenticatedUser')
    if (user) {
      return Event.query().where('organiser_id', (value) => value !== user.id).where('attending', true).orWhere('checked_in', true).with(relationships).get()
    }
    return []
  },
  organisingEvents: (state) => (relationships = []) => {
    const user = User.getters('authenticatedUser')
    if (user) {
      return Event.query().where('organiser_id', user.id).with(relationships).get()
    }
    return []
  },
  getCurrentEvent: (state) => {
    return state.currentEvent
  },
  getNewEvent: (state) => {
    return state.newEvent
  },
  getErrors: (state) => {
    return state.errors
  }
}

/*
 * Each action will utilise the event service to perform CRUD requests.
 * The state will then be updated according to what is returned
 */
const actions = {
  setDistance (context, payload) {
    context.commit('setDistance', payload)
  },
  setDuration (context, payload) {
    context.commit('setDuration', payload)
  },
  setSpeed (context, payload) {
    context.commit('setSpeed', payload)
  },
  async createEvent (context, payload) {
    const [data, error] = await EventService.createEvent(payload)

    if (data) {
      Event.insertOrUpdate({ data: data })
      return data
    } else {
      // console.log('error occurred', error)
      throw error
    }
  },
  async updateEvent (context, { eventId, event }) {
    const [data, error] = await EventService.updateEvent(eventId, event)

    if (data) {
      Event.update({ where: data.event_id, data: data })
      return data
    } else {
      throw error
    }
  },
  async getNearbyBox (context, payload) {
    const [data, error] = await EventService.getNearbyBox(payload.ne, payload.sw)
    if (data) {
      const normalisedEvents = data.map((event) => {
        return { ...event, organiser_id: event.organiser.id }
      })

      Event.insertOrUpdate({ data: normalisedEvents })
    } else {
      console.log('error occurred', error)
    }
  },
  async getNearbyLocation (context, payload) {
    const [data, error] = await EventService.getNearbyLocation(payload.lat, payload.lon, payload.distance)
    if (data) {
      const normalisedEvents = data.map((event) => {
        return { ...event, organiser_id: event.organiser.id }
      })
      Event.insertOrUpdate({ data: normalisedEvents })
    } else {
      console.log('error occurred', error)
    }
  },
  async getEventDetails (context, payload) {
    const [data, error] = await EventService.getEventDetails(payload)
    if (data) {
      const normalisedEvent = { ...data, organiser_id: data.organiser.id }

      return Event.insertOrUpdate({ data: normalisedEvent })
    } else {
      throw error
    }
  },
  async deleteEvent (context, payload) {
    const [data, error] = await EventService.deleteEvent(payload)
    if (data) {
      Event.delete(payload)
    } else {
      console.log('error occurred', error)
    }
  },
  async startEvent (context, payload) {
    const [data, error] = await EventService.startEvent(payload)
    if (data) {
      Event.update({ where: data.event_id, data: data })
      context.commit('setCurrentEvent', data.event_id)
      return data
    } else {
      throw error
    }
  },
  async finishEvent (context, payload) {
    const [data, error] = await EventService.finishEvent(payload)
    if (data) {
      Event.update({ where: data.event_id, data: data })
      context.commit('removeCurrentEvent')
      return data
    } else {
      console.log('error occurred', error)
    }
  },
  async fetchAttendingEvents () {
    const [data, error] = await EventService.getAttendingEvents()
    if (data) {
      const normalisedEvents = data.map((event) => {
        return { ...event, organiser_id: event.organiser.id }
      })

      Event.insertOrUpdate({ data: normalisedEvents })
    } else {
      console.log('error occurred', error)
    }
  },
  async fetchOrganisingEvents () {
    const [data, error] = await EventService.getOrganisingEvents()
    if (data) {
      const normalisedEvents = data.map((event) => {
        return { ...event, organiser_id: event.organiser.id }
      })

      Event.insertOrUpdate({ data: normalisedEvents })
    } else {
      console.log('error occurred', error)
    }
  },
  async removeNearby (context, payload) {
    Event.delete((event) => event.attending === false && !payload.includes(event.event_id))
  },
  async leaveEvent (context, payload) {
    const [data, error] = await EventService.leaveEvent(payload)
    if (data) {
      EventService.broadcastLeave(data.event_id)
      Participates.delete([data.event_id, User.getters('authenticatedUser').id])
      return Event.insertOrUpdate({ data: data })
    } else {
      console.log('error occurred', error)
    }
  },
  async attendEvent (context, payload) {
    const [data, error] = await EventService.attendEvent(payload)
    if (data) {
      EventService.broadcastAttend(data.event_id)
      return Event.insertOrUpdate({ data: data })
    } else {
      console.log('error occurred', error)
    }
  },
  async checkInEvent (context, payload) {
    const [data, error] = await EventService.checkInEvent(payload)
    if (data) {
      Event.update({ data: data })
      context.commit('setCurrentEvent', data.event_id)
    } else {
      console.log('error occurred', error)
    }
  },
  setOrganiserLocation (context, payload) {
    context.commit('setOrganiserLocation', payload)
  },
  removeCurrentEvent (context, payload) {
    context.commit('removeCurrentEvent')
  },
  addNewRouteCoordinates (context, payload) {
    context.commit('addNewRouteCoordinates', payload)
  },
  insertNewRouteCoordinates (context, payload) {
    context.commit('insertNewRouteCoordinates', { coordinates: payload.coordinates, index: payload.index })
  },
  removeFromNewRouteCoordinates (context, payload) {
    context.commit('removeFromNewRouteCoordinates', payload.index)
  },
  updateNewEvent (context, payload) {
    context.commit('updateNewEvent', payload)
  },
  setNewEvent (context, payload) {
    context.commit('setNewEvent', payload)
  },
  resetNewEvent (context, payload) {
    context.commit('resetNewEvent')
  },
  resetErrors (context, payload) {
    context.commit('resetErrors')
  },
  setErrors (context, payload) {
    context.commit('setErrors', payload)
  },
  addError (context, payload) {
    context.commit('addError', payload)
  },
  removeError (context, payload) {
    context.commit('removeError', payload.field)
  },
  async searchEvents (context, payload) {
    const [data, error] = await EventService.searchEvents(payload)
    if (data) {
      return data
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
