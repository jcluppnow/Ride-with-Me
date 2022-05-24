<template>
  <div>
    <!-- Guest user -->
    <div
      v-if="!authenticated"
      :key="'not-authenticated'"
      class="w-full"
    >
      <UnauthenticatedEventButtons
        :event="event"
        @close="$emit('close')"
      />
    </div>

    <!-- User is organiser -->
    <div
      v-else-if="isOrganiser"
      :key="'organiser'"
      class="w-full"
    >
      <OrganiserEventButtons
        :event="event"
        @start="$emit('start', event.event_id)"
        @finish="$emit('finish', event.event_id)"
      />
    </div>

    <!-- User is authenticated -->
    <div
      v-else
      :key="'not-attending'"
      class="w-full"
    >
      <UserEventButtons
        :event="event"
        @close="$emit('close')"
        @leave="$emit('leave', event.event_id)"
        @checkIn="$emit('checkIn', event.event_id)"
        @attend="$emit('attend', event.event_id)"
      />
    </div>
  </div>
</template>

<script>
import User from '@/store/models/user'
import UnauthenticatedEventButtons from './buttons/UnauthenticatedEventButtons'
import OrganiserEventButtons from './buttons/OrganiserEventButtons'
import UserEventButtons from './buttons/UserEventButtons'

export default {
  name: 'EventModalButtons',
  components: {
    UnauthenticatedEventButtons,
    OrganiserEventButtons,
    UserEventButtons
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  computed: {
    checkInAvailable () {
      return this.event.startingTimeDate.toLocaleString('en-US', { hour: 'numeric', hour12: true })
    },
    startAvailable () {
      const today = new Date()
      const startingTime = this.event.startingTimeDate

      return (startingTime - today) < 60 * 1000 * 30 // 30 minutes
    },
    eventIsToday () {
      const today = new Date()
      const startingTime = this.event.startingTimeDate

      return startingTime.getFullYear() === today.getFullYear() &&
                startingTime.getMonth() === today.getMonth() &&
                startingTime.getDate() === today.getDate()
    },
    authenticated () {
      return User.getters('isAuthenticated')
    },
    isOrganiser () {
      return User.getters('isOrganiserFor')(this.event.event_id)
    }
  }
}
</script>
