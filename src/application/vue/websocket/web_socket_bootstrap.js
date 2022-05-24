import WebSocketService from '@/services/WebSocketService'
import Event from '@/store/models/event'
import Participates from '@/store/models/participates'
import ChatMessage from '@/store/models/chat_message'
import User from '@/store/models/user'
import NotificationModel from '@/store/models/notification'
import router from '@/router/router'
import store from '@/store/store'
import helpers from '@/helpers'

WebSocketService.events.onOpen((e) => {
  console.log('on open')
})

WebSocketService.events.onClose((e) => {
  // Reset the websocket connection on close
  setTimeout(() => {
    WebSocketService.connect()
  }, 1000)
})

// this.chatSocket.onsocket_error = (data) => {
//   console.log(data)
// }

WebSocketService.events.onNewParticipant((data) => {
  Event.insertOrUpdate({ data })
})

WebSocketService.events.onParticipantLeave((data) => {
  Participates.delete([data.event_id, data.user_id])
})

WebSocketService.events.onChatMessage((data) => {
  ChatMessage.insert({ data })
})

WebSocketService.events.onSocketError((data) => {
  console.log('socket error', data)
})

WebSocketService.events.onEventStart(async (data) => {
  const { event: [event] } = await Event.update({ data: data })
  if (event.checked_in) {
    window.swal.fire({
      title: `${event.name} started!`,
      text: 'Would you like to view it on the map?',
      icon: 'success',
      confirmButtonText: 'Okay',
      showCancelButton: true,
      showCloseButton: true
    }).then((result) => {
      if (result.isConfirmed) {
        if (router.app.$route.fullPath !== `/#${event.event_id}`) {
          router.push({ name: 'Dashboard', hash: `#${event.event_id}` })
        }
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
})

WebSocketService.events.onEventFinish(async (data) => {
  const { event: [event] } = await Event.update({ data: data })

  if (event.event_id === Event.getters('getCurrentEvent')) {
    window.swal.fire({
      title: `${event.name} finished!`,
      text: 'The organiser has finished the event.',
      icon: 'success',
      confirmButtonText: 'Okay'
    })

    Event.dispatch('setOrganiserLocation', null)
    Event.dispatch('removeCurrentEvent')
  }
})

WebSocketService.events.onOrganiserLocation((data) => {
  const { latitude: organiserLat, longitude: organiserLong, event_id: eventId } = data

  if (eventId === Event.getters('getCurrentEvent')) {
    Event.dispatch('setOrganiserLocation', { latitude: organiserLat, longitude: organiserLong })
  }
})

WebSocketService.events.onOrganiserLocation((data) => {
  const { latitude: organiserLat, longitude: organiserLong, event_id: eventId } = data

  if (eventId === Event.getters('getCurrentEvent')) {
    if (User.getters('getLocation')) {
      const { latitude: lat, longitude: long } = User.getters('getLocation')

      // Calculate distance between the user and the organiser
      const distance = helpers.haversineDistance(lat, long, organiserLat, organiserLong)

      if (distance >= 200.0) {
        const hasShownDistanceAlert = User.getters('getHasShownDistanceAlert')
        if (!hasShownDistanceAlert) {
          User.dispatch('setHasShownDistanceAlert', true)

          if (!('Notification' in window) || Notification.permission !== 'granted') {
            // Show SweetAlert
            window.swal.fire({
              title: 'Distance Warning',
              text: 'You are too far from the event organiser.',
              icon: 'warning',
              confirmButtonText: 'close'
            })
          }

          // Notify organiser
          NotificationModel.dispatch('sendDistanceAlert', eventId)
        }
      }
    } else {
      User.dispatch('setHasShownDistanceAlert', false)
    }
  }
})

WebSocketService.events.onNotification((data) => {
  const { notification } = data
  NotificationModel.insert({ data: notification })
})

WebSocketService.events.onDistanceAlert((data) => {
  const { notification } = data
  NotificationModel.insert({ data: notification })

  // Show SweetAlert
  window.swal.fire({
    title: 'Distance Warning',
    text: notification.content,
    icon: 'warning',
    confirmButtonText: 'close'
  })
})
