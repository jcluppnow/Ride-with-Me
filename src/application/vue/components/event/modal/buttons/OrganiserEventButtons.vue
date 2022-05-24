<template>
  <div class="flex justify-between space-x-2 p-1 sm:p-3">
    <div
      v-if="event.started && !event.finished"
    >
      <button
        class="px-10 py-2 shadow-lg text-center bg-rwmLighterBlue hover:bg-rwmOrange text-sm text-white rounded"
        @click.prevent="$emit('finish', event.event_id)"
        cy="finish-event"
      >
        Finish
      </button>
    </div>
    <div
      v-if="startAvailable && !event.started"
    >
      <button
        cy="start-event"
        class="px-10 py-2 shadow-lg text-center bg-rwmLighterBlue hover:bg-rwmOrange text-sm text-white rounded"
        @click.prevent="$emit('start', event.event_id)"
      >
        Start
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrganiserEventButtons',
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  computed: {
    startAvailable () {
      const today = new Date()
      const startingTime = this.event.startingTimeDate

      return (startingTime - today) < 60 * 1000 * 30 // 30 minutes
    }
  }
}
</script>
