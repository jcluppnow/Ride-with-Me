let socketClient = null
const eventCallbacks = {}
// Array of events that can come from the backend and from the websocket itself
const eventTypes = ['onopen', 'onclose', 'oneventstart', 'onsocketerror', 'oneventfinish', 'onorganiserlocation',
  'onchatmessage', 'onconnect', 'ondistancealert', 'onnotification', 'onnewparticipant', 'onparticipantleave']

// initialise an empty array of callbacks for each event
eventTypes.forEach(type => {
  eventCallbacks[type] = []
})

/**
 * Sets up a promise that will resolve when the corresponding
 * response or error is returned from the socket
 */
const sendSocketRequest = (request) => {
  return new Promise((resolve, reject) => {
    // Generate a random request id to use as an event handler
    let requestId = Math.floor((Math.random() * 10000) + 1)

    // ensure that the request id is not already in use
    while (`onresponse${requestId}` in socketClient) {
      requestId = Math.floor((Math.random() * 10000) + 1)
    }

    // add callback for response
    socketClient[`onresponse${requestId}`] = (data) => {
      // remove event handlers for this request
      delete socketClient[`onresponse${requestId}`]
      delete socketClient[`onsocketerror${requestId}`]
      resolve(data)
    }

    // add call back for error
    socketClient[`onsocketerror${requestId}`] = (error) => {
      delete socketClient[`onresponse${requestId}`]
      delete socketClient[`onsocketerror${requestId}`]
      reject(error)
    }

    request.request_id = requestId

    socketClient.send(JSON.stringify(request))
  })
}

/**
 * Set of functions to bind a callback to a specific event
 */
const events = {
  onOpen (callback) {
    eventCallbacks.onopen = [...eventCallbacks.onopen, callback]
    return eventCallbacks.onopen.length - 1
  },
  onClose (callback) {
    eventCallbacks.onclose = [...eventCallbacks.onclose, callback]
    return eventCallbacks.onclose.length - 1
  },
  onConnect (callback) {
    eventCallbacks.onconnect = [...eventCallbacks.onconnect, callback]
    return eventCallbacks.onconnect.length - 1
  },
  onSocketError (callback) {
    eventCallbacks.onsocketerror = [...eventCallbacks.onsocketerror, callback]
    return eventCallbacks.onsocketerror.length - 1
  },
  onEventStart (callback) {
    eventCallbacks.oneventstart = [...eventCallbacks.oneventstart, callback]
    return eventCallbacks.oneventstart.length - 1
  },
  onEventFinish (callback) {
    eventCallbacks.oneventfinish = [...eventCallbacks.oneventfinish, callback]
    return eventCallbacks.oneventfinish.length - 1
  },
  onOrganiserLocation (callback) {
    eventCallbacks.onorganiserlocation = [...eventCallbacks.onorganiserlocation, callback]
    return eventCallbacks.onorganiserlocation.length - 1
  },
  onChatMessage (callback) {
    eventCallbacks.onchatmessage = [...eventCallbacks.onchatmessage, callback]
    return eventCallbacks.onchatmessage.length - 1
  },
  onDistanceAlert (callback) {
    eventCallbacks.ondistancealert = [...eventCallbacks.ondistancealert, callback]
    return eventCallbacks.ondistancealert.length - 1
  },
  onNotification (callback) {
    eventCallbacks.onnotification = [...eventCallbacks.onnotification, callback]
    return eventCallbacks.onnotification.length - 1
  },
  onNewParticipant (callback) {
    eventCallbacks.onnewparticipant = [...eventCallbacks.onnewparticipant, callback]
    return eventCallbacks.onnewparticipant.length - 1
  },
  onParticipantLeave (callback) {
    eventCallbacks.onparticipantleave = [...eventCallbacks.onparticipantleave, callback]
    return eventCallbacks.onparticipantleave.length - 1
  },
  remove (callbackType, index) {
    eventCallbacks[callbackType].splice(index, 1)
  }
}

export default {
  /**
   * Connect websockect and bind event handlers
   */
  connect () {
    if (socketClient !== null && socketClient.readyState !== WebSocket.CLOSED) {
      console.error('connect was called while connected already')
    } else {
      socketClient = new WebSocket(`${process.env.MIX_SOCKET_URL || 'ws://localhost:8080'}/ws/ridewithme`)

      socketClient.onmessage = (ev) => {
        const { event: webSocketEvent, data } = JSON.parse(ev.data)
        if (`on${webSocketEvent}` in socketClient) {
          socketClient[`on${webSocketEvent}`](data)
        } else {
          console.error('No event callback for', webSocketEvent)
        }
      }

      eventTypes.forEach(type => {
        socketClient[type] = (ev) => {
          eventCallbacks[type].forEach(callback => {
            callback(ev)
          })
        }
      })
    }
  },
  events,
  /**
   * Send request to web socket consumer
   */
  async sendRequest (request, data = {}) {
    if (socketClient.readyState === WebSocket.OPEN) {
      try {
        const response = await sendSocketRequest({
          request,
          data
        })
        return [response || {}, null]
      } catch (error) {
        return [null, error]
      }
    } else {
      return new Promise((resolve, reject) => {
        // Add an on open callback that will remove itself
        const callbackIndex = events.onOpen(async (ev) => {
          events.remove('onopen', callbackIndex)

          // Send request that was meant to be sent
          try {
            const response = await sendSocketRequest({
              request,
              data
            })
            resolve([response || {}, null])
          } catch (error) {
            resolve([null, error])
          }
        })
      })
    }
  }
}
