<template>
  <div class="px-2 sm:px-10 w-full">
    <div class="sm:w-2/3 mx-auto h-screen mt-12 sm:mt-10">
      <div class="flex justify-between font-bold text-2xl text-gray-800">
        Notifications
        <button
          v-if="notifications.length > 0"
          @click.prevent="readAll"
          type="button"
          name="button"
        >
          <small
            class="text-blue-400"
          >
            Clear all
          </small>
        </button>
      </div>
      <div>
        <div
          v-if="notifications.length > 0"
        >
          <NotificationList
            :notifications="notifications"
            class="mt-2"
          />
        </div>
        <div
          v-else
          class="font-semibold text-center"
        >
          No Notifications.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NotificationModel from '@/store/models/notification'
import NotificationList from '@/components/notification/NotificationList'

export default {
  name: 'Notifications',
  components: {
    NotificationList
  },
  computed: {
    notifications () {
      return NotificationModel.query().with(['notifier', 'event']).all()
    },
    debugNotificationModel () {
      return NotificationModel
    }
  },
  methods: {
    readAll () {
      NotificationModel.dispatch('readAll')
    }
  }
}
</script>
