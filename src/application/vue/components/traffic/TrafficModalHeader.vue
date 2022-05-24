<template>
  <!-- Main container for Traffic Modal Header. -->
  <div
    class="flex flex-row rounded-t-md py-2 w-9/12 sm:w-5/12 filter drop-shadow"
    :class="{ 'bg-green-300': isLowImpact, 'bg-yellow-400': isMinorImpact, 'bg-yellow-600': isModerateImpact, 'bg-red-600': isSevereImpact }"
  >
    <!-- Container for alert vector, verified badge, severity and close button. -->
    <div class="flex flex-row w-5/6">
      <svg-vue
        class="my-auto ml-2 h-8 w-8 text-white"
        icon="traffic/alert"
      />

      <!-- Inner container for alert vector, verified badge, severity and close button to assist with positioning. -->
      <div>
        <!-- Container for verified badge and severity. Conditionally rendered if verified is true. -->
        <div
          v-if="verified"
          class="flex flex-col"
        >
          <span class="ml-1 align-middle text-white text-base sm:text-2xl font-bold">{{ severityDescription }} Traffic Event</span>
          <div class="ml-1 flex content-center w-5/12 bg-white bg-opacity-70 rounded">
            <span
              class="mx-auto text-xs sm:text-sm font-medium"
              :class="{ 'text-green-300': isLowImpact, 'text-yellow-400': isMinorImpact, 'text-yellow-600': isModerateImpact, 'text-red-600': isSevereImpact } "
            >VERIFIED</span>
          </div>
        </div>

        <!-- Container for severity description. Conditionally rendered if verified is false. -->
        <div
          class="flex"
          v-else
        >
          <!-- Description of traffic event severity. -->
          <span class="mt-1 ml-1 font-bold align-middle text-white">{{ severityDescription }} Traffic Event</span>
        </div>
      </div>
    </div>

    <!-- Container for close button. -->
    <div class="relative w-1/6">
      <!-- Wrap svg-vue in a button to enable onclick function. -->
      <button
        class="absolute top-0 right-0 mr-2"
        @click="$emit('close')"
      >
        <!-- Vector asset for close button. -->
        <svg-vue
          class="h-6 w-6 text-white"
          icon="buttons/close-icon"
        />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrafficModalHeader',
  data () {
    return {
      isLowImpact: false,
      isMinorImpact: false,
      isModerateImpact: false,
      isSevereImpact: false,
      severityDescription: 'Unknown Severity'
    }
  },
  created () {
    switch (this.severity) {
    case 1:
      this.severityDescription = 'Low impact'
      this.isLowImpact = true
      break
    case 2:
      this.severityDescription = 'Minor'
      this.isMinorImpact = true
      break
    case 3:
      this.severityDescription = 'Moderate'
      this.isModerateImpact = true
      break
    case 4:
      this.severityDescription = 'Serious'
      this.isSevereImpact = true
      break
    default:
      this.severityDescription = 'Unknown severity'
      this.isLowImpact = true
    }
  },
  props: {
    severity: {
      default: 1,
      required: true,
      type: Number
    },
    verified: {
      default: false,
      required: true,
      type: Boolean
    }
  }
}
</script>
