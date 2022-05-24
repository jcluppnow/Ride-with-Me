<template>
  <div class="text-gray-600 font-semibold w-full max-h-full sm:w-2/3 sm:pr-4 ">
    <p>
      Participant list
    </p>
    <div
      v-for="(participant, i) in event.participants"
      :key="i"
    >
      {{ participant.full_name }}
    </div>
    <div v-if="event.participants.length === 0">
      No participants found
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventModalParticipantsDetails',
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}
</script>
