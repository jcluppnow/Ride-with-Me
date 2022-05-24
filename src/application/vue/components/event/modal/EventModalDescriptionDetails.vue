<template>
  <div class="scrollbar overflow-y-auto text-gray-600 font-semibold w-full max-h-96 sm:w-2/3 sm:pr-4  ">
    <EventBadges :event="event" />

    <div class="mt-2">
      <span class="whitespace-pre-wrap">{{ event.description ? event.description : '' }}</span>
    </div>
  </div>
</template>

<script>
import EventBadges from './EventModalBadges'

export default {
  name: 'EventModalHeaderDetails',
  components: {
    EventBadges
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
