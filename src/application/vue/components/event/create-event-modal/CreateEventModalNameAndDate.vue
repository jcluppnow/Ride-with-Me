<template>
  <div class="flex flex-wrap sm:flex-nowrap">
    <div class="font-semibold flex flex-col w-full sm:w-1/2">
      <label
        for="eventNameInput"
        class="text-sm md:text-base text-gray-700"
      >Name</label>

      <AppTextInput
        cy="eventNameInput"
        input-type="text"
        :name="'eventNameInput'"
        :error="errors.name ? errors.name[0] : ''"
        v-model="name"
        :attributes="{ maxlength: 255 }"
        :additional-input-classes="['w-full', 'text-base', 'p-1']"
        :debounce="300"
      />
    </div>

    <div class="font-semibold sm:ml-2 mt-2 flex flex-col w-full sm:mt-0 sm:w-1/2">
      <label
        for="eventDateInput"
        class="text-sm md:text-base text-gray-700"
      >Date</label>

      <AppTextInput
        cy="eventDateInput"
        input-type="datetime-local"
        :name="'eventDateInput'"
        :error="errors.starting_time ? 'Invalid date.' : ''"
        v-model="startingTime"
        :additional-input-classes="['w-full', 'text-base', 'leading-snug', 'p-1']"
        :debounce="300"
      />
    </div>
  </div>
</template>

<script>
import Event from '@/store/models/event'

export default {
  computed: {
    errors: {
      get () {
        return Event.getters('getErrors')
      },
      set (value) {
        Event.dispatch('addError', { field: value.field, value: value.value })
      }
    },
    name: {
      get () {
        return Event.getters('getNewEvent').name
      },
      set (value) {
        Event.dispatch('updateNewEvent', { name: value })
      }
    },
    startingTime: {
      get () {
        return Event.getters('getNewEvent').starting_time
      },
      set (value) {
        Event.dispatch('updateNewEvent', { starting_time: value })
      }
    }
  },
  watch: {
    name (value, oldValue) {
      if (value === '' && oldValue !== '') {
        this.errors = { field: 'name', value: 'Cannot be empty' }
      } else {
        Event.dispatch('removeError', { field: 'name' })
      }
    },
    startingTime (value) {
      if (value === '') {
        this.errors = { field: 'starting_time', value: 'Cannot be empty' }
      } else if (new Date(value) < new Date()) {
        this.errors = { field: 'starting_time', value: 'Cannot be in the past' }
      } else {
        Event.dispatch('removeError', { field: 'starting_time' })
      }
    }
  }
}
</script>
