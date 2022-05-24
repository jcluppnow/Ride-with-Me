<template>
  <div
    class="w-1/5"
  >
    <!-- Participant List -->
    <div class="h-screen overflow-y-auto scrollbar pr-1">
      <div class="font-semibold text-gray-800 py-2">
        Organiser
      </div>
      <Participant
        cy="organiser"
        :participant="event.organiser"
      />
      <div class="font-semibold text-gray-800 mt-4 py-2">
        Participants
      </div>
      <div>
        <div
          v-if="event.participants.length > 0"
          class="space-y-3 h-full"
        >
          <Participant
            v-for="(participant, i) in event.participants"
            :key="i"
            :cy="'participant-' + i"
            :participant="participant"
          />
        </div>
        <div
          v-else
          class="font-semibold text-center"
        >
          No Participants.
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import Participant from './Participant.vue'

export default {
  name: 'ParticipantList',
  components: {
    Participant
  },
  props: {
    event: {
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
