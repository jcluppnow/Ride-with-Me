<template>
  <div
    class="fixed bottom-0 left-0 z-50 flex flex-col justify-center items-center sm:m-4 inset-0 filter drop-shadow-lg"
  >
    <!-- Header for the Traffic Modal, contains severity and verified badge. -->
    <TrafficModalHeader
      @close="$emit('close')"
      :severity="traffic.severity"
      :verified="traffic.verified"
    />

    <!-- Body for the Traffic Modal, contains the date range and description. -->
    <TrafficModalBody
      :description="traffic.description + ' Traffic Event'"
      :starting-date="traffic.start_date"
      :end-date="traffic.end_date"
    />
  </div>
</template>

<script>
import TrafficModalHeader from './TrafficModalHeader'
import TrafficModalBody from './TrafficModalBody'

export default {
  name: 'TrafficModal',
  components: {
    TrafficModalHeader,
    TrafficModalBody
  },
  props: {
    traffic: {
      required: true,
      type: Object
    }
  }
}
</script>
