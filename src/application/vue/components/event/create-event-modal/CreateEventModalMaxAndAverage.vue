<template>
  <div class="flex flex-wrap mt-2 sm:flex-nowrap">
    <div class="flex flex-col w-full sm:w-1/2">
      <span
        class="text-sm md:text-base font-semibold text-gray-700"
        for="max_participants"
      >Max Participants:</span>

      <AppTextInput
        cy="maxParticipantsInput"
        input-type="number"
        :name="'maxParticipants'"
        :error="errors.max_participants ? errors.max_participants[0] : ''"
        v-model="maxParticipants"
        :attributes="{ required: true, min:1 }"
        :additional-input-classes="['w-full', 'text-base', 'leading-snug', 'p-1']"
        :debounce="300"
      />
    </div>

    <div class="sm:ml-2 flex flex-col w-full mt-2 sm:mt-0 sm:w-1/2">
      <span
        class="text-sm md:text-base font-semibold text-gray-700 text-sm"
        for="average_speed"
      >Average Speed:</span>

      <AppTextInput
        cy="averageSpeedInput"
        input-type="number"
        :name="'averageSpeed'"
        :error="errors.average_speed ? errors.average_speed[0] : ''"
        v-model="averageSpeed"
        :attributes="{ required: true, min: 1}"
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
    averageSpeed: {
      get () {
        return Event.getters('getNewEvent').average_speed
      },
      set (value) {
        Event.dispatch('updateNewEvent', { average_speed: value })
      }
    },
    maxParticipants: {
      get () {
        return Event.getters('getNewEvent').max_participants
      },
      set (value) {
        Event.dispatch('updateNewEvent', { max_participants: value })
      }
    }
  },
  watch: {
    averageSpeed (value) {
      Event.dispatch('removeError', { field: 'average_speed' })
      if (value === '') {
        this.errors = { field: 'average_speed', value: 'Cannot be empty' }
      } else if (value === '0') {
        this.errors = { field: 'average_speed', value: 'Cannot be 0' }
      } else {
        const convertedValue = Number(value)
        if (convertedValue < 0) {
          this.errors = { field: 'average_speed', value: 'Cannot be negative' }
        }
      }
    },
    maxParticipants (value) {
      Event.dispatch('removeError', { field: 'max_participants' })
      if (value === '') {
        this.errors = { field: 'max_participants', value: 'Cannot be empty' }
      } else if (value === '0') {
        this.errors = { field: 'max_participants', value: 'Cannot be 0' }
      } else {
        const convertedValue = Number(value)
        if (convertedValue < 0) {
          this.errors = { field: 'max_participants', value: 'Cannot be negative' }
        }
      }
    }
  }
}
</script>
