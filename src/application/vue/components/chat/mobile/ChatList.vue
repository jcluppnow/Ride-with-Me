<template>
  <div>
    <!-- Last Chats Title -->
    <div class="font-semibold mt-12 text-gray-800 py-2">
      Events
    </div>
    <!-- List chat messages vertically if they exist. -->
    <div>
      <div class="space-y-5 h-full">
        <EventChat
          v-for="(event, i) in events"
          :key="i"
          :cy="'event-' + i"
          :event="event"
          @select="$router.push({ name: 'MobileChat', params: { eventId: event.event_id }})"
        />
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
    }
  }
}
</script>
