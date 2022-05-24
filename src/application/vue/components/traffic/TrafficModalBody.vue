<template>
  <!-- Main container for Traffic Modal Body -->
  <div
    class="py-5 pl-2 pr-4 bg-white rounded-b-md mx-auto w-9/12 sm:w-5/12"
  >
    <!-- Container for date range vector and date range.  -->
    <div class="flex flex-row">
      <!-- Calendar vector asset. -->
      <svg-vue
        class="ml-0.5 text-gray-400 h-7 w-7"
        icon="traffic/calendar"
      />
      <!-- Conditionally render this start/end time or start time based on whether end time was set. -->
      <span
        class="ml-3 font-semibold mt-1"
        v-if="endTime"
      > {{ startTime }}{{ endTime }}</span>
      <span v-else> {{ startTime }}</span>
    </div>

    <!-- Container for Traffic Event description. -->
    <div class="ml-10 font-medium text-sm md:text-base">
      <!-- Description  of the Traffic Event. -->
      <span>{{ description }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrafficModalBody',
  data () {
    return {
      startTime: '',
      endTime: ''
    }
  },
  created () {
    // Convert start date to JS Date object.
    const startDate = new Date(this.startingDate)

    // Convert end date to JS Date object.
    const end = new Date(this.endDate)

    // Convert the start date object to a string with the day/month/year format.
    this.startTime = startDate.getDate() + '/' + (startDate.getMonth() + 1) + '/' + startDate.getFullYear()

    // Convert the end date object to a string with the day/month/year format if the string is not empty.
    if (this.endDate.length !== 0) this.endTime = ' - ' + end.getDate() + '/' + (end.getMonth() + 1) + '/' + end.getFullYear()
  },
  props: {
    description: {
      default: '',
      required: true,
      type: String
    },
    startingDate: {
      default: '',
      required: true,
      type: String
    },
    endDate: {
      default: '',
      required: false,
      type: String
    }
  }
}
</script>
