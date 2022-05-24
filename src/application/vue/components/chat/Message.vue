<template>
  <div
    class="flex"
    :class="{ 'justify-end': message.sender_id === authenticatedUser.id }"
  >
    <div
      class="w-auto rounded-lg shadow-lg p-2 max-w-md sm:max-w-lg flex flex-row space-x-2"
      :class="messageClass(message)"
    >
      <img
        class="shadow-sm h-12 w-12 rounded-full"
        :src="message.sender.profile"
        alt="user image"
      >
      <div class="flex flex-col">
        <div class="flex flex-row items-center space-x-2">
          <div class="font-semibold text-lg">
            {{ message.sender.full_name }}
          </div>
          <small>{{ timestamp() }}</small>
        </div>
        <div class="break-all max-w-xxs sm:max-w-md pr-3">
          <div class="break-normal break-words w-full">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ChatMessage from '@/store/models/chat_message'
import User from '@/store/models/user'

export default {
  name: 'Message',
  props: {
    event: {
      required: true,
      type: Object
    },
    message: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      content: null
    }
  },
  computed: {
    authenticatedUser () {
      return User.getters('authenticatedUser')
    }
  },
  methods: {
    sendMessage () {
      ChatMessage.dispatch('sendMessage', { content: this.content, event_id: this.event.event_id })
    },
    messageClass (message) {
      if (message.sender_id === this.authenticatedUser.id) {
        return 'bg-blue-300'
      } else if (message.sender_id === this.event.organiser_id) {
        return 'bg-indigo-400'
      } else {
        return 'bg-blue-400'
      }
    },
    timestamp () {
      const timestamp = this.message.createdAtDate
      return `${timestamp.getDate()}/${timestamp.getMonth() + 1} ${timestamp.getHours() % 12}:${`${timestamp.getMinutes()}`.padStart(2, '0')} ${timestamp.getHours() >= 12 ? 'PM' : 'AM'}`
    }
  }
}
</script>
