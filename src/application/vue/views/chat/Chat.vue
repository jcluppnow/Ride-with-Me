<template>
  <div>
    <div
      v-if="events.length"
      class="flex flex-row space-x-6 mx-6"
    >
      <ChatList
        :events="events"
        @select="selectEvent"
        :selected-event="selectedEvent"
      />
      <Messages :event="selectedEvent" />
      <ParticipantList :event="selectedEvent" />
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
import ChatList from '@/components/chat/ChatList'
import Messages from '@/components/chat/Messages'
import ParticipantList from '@/components/chat/ParticipantList'
import User from '@/store/models/user'
import Event from '@/store/models/event'
import ChatMessage from '@/store/models/chat_message'

export default {
  name: 'Chat',
  components: {
    ChatList,
    Messages,
    ParticipantList
  },
  data () {
    return {
      selectedEventId: null
    }
  },
  mounted () {
    // If there is an event ID hash in the url, then open the chat
    if (this.$route.hash) {
      const eventId = this.$route.hash.substring(1)
      if (eventId) {
        this.selectedEventId = eventId
      }
    }
  },
  computed: {
    debugUserModel () {
      return User
    },
    debugChatModel () {
      return ChatMessage
    },
    selectedEvent () {
      if (this.selectedEventId) {
        return Event.query().with(['organiser', 'participants']).find(this.selectedEventId)
      }
      return Event.getters('myEvents')(['organiser', 'participants'])[0]
    },
    events () {
      return Event.getters('myEvents')(['organiser', 'participants'])
    }
  },
  methods: {
    selectEvent (eventId) {
      this.selectedEventId = eventId
      this.$router.replace({ name: 'Chat', hash: `#${eventId}` })
    }
  }
}
</script>
