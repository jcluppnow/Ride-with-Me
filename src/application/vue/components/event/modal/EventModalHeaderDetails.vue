<template>
  <div class="relative">
    <div class="absolute overflow-hidden sm:rounded-t w-full h-full">
      <div class="overflow-hidden">
        <img
          class="w-full sm:transform sm:-translate-y-1/3 h-full"
          :src="event.hero_image"
          alt="image"
        >
        <!-- Apply a dark gradient effect over the header image -->
        <div class="absolute top-0 left-0 z-1 w-full h-full bg-gradient-to-t from-black to-transparent sm:rounded-t" />
      </div>
    </div>
    <div class="overflow-visible">
      <div class="relative z-40 pt-10 pb-2 font-bold px-4 w-full sm:rounded-t">
        <h1 class="text-2xl text-white font-semibold truncate">
          {{ event.name }}
        </h1>
        <h2 class="text-base font-medium text-white mt-2">
          {{ formattedDate }}
        </h2>

        <div class="flex space-x-1 mt-2 text-white">
          <!-- Location Icon -->
          <svg-vue
            icon="event/location-icon"
            class="h-5 w-5"
          />

          <p class="leading-tight font-medium">
            {{ event.location_string }}
          </p>
        </div>

        <div class="flex text-md font-semibold flex-col justify-start space-y-1 mt-2 sm:items-center sm:flex-row sm:justify-between">
          <div class="space-x-2">
            <div class="space-x-1 text-white inline-flex items-center">
              <!-- Distance Icon -->
              <svg-vue
                icon="event/distance-icon"
                class="h-5 w-5"
              />
              <p>{{ event.distanceInKm.toFixed(2) }} km</p>
            </div>
            <div class="space-x-1 text-white inline-flex items-center">
              <!-- Speed Icon -->
              <svg-vue
                icon="event/speed-icon"
                class="h-5 w-5"
              />
              <p>{{ event.average_speed }} km/h</p>
            </div>
            <div class="space-x-1 text-white inline-flex items-center">
              <!-- Duration Icon -->
              <svg-vue
                icon="event/duration-icon"
                class="h-5 w-5"
              />
              <p>{{ roundTime(event.durationinHr) }}hr</p>
            </div>
          </div>

          <EventModalIcons
            :event="event"
            @update="$emit('update')"
            @delete="$emit('delete')"
            @showParticipants="$emit('showParticipants')"
            @showInfo="$emit('showInfo')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventModalIcons from './EventModalIcons'

export default {
  name: 'EventModalHeaderDetails',
  components: {
    EventModalIcons
  },
  props: {
    event: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      showParticipants: false,
      eventProps: {
        date: new Date(),
        location: 'Elizabeth Quay, WA',
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
      const time = Intl.DateTimeFormat('en-AU', { hour: 'numeric', minute: 'numeric' }).format(this.event.startingTimeDate)
      return `${date} of ${month} ${this.event.startingTimeDate.getUTCFullYear()}, ${time}`
    }
  },
  methods: {
    roundTime (time) {
      const n = new Date(0, 0)
      n.setMinutes(Math.round((time * 60) / 5) * 5)
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
