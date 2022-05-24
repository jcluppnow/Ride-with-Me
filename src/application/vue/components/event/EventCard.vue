<template>
  <div
    class="hover:bg-rwmDarkBlue hover:text-white antialiased text-gray-700 rounded-lg bg-white overflow-hidden shadow-lg w-80"
    @click.prevent="$emit('clicked')"
  >
    <div class="overflow-hidden h-32">
      <img
        class="object-cover object-center min-h-full min-w-full"
        :src="event.hero_image"
        alt="image"
      >
    </div>

    <div
      class="p-5"
    >
      <h1 class="text-2xl font-semibold truncate">
        {{ event.name }}
      </h1>
      <h2 class="text-lg mt-2 font-semibold truncate">
        {{ formattedDate }}
      </h2>

      <div class="flex space-x-1 mt-2">
        <!-- Location Icon -->
        <svg-vue
          icon="event/location-icon"
          class="h-5 w-5"
        />

        <p class="leading-tight truncate">
          {{ event.location_string }}
        </p>
      </div>

      <div class="flex items-center justify-start space-x-2 mt-4 text-sm">
        <div class="space-x-1 inline-flex items-center">
          <!-- Distance Icon -->
          <svg-vue
            icon="event/distance-icon"
            class="h-4 w-4"
          />

          <p class="truncate">
            {{ event.distanceInKm.toFixed(2) }}
          </p>km
        </div>

        <div class="space-x-1 inline-flex items-center">
          <!-- Speed Icon -->
          <svg-vue
            icon="event/speed-icon"
            class="h-4 w-4"
          />
          <p class="truncate">
            {{ event.average_speed }}
          </p>km/h
        </div>

        <div class="space-x-1 inline-flex items-center">
          <!-- Duration Icon -->
          <svg-vue
            icon="event/duration-icon"
            class="h-4 w-4"
          />
          <p class="truncate">
            {{ roundTime(event.durationinHr) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'EventCard',
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      showModal: false,
      eventProps: {
        distance: 4,
        wind: 0.2,
        duration: 1
      }
    }
  },
  computed: {
    formattedDate () {
      const date = this.ordinal_suffix_of(this.event.startingTimeDate.getDate())
      const month = Intl.DateTimeFormat('en-AU', { month: 'long' }).format(this.event.startingTimeDate)
      return `${date} of ${month} ${this.event.startingTimeDate.getUTCFullYear()}`
    }
  },
  methods: {
    roundTime (time) {
      const n = new Date(0, 0)
      n.setMinutes(Math.round((+time * 60) / 5) * 5)
      n.setHours(parseInt(Number(time)))
      return n.toTimeString().slice(0, 5)
    },
    ordinal_suffix_of (i) {
      const j = i % 10
      const k = i % 100
      if (j === 1 && k !== 11) {
        return i + 'st'
      }
      if (j === 2 && k !== 12) {
        return i + 'nd'
      }
      if (j === 3 && k !== 13) {
        return i + 'rd'
      }
      return i + 'th'
    }
  }
}
</script>
