<template>
  <div class="w-1/5">
    <div class="h-screen overflow-y-auto scrollbar pr-1">
      <!-- Last Chats Title -->
      <div class="font-semibold text-gray-800 py-2 sm:px-2">
        Events
      </div>
      <!-- List chat messages vertically if they exist. -->
      <div class="">
        <div class="space-y-5 h-full">
          <EventChat
            v-for="(event, i) in events"
            :key="i"
            :cy="'event-' + i"
            :event="event"
            :selected="event.event_id === selectedEvent.event_id"
            @select="$emit('select', event.event_id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventChat from './EventChat'

export default {
  name: 'ChatList',
  components: {
    EventChat
  },
  props: {
    events: {
      required: true,
      type: Array
    },
    selectedEvent: {
      required: true,
      type: Object
    }
  }
}
</script>

<style scoped>

/* width */
.scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 8px;
}

/* Track */
.scrollbar::-webkit-scrollbar-track {
    border-radius: 2px;
}

/* Handle */
.scrollbar::-webkit-scrollbar-thumb {
    background: gray;
    border-radius: 10px;
}

/* Handle on hover */
.scrollbar::-webkit-scrollbar-thumb:hover {
    background: #4F4E4E;
}
</style>
