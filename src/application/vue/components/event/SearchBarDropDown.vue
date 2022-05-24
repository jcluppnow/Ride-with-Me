<template>
  <div class="shadow-md bg-white flex flex-col space-y-1 absolute py-1 px-1 w-full">
    <SearchBarSearchedEvent
      v-for="(event, index) in events"
      :key="index"
      :event="event"
      @select="$emit('select', $event)"
    />
  </div>
</template>

<script>
import SearchBarSearchedEvent from './SearchBarSearchedEvent'

export default {
  props: {
    events: {
      required: true,
      type: Array
    }
  },
  components: {
    SearchBarSearchedEvent
  }
}
</script>
