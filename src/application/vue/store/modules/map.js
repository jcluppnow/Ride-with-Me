/*
 * State associated with mapworks
 */
import User from '@/store/models/user'

function getUserLocation (callback, errorCallback) {
  // Create an position options object for custom settings.
  const options = {
    // Attempt to provide a high accuracy location.
    // Can result in slower times and increased power consumption.
    enableHighAccuracy: true,

    // Timeout before the error callback is invoked.
    timeout: 10000,

    // Maximum cached position age.
    maximumAge: 0
  }

  // Get the current position of the device.
  // Accepts 3 paramaters.
  // 1. Callback for a function to run on success.
  // 2. Callback for a function to run on error.
  // 3. Options to customize location check.
  navigator.geolocation.getCurrentPosition((position) => {
    const { coords: { latitude, longitude } } = position
    callback(latitude, longitude)
  }, (error) => {
    // Handle error code and output the error.
    switch (error.code) {
    case error.PERMISSION_DENIED:
      console.log('User denied the request for Geolocation.')
      break
    case error.POSITION_UNAVAILABLE:
      console.log('Location information is unavailable.')
      break
    case error.TIMEOUT:
      console.log('The request to get user location timed out.')
      break
    case error.UNKNOWN_ERROR:
      console.log('An unknown error occurred.')
      break
    }

    window.swal.fire({
      title: 'Could not get your location!',
      text: 'Please enable location permissions and try again.',
      icon: 'error',
      confirmButtonText: 'Okay'
    })

    if (errorCallback) {
      errorCallback(error)
    }
  }, options)
}

function watchUserLocation (callback, errorCallback) {
  // Create an position options object for custom settings.
  const options = {
    // Attempt to provide a high accuracy location.
    // Can result in slower times and increased power consumption.
    enableHighAccuracy: true,

    // Timeout before the error callback is invoked.
    timeout: 10000,

    // Maximum cached position age.
    maximumAge: 0
  }

  // Get the current position of the device.
  // Accepts 3 parameters.
  // 1. Callback for a function to run on success.
  // 2. Callback for a function to run on error.
  // 3. Options to customize location check.
  return navigator.geolocation.watchPosition((position) => {
    const { coords: { latitude, longitude } } = position
    callback(latitude, longitude)
  }, (error) => {
    // Handle error code and output the error.
    switch (error.code) {
    case error.PERMISSION_DENIED:
      console.log('User denied the request for Geolocation.')
      break
    case error.POSITION_UNAVAILABLE:
      console.log('Location information is unavailable.')
      break
    case error.TIMEOUT:
      console.log('The request to get user location timed out.')
      break
    case error.UNKNOWN_ERROR:
      console.log('An unknown error occurred.')
      break
    }

    window.swal.fire({
      title: 'Could not get your location!',
      text: 'Please enable location permissions and try again.',
      icon: 'error',
      confirmButtonText: 'Okay'
    })

    if (errorCallback) {
      errorCallback(error)
    }
  }, options)
}

const state = {
  mapEmbed: null,
  watcherId: null
}

const getters = {
  getMapEmbed: (state) => {
    return state.mapEmbed
  },
  watcherId: (state) => {
    return state.watcherId
  }
}

const mutations = {
  setMapEmbed (state, inMapEmbed) {
    state.mapEmbed = inMapEmbed
  },
  clearWatcher (state) {
    if (state.watcherId) {
      navigator.geolocation.clearWatch(state.watcherId)
    }
  },
  setWatcherId (state, watcherId) {
    state.watcherId = watcherId
  }
}

const actions = {
  clearWatcher (context) {
    context.commit('clearWatcher')
  },
  async watchLocation (context, payload) {
    if (navigator.geolocation) {
      let watcherId = 0
      const permission = await navigator.permissions.query({ name: 'geolocation' })
      const watcher = context.getters.watcherId
      const location = User.getters('getLocation')

      if (watcher && location) {
        payload.callback(location.latitude, location.longitude)
      } else if (permission.state !== 'granted') {
        window.swal.fire(payload.swalConfig).then((result) => {
          if (result.isConfirmed) {
            watcherId = watchUserLocation(payload.callback, payload.error)
          }
        })
      } else {
        watcherId = watchUserLocation(payload.callback, payload.error)
      }

      context.commit('setWatcherId', watcherId)
    }
  },
  async getLocation (context, payload) {
    if (navigator.geolocation) {
      const permission = await navigator.permissions.query({ name: 'geolocation' })
      const watcher = context.getters.watcherId
      const location = User.getters('getLocation')

      if (watcher && location) {
        payload.callback(location.latitude, location.longitude)
      } else if (permission.state !== 'granted') {
        window.swal.fire(payload.swalConfig).then((result) => {
          if (result.isConfirmed) {
            getUserLocation(payload.callback, payload.error)
          }
        })
      } else {
        getUserLocation(payload.callback, payload.error)
      }
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
