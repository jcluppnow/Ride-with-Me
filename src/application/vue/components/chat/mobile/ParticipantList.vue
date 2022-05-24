<template>
  <div
    class="z-40 bg-gray-100 w-60 py-4 fixed inset-y-0 right-0 bottom-0 shadow-lg"
  >
    <!-- Participant List -->
    <div class="h-screen overflow-y-auto scrollbar px-1">
      <div class="flex justify-between text-gray-800 py-2 mt-7">
        Organiser
        <button
          type="button"
          @click.prevent="$emit('close')"
        >
          <svg-vue

            icon="event/close-icon"
            class="h-6 w-6 text-black"
          />
        </button>
      </div>
      <Participant
        cy="organiser"
        :participant="organiser"
      />
      <div class="mt-4">
        Participants
      </div>
      <div>
        <div
          v-if="participants.length > 0"
          class="space-y-3 h-full"
        >
          <Participant
            v-for="(participant, i) in participants"
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

import Participant from '../Participant.vue'
import User from '@/store/models/user'

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
  },
  computed: {
    organiser () {
      return User.find(this.event.organiser_id)
    },
    participants () {
      if (this.event) {
        return User.query()
          .with('events', (query) => query.where('event_id', this.event.event_id))
          .where((user) => user.id !== this.event.organiser_id)
          .has('events', '>', 0).get()
      }
      return []
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
