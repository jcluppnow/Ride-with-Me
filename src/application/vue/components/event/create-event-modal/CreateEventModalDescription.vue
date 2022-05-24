<template>
  <div class="mt-2 w-full h-full">
    <label class="text-sm md:text-base font-semibold text-gray-700">Description</label>

    <AppTextAreaInput
      class="h-full sm:pb-4"
      cy="descriptionInput"
      input-type="number"
      input-name="description"
      :error="errors.description ? errors.description[0] : ''"
      v-model="description"
      :attributes="{ maxlength: 3000 }"
      :additional-input-classes="['w-full', 'text-base', 'leading-snug', 'h-full']"
      :debounce="300"
    />
  </div>
</template>

<script>
import Event from '@/store/models/event'

export default {
  props: {
    errors: {
      required: true,
      type: Object
    }
  },
  computed: {
    description: {
      get () {
        return Event.getters('getNewEvent').description
      },
      set (value) {
        Event.dispatch('updateNewEvent', { description: value })
      }
    }
  }
}
</script>
