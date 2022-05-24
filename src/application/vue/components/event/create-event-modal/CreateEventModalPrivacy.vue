<template>
  <div class="sm:mt-4 w-full">
    <span class="text-sm md:text-base font-semibold text-gray-700 pb-2">Privacy</span>
    <div class="flex items-center">
      <input
        cy="publicRadioInput"
        name="privacyChoice"
        type="radio"
        value="false"
        v-model="isPrivate"
      >

      <span class="ml-1 text-sm md:text-base">Public</span>
      <span class="text-sm md:text-base text-gray-600 ml-6">Anyone can see and attend this event.</span>
    </div>

    <div class="flex items-center">
      <input
        cy="privateRadioInput"
        name="privacyChoice"
        type="radio"
        value="true"
        v-model="isPrivate"
      >

      <span class="ml-1 text-sm md:text-base">Private</span>
      <span class="text-sm md:text-base text-gray-600 ml-4">Only those you share a link with can view this event.</span>
    </div>
  </div>
</template>

<script>
import Event from '@/store/models/event'

export default {
  computed: {
    isPrivate: {
      get () {
        return Event.getters('getNewEvent').is_private
      },
      set (value) {
        Event.dispatch('updateNewEvent', { is_private: value })
      }
    }
  }
}
</script>
