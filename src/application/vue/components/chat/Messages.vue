<template>
  <div class="w-3/5 flex-shrink-0">
    <div class="flex flex-col h-screen">
      <span
        class="font-semibold text-gray-800 py-2"
      >
        {{ event.name }}
      </span>
      <MessageFrame :event="event" />
    </div>
  </div>
</template>

<script>

import MessageFrame from './MessageFrame.vue'

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
