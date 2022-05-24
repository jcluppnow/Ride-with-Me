import Vue from 'vue'
import VueMobileDetection from 'vue-mobile-detection'
import 'animate.css'
import App from '@/App.vue'
import Swal from 'sweetalert2'
import router from '@/router/router'
import store from '@/store/store'
import AxiosService from '@/services/AxiosService'
import User from '@/store/models/user'
import Event from '@/store/models/event'
import Participates from '@/store/models/participates'
import NotificationModel from '@/store/models/notification'
import ChatMessage from '@/store/models/chat_message'
import AppTextInput from '@/components/app/AppTextInput'
import AppTextAreaInput from '@/components/app/AppTextAreaInput'
import AppFileInput from '@/components/app/AppFileInput'
import WebSocketService from '@/services/WebSocketService'
import './websocket/web_socket_bootstrap'
import SvgVue from 'svg-vue'

window.socketClient = WebSocketService

// Initialise axios csrf
AxiosService.bootstrap()

window.swal = Swal

// Make axios globally available for vue
window.axios = AxiosService.axiosClient

router.beforeEach((to, from, next) => {
  if (!User.getters('isAuthenticated')) {
    if (to.name === null) {
      next()
    } else {
      if (to.name !== 'Dashboard') {
        window.location.href = '/accounts/login/'
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

// Mixin to allow detection of mobile user agent
Vue.use(VueMobileDetection)

Vue.component('AppTextInput', AppTextInput)
Vue.component('AppTextAreaInput', AppTextAreaInput)
Vue.component('AppFileInput', AppFileInput)

Vue.use(SvgVue)

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  render: h => h(App),
  store,
  router,
  mounted () {
    this.registerSw()
  },
  methods: {
    async registerSw () {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').then((reg) => {
          console.log('Service worker registered', reg)
        }).catch((error) => {
          console.log('failed to register', error)
        })
      }
    }
  },
  created () {
    User.dispatch('fetchAuthenticatedUser')
      .then(async () => {
        if (User.getters('isAuthenticated')) {
          // Fetch events
          await Participates.deleteAll()
          await Event.deleteAll()
          User.dispatch('setLocation', null)
          Event.dispatch('fetchAttendingEvents')
          Event.dispatch('fetchOrganisingEvents')
          NotificationModel.dispatch('getNotifications')
          ChatMessage.dispatch('getMessages')
          WebSocketService.connect()

          if (window.Cypress) {
            window.appReady = true
          }

          if (Event.getters('getCurrentEvent')) {
            const { event: [currentEvent] } = await Event.dispatch('getEventDetails', Event.getters('getCurrentEvent'))

            if (currentEvent && currentEvent.finished) {
              Event.dispatch('removeCurrentEvent')
            } else if (currentEvent && currentEvent.started) {
            // If organiser, ask to finish event, if event not finished, ask to enable tracking again
              if (currentEvent.organiser_id === User.getters('authenticatedUser').id) {
                window.swal.fire({
                  title: `Has ${currentEvent.name} finished?`,
                  text: 'This will mark the event as finished.',
                  icon: 'warning',
                  showDenyButton: true,
                  confirmButtonText: 'Yes',
                  denyButtonText: 'No.'
                }).then((result) => {
                  if (result.isConfirmed) {
                    Event.dispatch('finishEvent', currentEvent.event_id)
                  } else {
                    store.dispatch('map/watchLocation', {
                      callback (latitude, longitude) {
                        User.dispatch('broadcastLocation', { latitude, longitude, event_id: currentEvent.event_id })
                        User.dispatch('setLocation', { latitude, longitude })
                      },
                      swalConfig: {
                        title: 'Would you like to re-enable location tracking?',
                        icon: 'question',
                        showDenyButton: true,
                        confirmButtonText: 'Yes',
                        denyButtonText: 'No.'
                      }
                    })
                  }
                })
              } else {
                window.swal.fire({
                  title: 'Have you finished this event?',
                  text: 'Would you like to stop participating in this event?',
                  icon: 'warning',
                  showDenyButton: true,
                  confirmButtonText: 'Yes',
                  denyButtonText: 'No.'
                }).then((result) => {
                  if (result.isConfirmed) {
                    Event.dispatch('removeCurrentEvent')
                  } else {
                    store.dispatch('map/watchLocation', {
                      callback (latitude, longitude) {
                        User.dispatch('setLocation', { latitude, longitude })
                      },
                      swalConfig: {
                        title: 'Track location?',
                        text: 'Would you like to view your location on the map?',
                        icon: 'success',
                        confirmButtonText: 'Okay',
                        showCancelButton: true,
                        showCloseButton: true
                      }
                    })
                  }
                })
              }
            }
          }
        }
      })
      .catch(console.error)
  }
})

if (window.Cypress) {
  // only available during E2E tests
  window.app = app
  window.disableDebounce = true
}
