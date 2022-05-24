<template>
  <div class="">
    <div class="flex flex-col h-screen">
      <span
        class="flex justify-between mt-12 font-semibold py-2 mx-2"
      >
        <button
          type="button"
          @click.prevent="$router.go(-1)"
        >
          <svg-vue
            icon="chat/back-icon"
            class="h-7 w-7 text-black"
          />
        </button>
        {{ event.name }}
        <button
          type="button"
          @click.prevent="$emit('showParticipants')"
        >
          <svg-vue
            icon="event/participants-icon"
            class="h-7 w-7 text-black"
          />
        </button>
      </span>
      <MessageFrame :event="event" />
    </div>
  </div>
</template>

<script>

import MessageFrame from '../MessageFrame.vue'

export default {
  name: 'Messages',
  components: {
    MessageFrame
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}

</script>
