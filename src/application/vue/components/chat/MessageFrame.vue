<template>
  <!-- Enter Message -->
  <div class="bg-white p-1 sm:mb-2 flex flex-col w-full justify-end h-full overflow-hidden rounded shadow-lg">
    <div
      cy="messageFrame"
      class="overflow-y-auto p-1 flex flex-col space-y-2 scrollbar overflow-x-hidden"
      ref="messageList"
      @scroll="scrolled"
    >
      <Message
        v-for="(message, i) in messages"
        :key="i"
        :message="message"
        :event="event"
      />
    </div>
    <div class="flex flex-row w-full">
      <AppTextInput
        cy="messageInput"
        input-type="text"
        :name="'messageInput'"
        v-model="content"
        :attributes="{ maxlength: 255 }"
        :class="['flex-grow', 'h-full']"
        :additional-input-classes="['w-full', 'text-base', 'p-1', 'h-full']"
        @enter="sendMessage"
      />
    </div>
  </div>
</template>

<script>
import ChatMessage from '@/store/models/chat_message'
import User from '@/store/models/user'
import Message from './Message'

export default {
  name: 'MessageFrame',
  components: {
    Message
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      content: null,
      page: 1
    }
  },
  watch: {
    messages () {
      if (this.$refs.messageList && this.$refs.messageList.scrollHeight - this.$refs.messageList.scrollTop === this.$refs.messageList.clientHeight) {
        this.$nextTick(() => {
          const list = this.$refs.messageList
          list.scrollTop = list.scrollHeight
        })
      }
    },
    event (newVal, oldVal) {
      if (newVal.event_id !== oldVal.event_id) {
        this.page = 1
        this.content = null
        this.$nextTick(() => {
          const list = this.$refs.messageList
          list.scrollTop = list.scrollHeight
        })
      }
    }
  },
  mounted () {
    this.$nextTick(() => {
      const list = this.$refs.messageList
      list.scrollTop = list.scrollHeight
    })
  },
  computed: {
    messages () {
      return ChatMessage.getters('messagesForEvent')(this.event.event_id)
    },
    authenticatedUser () {
      return User.getters('authenticatedUser')
    },
    latestMessage () {
      return ChatMessage.query().where('event_id', this.event.event_id).orderBy('message_id', 'desc').first()
    }
  },
  methods: {
    scrolled (ev) {
      const list = this.$refs.messageList
      if (list) {
        const scrollable = this.$refs.messageList.scrollHeight > this.$refs.messageList.clientHeight
        if (scrollable && this.$refs.messageList.scrollTop === 0) {
          ChatMessage.dispatch('getMessagesForEvent', { eventId: this.event.event_id, page: this.page + 1 }).then(({ chat_message: messages }) => {
            // delete messages that are older than the latest paginated message, saving up to 16 messages that are older`
            const latestMessage = messages[0]
            const messagesToDelete = ChatMessage.query().where('event_id', this.event.event_id).where((message) => message.message_id > latestMessage.message_id).orderBy('message_id').offset(16).get()

            messagesToDelete.forEach((message) => {
              if (message.message_id !== this.latestMessage.message_id) {
                message.$delete()
              }
            })

            this.$refs.messageList.scrollTop = Math.round(this.$refs.messageList.scrollHeight * 0.1)

            this.page += 1
          }).catch(console.log)
        } else if (this.page > 1 && scrollable && this.$refs.messageList.scrollHeight - this.$refs.messageList.scrollTop === this.$refs.messageList.clientHeight) {
          ChatMessage.dispatch('getMessagesForEvent', { eventId: this.event.event_id, page: this.page - 1 >= 1 ? this.page - 1 : 1 }).then(({ chat_message: messages }) => {
            // delete messages that are younger than the latest paginated message, saving up to 16 messages that are younger
            const latestMessage = messages[messages.length - 1]
            const messagesToDelete = ChatMessage.query().where('event_id', this.event.event_id).where((message) => message.message_id < latestMessage.message_id).orderBy('message_id', 'desc').offset(16).get()
            messagesToDelete.forEach((message) => {
              if (message.message_id !== this.latestMessage.message_id) {
                message.$delete()
              }
            })

            this.$refs.messageList.scrollTop = Math.round(this.$refs.messageList.scrollHeight * 0.1)

            this.page = this.page - 1 > 1 ? this.page - 1 : 1
          }).catch(console.log)
        }
      }
    },
    sendMessage () {
      if (this.content !== '') {
        ChatMessage.dispatch('sendMessage', { content: this.content, event_id: this.event.event_id }).then(() => {
          this.content = ''
        })
      }
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
