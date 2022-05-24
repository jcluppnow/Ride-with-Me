<template>
  <!-- Event Chat box -->
  <div
    class="rounded text-gray-900 bg-white overflow-hidden shadow-lg hover:bg-blue-100 transition duration-100 ease-in"
    @click.prevent="$emit('select')"
  >
    <div
      class="flex flex-row items-center"
    >
      <!--Profile picture -->
      <img
        class="shadow-sm h-14 w-14 rounded"
        :src="event.hero_image"
        alt="user image"
      >

      <!-- Text -->
      <div class="flex flex-col ml-2">
        <!--Event name -->
        <h1 class="text-base font-semibold overflow-ellipsis overflow-hidden whitespace-nowrap">
          {{ event.name }}
        </h1>
        <!--Message content -->
        <h2 class="text-base font-medium text-gray-500 overflow-ellipsis overflow-hidden whitespace-nowrap w-60">
          {{ latestMessage ? latestMessage.content : '' }}
        </h2>
      </div>
    </div>
  </div>
</template>

<script>
import ChatMessage from '@/store/models/chat_message'

export default {
  name: 'EventChat',
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  computed: {
    latestMessage () {
      return ChatMessage.query().where('event_id', this.event.event_id).orderBy('message_id', 'desc').first()
    }
  }
}
</script>
