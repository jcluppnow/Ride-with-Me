<template>
  <div class="flex justify-between space-x-2 p-1 sm:p-3">
    <div v-if="event.attending && !event.started && checkInAvailable && !event.checked_in">
      <button
        class="px-10 py-2 shadow-lg text-center bg-rwmLighterBlue hover:bg-rwmOrange text-sm text-white rounded"
        @click.prevent="$emit('checkIn', event.event_id)"
      >
        Check In
      </button>
    </div>

    <div v-if="event.attending">
      <button
        class="px-10 py-2 shadow-lg text-center bg-rwmLighterBlue hover:bg-rwmOrange text-sm text-white rounded"
        @click.prevent="$emit('leave', event.event_id)"
      >
        Leave
      </button>
    </div>

    <div v-if="!event.attending && !event.started">
      <button
        class="px-10 py-2 shadow-lg text-center bg-rwmLighterBlue hover:bg-rwmOrange text-sm text-white rounded"
        @click.prevent="$emit('attend', event.event_id)"
      >
        Attend
      </button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'UserEventButtons',
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  computed: {
    checkInAvailable () {
      const today = new Date()
      const startingTime = this.event.startingTimeDate

      return startingTime.getFullYear() === today.getFullYear() &&
                startingTime.getMonth() === today.getMonth() &&
                startingTime.getDate() === today.getDate() &&
                startingTime.getHours() >= (today.getHours() - 1)
    }
  }
}
</script>
