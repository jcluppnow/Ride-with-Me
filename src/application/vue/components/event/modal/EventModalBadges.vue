<template>
  <div class="flex space-x-1">
    <div
      v-if="event.started"
      class="flex items-center bg-indigo-500 text-sm text-white px-2 py-1 rounded"
    >
      <svg-vue
        icon="buttons/tick-icon"
        class="h-4 w-4 text-white"
      />

      Started
    </div>
    <div
      v-if="event.checked_in"
      class="flex items-center bg-indigo-500 text-sm text-white px-2 py-1 rounded"
    >
      <svg-vue
        icon="buttons/tick-icon"
        class="h-4 w-4 text-white"
      />

      Checked in
    </div>
    <div
      v-if="event.finished"
      class="flex items-center bg-red-600 text-sm text-white px-2 py-1 rounded"
    >
      <svg-vue
        icon="buttons/tick-icon"
        class="h-4 w-4 text-white"
      />

      Finished
    </div>
    <div
      v-if="event.is_full"
      class="flex items-center bg-red-600 text-sm text-white px-2 py-1 rounded"
    >
      <svg-vue
        icon="buttons/tick-icon"
        class="h-4 w-4 text-white"
      />

      Full
    </div>
    <div
      v-if="event.is_private"
      class="flex items-center bg-red-600 text-sm text-white px-2 py-1 rounded"
    >
      <svg-vue
        icon="buttons/tick-icon"
        class="h-4 w-4 text-white"
      />

      Private
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventModalBadges',
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}
</script>
