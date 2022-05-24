<template>
  <div class="sm:mt-4 w-full">
    <label class="text-sm md:text-base font-semibold text-gray-700">Route</label>

    <div class="flex flex-wrap sm:flex-nowrap">
      <div class="w-full sm:w-1/2">
        <button
          @click.prevent="$emit('draw')"
          class="w-full text-white bg-rwmDarkBlue hover:bg-rwmOrange rounded flex justify-center items-center pr-2 py-2 shadow-lg"
        >
          <!-- Draw vector -->
          <svg-vue
            icon="event/create-event-modal/draw-icon"
            class="ml-2 h-5 w-5 xl:ml-1"
          />

          <span class="text-sm md:text-base">Draw</span>
        </button>
      </div>

      <AppFileInput
        v-if="routeFileName === ''"
        class="w-full sm:w-1/2 mt-2 sm:mt-0 sm:ml-2"
        cy="routeFileInput"
        @change="routeFileUploaded"
        :attributes="{ accept: '.kml, .gpx' }"
        :additional-input-classes="['flex', 'items-center', 'py-2', 'pr-2', 'w-full']"
        :base-errorless-classes="['text-white', 'bg-rwmDarkBlue', 'hover:bg-rwmOrange', 'hover:text-white', 'rounded', 'inline-flex', 'items-center', 'justify-center', 'shadow-lg']"
        :base-error-classes="['text-white', 'bg-rwmDarkBlue', 'hover:bg-rwmOrange', 'hover:text-white', 'rounded', 'inline-flex', 'items-center', 'justify-center', 'shadow-lg']"
        :error="(errors.route_coordinates || errors.starting_location) ? 'Ensure the route is not empty' : ''"
      >
        <template #button>
          <!-- Upload vector -->
          <svg-vue
            icon="event/create-event-modal/upload-icon"
            class="ml-2 xl:ml-1 2xl:ml-1 h-5 w-5"
          />

          <span class="text-sm md:text-base">Import</span>
        </template>
      </AppFileInput>

      <div
        v-else
        class="flex flex-row items-center justify-center w-full sm:w-1/2 ml-2"
      >
        {{ routeFileName }}
        <button
          type="button"
          @click.prevent="clearRouteFile"
          class="text-red-500"
        >
          <svg-vue
            icon="event/close-icon"
            class="h-8 w-8"
          />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Event from '@/store/models/event'
import { mapActions, mapState } from 'vuex'

export default {
  props: {
    errors: {
      required: true,
      type: Object
    }
  },
  computed: {
    routeFileName () {
      return this.routeFile ? this.routeFile.name : ''
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
    ...mapState({
      routeFile: state => state.files.routeFile
    })
  },
  methods: {
    ...mapActions({
      setRouteFile: 'files/setRouteFile',
      clearRouteFile: 'files/clearRouteFile'
    }),
    async routeFileUploaded (files) {
    // Convert file using toGeoJSON, extract desired json and store.
      const selectedFile = files[0]
      this.setRouteFile(selectedFile)
      const fileText = await selectedFile.text()
      const xmlDom = new window.DOMParser().parseFromString(fileText, 'text/xml')

      const { toGeoJSON } = window

      if (fileText.includes('gpx')) {
        const geoData = toGeoJSON.gpx(xmlDom)
        const lineString = geoData.features.find(
          feature => feature.geometry.type === 'LineString'
        ).geometry

        lineString.coordinates = lineString.coordinates.map(
        // Strip elevation coordinate if present
          coord => [coord[0], coord[1]]
        )

        const extractedStartingPoint = lineString.coordinates[0]

        const startingPointObject = {
          type: 'Point',
          coordinates: [
            extractedStartingPoint[0],
            extractedStartingPoint[1]
          ]
        }

        this.routeCoordinates = lineString
        this.startingLocation = startingPointObject
      } else {
        const geoData = toGeoJSON.kml(xmlDom)
        const lineString = geoData.features.find(
          feature => feature.geometry.type === 'LineString'
        ).geometry

        lineString.coordinates = lineString.coordinates.map(
        // Strip elevation coordinate if present
          coord => [coord[0], coord[1]]
        )

        const extractedStartingPoint = lineString.coordinates[0]

        const startingPointObject = {
          type: 'Point',
          coordinates: [
            extractedStartingPoint[0],
            extractedStartingPoint[1]
          ]
        }

        this.routeCoordinates = lineString
        this.startingLocation = startingPointObject
      }
    }
  }
}
</script>
