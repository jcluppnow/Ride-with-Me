self.addEventListener('push', (event) => {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  const eventInfo = event.data.text()
  const data = JSON.parse(eventInfo)
  const head = data.head || 'Ride with Me'
  const body = data.body || 'Notification'

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    self.registration.showNotification(head, {
      body: body,
      icon: 'https://i.imgur.com/MZM3K5w.png'
    })
  )
})
