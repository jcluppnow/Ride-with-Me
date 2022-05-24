<template>
  <div
    class="side-scroll max-w-screen overflow-x-auto"
  >
    <div class="pr-4 sm:pl-4 flex sm:-ml-2 pb-4">
      <!-- List events horizontally if they exist. -->
      <div
        v-for="(eventModel, i) in events"
        :key="i"
        class="mt-0 flex-shrink-0"
      >
        <!-- Event card component that emits an a click event to parent. -->
        <EventCard
          :cy="'event-card-' + i"
          :event="eventModel"
          class="m-2 cursor-pointer"
          @clicked="$emit('eventClicked', eventModel.event_id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EventCard from './EventCard'

export default {
  name: 'EventList',
  components: {
    EventCard
  },
  props: {
    events: {
      required: true,
      type: Array
    }
  }
}
</script>

<style scoped>
.max-w-screen {
    max-width: 100vw;
}

/* width */
.side-scroll::-webkit-scrollbar {
width: 6px;
height: 8px;
}

/* Track */
.side-scroll::-webkit-scrollbar-track {
border-radius: 2px;
}

/* Handle */
.side-scroll::-webkit-scrollbar-thumb {
background: gray;
border-radius: 10px;
}

/* Handle on hover */
.side-scroll::-webkit-scrollbar-thumb:hover {
background: #4F4E4E;
}
</style>
