<template>
  <div>
    <div class="w-full flex items-center mt-1 border-b border-gray-300 pb-2">
      <img
        class="w-20 h-20 rounded-md"
        :src="event.organiser.profile"
      >

      <div class="pl-4">
        <p class="font-semibold text-lg">
          Organised By
        </p>
        <p class="text-xl">
          {{ event.organiser.full_name }}
        </p>
      </div>
    </div>

    <span v-if="event.weather">
      <div

        class="flex justify-between items-center mt-2"
      >
        <div class="flex items-center w-max ">
          <!-- Weather Icon -->
          <svg-vue
            icon="event/weather-icon"
            class="h-8 w-8 text-yellow-500"
          />

          <div class="pl-1">
            {{ event.weather.temperature }}℃
          </div>
        </div>

        <div class="flex items-center w-max">
          <!-- Rain Icon -->
          <svg-vue
            icon="event/rain-icon"
            class="h-6 w-6 text-rwmDarkBlue"
          />

          <div class="pl-1">
            {{ event.weather.precipitation }} %
          </div>
        </div>
      </div>

      <div
        class="flex justify-between items-center mt-2 border-b border-gray-300 pb-2"
      >
        <div class="flex items-center w-max ">
          <!-- Wind Icon -->
          <svg-vue
            id="windDirectionVector"
            icon="event/wind-icon"
            class="h-8 w-8"
          />

          <div class="pl-1">
            {{ event.weather.wind_speed }} km/h
          </div>
        </div>

        <div class="flex items-center w-max ">
          <!-- Weather Icon -->
          <svg-vue
            icon="event/humidity-icon"
            class="h-6 w-6 text-blue-600"
          />

          <div class="pl-1">
            {{ event.weather.humidity }}%
          </div>
        </div>
      </div>
    </span>

    <div class="flex sm:flex-col justify-between sm:justify-start">
      <div class="flex items-center mt-2">
        <!-- Map Icon -->
        <svg-vue
          icon="event/map-icon"
          class="h-8 w-8"
        />

        <div class="pl-2">
          <button
            class="font-semibold"
            @click.prevent="$emit('viewOnMap')"
          >
            View on Map
          </button>
        </div>
      </div>
      <div class="flex items-center text-blue-500 mt-2">
        <!-- Download Icon -->
        <svg-vue
          icon="event/download-icon"
          class="h-8 w-8"
        />

        <div class="pl-2">
          <a
            :href="`api/v1/events/${event.event_id}.gpx`"
            download
          >
            Download to GPS
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted () {
    console.log('Weather during mounted')
    console.log(event)
    console.log(this.event)
    if (this.event.weather !== null) {
      this.weatherLoaded = true
      const windDirectionVector = document.getElementById('windDirectionVector')
      // svg is offset by 90 degrees
      const rotation = `rotate(${this.event.weather.wind_direction - 90})`
      windDirectionVector.setAttribute('transform', rotation)
    }
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}
</script>
