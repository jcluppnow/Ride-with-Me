/*
 * State associated with notifications model
 */
import NotificationService from '@/services/NotificationService'
import NotificationModel from '@/store/models/notification'
import helpers from '@/helpers'

const state = {
}

const mutations = {
}

const getters = {
}

const actions = {
  async getNotifications (context, payload) {
    const [data, error] = await NotificationService.getNotifications()

    if (data) {
      console.log(data)
      NotificationModel.insertOrUpdate({ data: data })
      return data
    } else {
      throw error
    }
  },
  async readNotification (context, payload) {
    const [data, error] = await NotificationService.readNotification(payload)

    if (data) {
      NotificationModel.delete(payload)
      return data
    } else {
      throw error
    }
  },
  async readAll (context, payload) {
    const [data, error] = await NotificationService.readAll()

    if (data) {
      NotificationModel.deleteAll()
      return data
    } else {
      throw error
    }
  },
  async sendDistanceAlert (context, payload) {
    const [data, error] = await NotificationService.sendDistanceAlert(payload)

    if (data) {
      console.log(data)
      NotificationModel.insertOrUpdate({ data: data })
      return data
    } else {
      throw error
    }
  },
  async subscribe (context, payload) {
    const subscription = await payload.pushManager.getSubscription()
    if (subscription) {
      context.dispatch('registerPushNotification', subscription)
      return
    }

    const key = process.env.MIX_VAPID_PUBLIC_KEY
    const options = {
      userVisibleOnly: true,
      // if key exists, create applicationServerKey property
      ...(key && { applicationServerKey: helpers.urlB64ToUint8Array(key) })
    }

    const sub = await payload.pushManager.subscribe(options)
    context.dispatch('registerPushNotification', sub)
  },
  async requestPushNotification (context, payload) {
    if ('serviceWorker' in navigator) {
      const reg = await navigator.serviceWorker.register('/sw.js')
      if (!reg.showNotification) {
        window.swal.fire({
          title: 'Cannot enable push notifications',
          text: 'Notifications are not support.',
          icon: 'error'
        })
        return
      }
      if (Notification.permission === 'denied') {
        window.swal.fire({
          title: 'Cannot enable push notifications',
          text: 'Notifications have been blocked.',
          icon: 'error'
        })
        return
      }
      if (!('PushManager' in window)) {
        window.swal.fire({
          title: 'Cannot enable push notifications',
          text: 'Notifications are not support by your browser.',
          icon: 'error'
        })
        return
      }
      context.dispatch('subscribe', reg)
    } else {
      window.swal.fire({
        title: 'Cannot enable push notifications',
        text: 'Notifications are not support by your browser.',
        icon: 'error'
      })
    }
  },
  async registerPushNotification (context, payload) {
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase()

    const [data, error] = await NotificationService.registerPushNotification('subscribe', payload.toJSON(), browser)

    if (data) {
      return data
    } else {
      throw error
    }
  },
  requestNotificationPermission (context, payload) {
    if ('Notification' in window) {
      if (Notification.permission === 'default') {
        window.swal.fire({
          title: 'Notifications',
          text: 'Would you to enable notifications? Notifications let you receive alerts even when Ride with Me is backgrounded.',
          icon: 'question',
          confirmButtonText: 'Okay',
          showCancelButton: true,
          showCloseButton: true
        }).then((result) => {
          console.log(result)
          if (result.isConfirmed) {
            Notification.requestPermission()
          }
        })
      }
    } else {
      window.swal.fire({
        title: 'Notifications',
        text: 'Push notifications are not support',
        icon: 'error',
        confirmButtonText: 'Okay'
      })
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
