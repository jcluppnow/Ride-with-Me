<template>
  <div>
    <div
      v-if="events.length"
      class="mx-2"
    >
      <ChatList
        :events="events"
      />
    </div>
    <div
      v-else
      class="font-semibold ml-3 text-center"
    >
      You are not attending any events, you can attend an event by clicking on an event and clicking attend.
    </div>
  </div>
</template>

<script>
import ChatList from '@/components/chat/mobile/ChatList'
import Event from '@/store/models/event'

export default {
  name: 'Chat',
  components: {
    ChatList
  },
  computed: {
    events () {
      return Event.getters('myEvents')(['organiser', 'participants'])
    }
  }
}
</script>
