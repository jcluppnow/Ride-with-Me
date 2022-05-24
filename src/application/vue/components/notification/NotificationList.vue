<template>
  <div>
    <div class="overflow-y-auto scrollbar space-y-3">
      <NotificationComponent
        v-for="(notification, i) in notifications"
        :key="i"
        :cy="'notification-' + i"
        :notification="notification"
      />
    </div>
  </div>
</template>

<script>
import NotificationComponent from './Notification'

export default {
  name: 'NotificationList',
  components: {
    NotificationComponent
  },
  props: {
    notifications: {
      required: true,
      type: Array
    }
  }
}
</script>
