<template>
  <ModalLayout
    :external-classes="'w-screen lg:max-w-3/2xl'"
    @close="$emit('draw')"
  >
    <template #header>
      <div class="shadow-lg sm:shadow-none h-14">
        <h1
          v-if="updatingEventId"
          class="text-gray-700 text-2xl font-semibold p-4"
        >
          Update Event
        </h1>
        <h1
          v-else
          class="text-gray-700 text-2xl font-semibold p-4"
        >
          Create Event
        </h1>
      </div>
    </template>

    <template #body>
      <div class="flex flex-col w-full">
        <CreateEventModalNameAndDate :errors="errors" />
        <CreateEventModalPhotoUpload :errors="errors" />
        <CreateEventModalDrawAndImport
          @draw="$emit('draw')"
          @clearRoute="$emit('clearRoute')"
          :errors="errors"
        />
        <CreateEventModalMaxAndAverage :errors="errors" />
        <CreateEventModalDescription :errors="errors" />
        <CreateEventModalPrivacy />
      </div>
    </template>

    <template #footer>
      <CreateEventModalFooterButtons
        @publishEvent="publishEvent"
        @updateEvent="updateEvent"
        @close="$emit('close')"
      />
    </template>
  </ModalLayout>
</template>

<script>
import ModalLayout from '@/components/ModalLayout'
import Event from '@/store/models/event'
import Weather from '@/store/models/weather'
import { mapState, mapActions } from 'vuex'
import CreateEventModalNameAndDate from './CreateEventModalNameAndDate'
import CreateEventModalPhotoUpload from './CreateEventModalPhotoUpload'
import CreateEventModalMaxAndAverage from './CreateEventModalMaxAndAverage'
import CreateEventModalDescription from './CreateEventModalDescription'
import CreateEventModalPrivacy from './CreateEventModalPrivacy'
import CreateEventModalFooterButtons from './CreateEventModalFooterButtons'
import CreateEventModalDrawAndImport from './CreateEventModalDrawAndImport'

export default {
  name: 'CreateEventModal',
  components: {
    ModalLayout,
    CreateEventModalNameAndDate,
    CreateEventModalPhotoUpload,
    CreateEventModalMaxAndAverage,
    CreateEventModalDescription,
    CreateEventModalFooterButtons,
    CreateEventModalDrawAndImport,
    CreateEventModalPrivacy
  },
  computed: {
    errors: {
      get () {
        return Event.getters('getErrors')
      },
      set (value) {
        console.log(value)
        return Event.dispatch('setErrors', value)
      }
    },
    startingTimeAsIsoString () {
    // Fetch the starting time for area code.
      if (this.startingTime) {
        return new Date(this.startingTime).toISOString()
      }
      return null
    },
    name () {
      return Event.getters('getNewEvent').name
    },
    description () {
      return Event.getters('getNewEvent').description
    },
    startingTime () {
      return Event.getters('getNewEvent').starting_time
    },
    averageSpeed () {
      return Event.getters('getNewEvent').average_speed
    },
    maxParticipants () {
      return Event.getters('getNewEvent').max_participants
    },
    isPrivate () {
      return Event.getters('getNewEvent').is_private
    },
    routeCoordinates: {
      get () {
        return Event.getters('getNewEvent').route_coordinates
      },
      set (value) {
        Event.dispatch('updateNewEvent', { route_coordinates: value })
      }
    },
    startingLocation: {
      get () {
        return Event.getters('getNewEvent').starting_location
      },
      set (value) {
        Event.dispatch('updateNewEvent', { starting_location: value })
      }
    },
    updatingEventId () {
      return Event.getters('getNewEvent').event_id
    },
    ...mapState({
      imageFile: state => state.files.imageFile,
      routeFile: state => state.files.routeFile
    })
  },
  methods: {
    ...mapActions({
      setImageFile: 'files/setImageFile',
      setRouteFile: 'files/setRouteFile',
      clearRouteFile: 'files/clearRouteFile',
      clearImageFile: 'files/clearImageFile'
    }),
    clearRoute () {
      this.clearRouteFile()
      this.routeCoordinates = { type: 'LineString', coordinates: [] }
      this.startingLocation = { type: 'Point', coordinates: [] }
    },
    publishEvent () {
      const formData = new FormData()
      formData.append('name', this.name)
      formData.append('is_private', this.isPrivate)
      formData.append('description', this.description)
      formData.append('max_participants', this.maxParticipants)
      formData.append('hero_image', this.imageFile)
      formData.append('average_speed', this.averageSpeed)
      formData.append('starting_time', this.startingTimeAsIsoString)
      formData.append('starting_location', JSON.stringify(this.startingLocation))
      formData.append('route_coordinates', JSON.stringify(this.routeCoordinates))
      Event.dispatch('createEvent', formData).then((newEvent) => {
        this.clearRouteFile()
        this.clearImageFile()

        const latitude = newEvent.starting_location.coordinates[0]
        const longitude = newEvent.starting_location.coordinates[1]
        Weather.dispatch('getWeather', { eventId: newEvent.event_id, lat: latitude, long: longitude, weatherDate: newEvent.starting_time }).then(({ weather: [weather] }) => {
          window.swal.fire({
            title: 'Event created!',
            icon: 'success',
            confirmButtonText: 'Okay'
          }).then(() => {
            this.$router.push({ name: 'Dashboard', hash: `#${newEvent.event_id}` })
          })
        }).catch((error) => {
          window.swal.fire({
            title: 'Event created!',
            icon: 'success',
            confirmButtonText: 'Okay'
          }).then(() => {
            this.$router.push({ name: 'Dashboard', hash: `#${newEvent.event_id}` })
          })
          console.log(error)
          this.errors = error.data || {}
        })
      }).catch((error) => {
        window.swal.fire({
          title: 'Failed to create event!',
          text: 'Please check the form for errors',
          icon: 'error',
          confirmButtonText: 'Okay'
        })
        this.errors = error.data
      })
    },
    updateEvent (eventId) {
      const formData = new FormData()
      formData.append('name', this.name)
      formData.append('is_private', this.isPrivate)
      formData.append('description', this.description)
      formData.append('max_participants', this.maxParticipants)
      formData.append('average_speed', this.averageSpeed)
      formData.append('starting_time', this.startingTimeAsIsoString)
      if (this.imageFile) {
        formData.append('hero_image', this.imageFile)
      }
      formData.append('starting_location', JSON.stringify(this.startingLocation))
      formData.append('route_coordinates', JSON.stringify(this.routeCoordinates))
      Event.dispatch('updateEvent', { eventId: eventId, event: formData }).then((newEvent) => {
        this.clearRouteFile()
        this.clearImageFile()
        window.swal.fire({
          title: 'Event updated!',
          icon: 'success',
          confirmButtonText: 'Okay'
        }).then(() => {
          this.$router.push({ name: 'Dashboard', hash: `#${newEvent.event_id}` })
        })
      }).catch((error) => {
        window.swal.fire({
          title: 'Failed to update event!',
          text: 'Please check the form for errors',
          icon: 'error',
          confirmButtonText: 'Okay'
        })
        this.errors = error.data
      })
    }
  }
}
</script>
