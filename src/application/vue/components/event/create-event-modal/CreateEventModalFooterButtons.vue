<template>
  <div class="flex flex-col my-4 w-full sm:flex-row">
    <button
      class="sm:ml-4 w-full sm:w-1/2 bg-rwmDarkBlue hover:bg-rwmOrange text-sm lg:text-base text-white py-2 mr-2 rounded shadow-lg"
      @click.prevent="$emit('close')"
    >
      Cancel
    </button>

    <button
      cy="updateButton"
      v-if="updatingEventId"
      @click="$emit('updateEvent', updatingEventId)"
      class="sm:mr-4 w-full sm:w-1/2 mt-2 sm:mt-0 bg-rwmDarkBlue hover:bg-rwmOrange text-sm lg:text-base text-white py-2 ml-2 rounded shadow-lg"
    >
      Update
    </button>

    <button
      cy="publishButton"
      v-else
      @click="$emit('publishEvent')"
      class="sm:mr-4 w-full sm:w-1/2 mt-2 sm:mt-0 bg-rwmDarkBlue hover:bg-rwmOrange text-sm lg:text-base text-white py-2 rounded shadow-lg"
    >
      Publish
    </button>
  </div>
</template>

<script>
import Event from '@/store/models/event'

export default {
  computed: {
    updatingEventId () {
      return Event.getters('getNewEvent').event_id
    }
  }
}
</script>
