<template>
  <div
    @click.prevent="$router.push({ path: notification.link })"
    class="rounded text-black-900 overflow-hidden shadow-lg bg-white cursor-pointer"
  >
    <div class="flex flex-row justify-between p-2 px-4">
      <div
        class="flex flex-col"
      >
        <div>
          {{ notification.notifier.full_name }} in {{ notification.event.name }}
          <small class="ml-2">
            {{ timestamp }}
          </small>
        </div>

        <!--Participant name -->
        <h1 class="text-base font-semibold chatbox chat truncate">
          {{ notification.content }}
        </h1>
      </div>
      <div class="flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        ><path d="M13.025 1l-2.847 2.828 6.176 6.176h-16.354v3.992h16.354l-6.176 6.176 2.847 2.828 10.975-11z" /></svg>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Notification',
  props: {
    notification: {
      required: true,
      type: Object
    }
  },
  computed: {
    timestamp () {
      const timestamp = this.notification.createdAtDate
      return `${timestamp.getDate()}/${timestamp.getMonth() + 1} ${`${timestamp.getHours() % 12}`.padStart(2, '0')}:${`${timestamp.getMinutes()}`.padStart(2, '0')}`
    }
  }
}
</script>
