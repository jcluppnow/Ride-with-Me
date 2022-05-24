<template>
  <div
    class="rounded text-black-900 overflow-hidden shadow-lg bg-white"
  >
    <div
      class="flex flex-row p-2 items-center"
    >
      <!--Profile picture -->
      <img
        class="shadow-sm h-12 w-12 rounded-full"
        :src="participant.profile"
        alt="user image"
      >

      <!--Participant name -->
      <h1 class="ml-2 text-base font-semibold chatbox chat truncate">
        {{ participant.full_name }}
      </h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Participant',
  props: {
    participant: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      participantProps: {}
    }
  }
}
</script>
