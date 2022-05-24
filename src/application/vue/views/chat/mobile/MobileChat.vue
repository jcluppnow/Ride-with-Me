<template>
  <div>
    <Messages
      v-if="selectedEvent"
      :event="selectedEvent"
      @showParticipants="showParticipants = true"
    />
    <transition
      name="slide-menu"
      enter-active-class="animate__animated animate__slideInRight animate__faster"
      leave-active-class="animate__animated animate__slideOutRight animate__faster"
    >
      <ParticipantList
        v-if="showParticipants"
        :event="selectedEvent"
        @close="showParticipants = false"
      />
    </transition>
    <div
      v-if="showParticipants"
      class="absolute h-screen w-screen bottom-0 left-0 z-10"
      @click.prevent="showParticipants = false"
    />
  </div>
</template>

<script>
import Messages from '@/components/chat/mobile/Messages'
import ParticipantList from '@/components/chat/mobile/ParticipantList'
import Event from '@/store/models/event'

export default {
  name: 'Chat',
  components: {
    Messages,
    ParticipantList
  },
  data () {
    return {
      showParticipants: false
    }
  },
  created () {
    this.selectedEventId = this.$route.params.eventId
  },
  computed: {
    selectedEvent () {
      return Event.find(this.selectedEventId)
    }
  }
}
</script>
