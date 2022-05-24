<template>
  <div
    class="text-gray-900 bg-white overflow-hidden hover:bg-rwmDarkBlue hover:text-white transition duration-100 ease-in"
    @click.prevent="$emit('select', event.event_id)"
  >
    <div class="flex items-center">
      <!--Event picture -->
      <img
        class="rounded shadow-sm h-14 w-14"
        alt="user image"
        :src="event.hero_image"
      >

      <div class="flex flex-col ml-2">
        <h1 class="text-base font-semibold overflow-ellipsis overflow-hidden whitespace-nowrap">
          {{ event.name }}
        </h1>
        <h2 class="text-base font-medium text-gray-500 overflow-ellipsis overflow-hidden whitespace-nowrap w-48">
          {{ event.organiser.full_name }}
        </h2>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}
</script>
