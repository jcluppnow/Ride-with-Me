<template>
  <div class="text-white">
    <div class="flex space-x-4 sm:space-x-3">
      <button
        @click.prevent="$emit('showInfo')"
        class="group block sm:hidden"
      >
        <svg-vue
          icon="event/info-icon"
          class="h-5 w-5 group-hover:text-yellow-500"
        />
      </button>

      <AppHoverTip text="Copy Event Link">
        <button
          @click.prevent="copyLink"
          class="group block"
        >
          <svg-vue
            icon="event/link-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>

      <!-- Edit Icon -->
      <AppHoverTip
        v-if="event.organiser_id === authenticatedUserId && !event.started"
        text="Edit"
      >
        <button
          class="group block"
          @click.prevent="$emit('update')"
          cy="update-event"
        >
          <svg-vue
            icon="event/edit-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>

      <AppHoverTip text="Participants">
        <button
          type="button"
          @click.prevent="$emit('showParticipants')"
          class="group block"
        >
          <!-- Participants Icon -->
          <svg-vue
            icon="event/participants-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>

      <AppHoverTip
        v-if="event.attending"
        text="Chat"
      >
        <button
          class="group block"
          type="button"
          @click.prevent="$router.push({ name: 'Chat', hash: `#${event.event_id}`})"
        >
          <!-- Chat Icon -->
          <svg-vue
            icon="event/chat-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>

      <AppHoverTip
        v-if="event.attending"
        text="Notifications"
      >
        <button
          class="group block"
          @click.prevent="requestNotificationPermission"
        >
          <!-- Notifications Icon -->
          <svg-vue
            icon="event/notifications-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>

      <AppHoverTip
        v-if="event.organiser_id === authenticatedUserId"
        text="Delete"
      >
        <button
          @click.prevent="$emit('delete', event.event_id)"
          class="group block"
        >
          <svg-vue
            icon="event/trash-icon"
            class="h-5 w-5 group-hover:text-yellow-500"
          />
        </button>
      </AppHoverTip>
    </div>
  </div>
</template>

<script>
import User from '@/store/models/user'
import NotificationModel from '@/store/models/notification'
import AppHoverTip from '@/components/app/AppHoverTip'

export default {
  components: {
    AppHoverTip
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  computed: {
    authenticatedUserId () {
      return User.getters('authenticatedUser')?.id
    }
  },
  methods: {
    requestNotificationPermission () {
      NotificationModel.dispatch('requestPushNotification').then(() => {
        window.swal.fire({
          title: 'Subscribed',
          text: 'You will receive push notifications',
          icon: 'success'
        })
      })
    },
    copyLink () {
      navigator.clipboard.writeText(`${process.env.MIX_APP_URL || 'http://localhost:8080'}/events#${this.event.event_id}`)
    }
  }
}
</script>
