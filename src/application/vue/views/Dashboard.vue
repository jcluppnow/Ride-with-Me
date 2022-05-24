<template>
  <div>
    <!-- Container for Mapworks. -->
    <div>
      <MapworksEmbed
        @ready="loadMapworks"
        ref="mapworks"
      />

      <!-- Bottom right bottoms -->
      <div class="absolute z-10 bottom-2 right-2 flex flex-col space-y-2">
        <!-- Filter Button -->
        <button
          type="button"
          class="p-3 bg-rwmOrange text-gray-100 font-semibold rounded-full shadow-lg text-center"
          @click.prevent="showFilterModal = !showFilterModal"
        >
          <!-- Filter SVG -->
          <svg-vue
            icon="dashboard/filter-icon"
            class="text-white h-6 w-6"
          />
        </button>

        <button
          type="button"
          class="p-3 bg-rwmOrange text-gray-100 font-semibold rounded-full shadow-lg text-center"
          @click.prevent="getUserLocation"
        >
          <!-- Location Cross SVG -->
          <svg-vue
            icon="event/location"
            class="h-6 w-6 text-white"
          />
        </button>

        <button
          v-if="currentEvent"
          type="button"
          class="p-3 bg-rwmOrange text-gray-100 font-semibold rounded-full shadow-lg text-center"
          @click.prevent="$router.push({ name: 'Chat', hash: `#${currentEvent}`})"
        >
          <!-- Chat message SVG -->
          <svg-vue
            icon="dashboard/chat-icon"
            class="h-6 w-6 text-white"
          />
        </button>
      </div>
    </div>

    <!-- Modal that will show the event selected -->
    <EventModal
      v-if="showEventModal"
      :event="selectedEvent"
      @close="closeModal"
      @leave="leaveEvent"
      @attend="attendEvent"
      @checkIn="checkInEvent"
      @viewOnMap="drawEventRoute"
      @delete="deleteEvent"
      @start="startEvent"
      @update="updateEvent"
      @finish="finishEvent"
    />

    <!-- FilterModal listens out for the filterEvents event -->
    <FilterModal
      v-if="showFilterModal"
      @reset="resetFilter"
      @filter="filterEvents"
      @close="showFilterModal = !showFilterModal"
    />

    <!-- Traffic Modal that displays the details of a specific traffic event -->
    <TrafficModal
      v-if="showTrafficModal"
      :traffic="selectedTraffic"
      @close="closeTrafficModal"
    />
  </div>
</template>

<script>
import FilterModal from '../components/event/FilterModal'
import Event from '@/store/models/event'
import User from '@/store/models/user'
import NotificationModel from '@/store/models/notification'
import Traffic from '@/store/models/traffic'
import ChatMessage from '@/store/models/chat_message'
import EventModal from '@/components/event/modal/EventModal'
import MapworksEmbed from '@/components/MapworksEmbed'
import { mapActions } from 'vuex'
import TrafficModal from '@/components/traffic/TrafficModal'

export default {
  name: 'Dashboard',
  components: {
    FilterModal,
    EventModal,
    TrafficModal,
    MapworksEmbed
  },
  data () {
    return {
      eventLayer: null,
      trafficLayer: null,
      map: null,
      showEventModal: false,
      showFilterModal: false,
      showTrafficModal: false,
      selectedEventId: null,
      selectedTrafficId: null,
      eventRoute: null,
      eventPoints: [],
      trafficPoints: [],
      locationLayer: null,
      filterValues: null,
      organiserLocationLayer: null,
      organiserLocationPoint: null,
      userLocationPoint: null,
      userLocationLayer: null
    }
  },
  beforeDestroy () {
    // Clean up events that were binded to in this component.
    this.map.off('navigation:stabilised')
    this.map.off('feature:onclick')

    // Clear all layer
    this.map.getTree().nodes().models.forEach((node) => {
      if (node && ((this.eventLayer && node.cid === this.eventLayer.cid) || (this.locationLayer && node.id === this.locationLayer.cid) ||
      (this.trafficLayer && node.id === this.trafficLayer.cid) || (this.organiserLocationLayer && node.id === this.organiserLocationLayer.cid) ||
      (this.userLocationLayer && node.id === this.userLocationLayer.cid))) {
        node.empty()
        node.remove()
      }
    })
  },
  watch: {
    $route (to, from) {
      if (to.hash) {
        const eventId = this.$route.hash.substring(1)
        if (eventId) {
          this.drawEventRoute(eventId)
        }
      }
    },
    events () {
      // Every time the events updates, draw each of their points
      if (this.map && this.map._isReady) {
        this.removePoints()
        this.events.forEach(event => {
          const point = this.map.createPoint(event.starting_location.coordinates[0], event.starting_location.coordinates[1], this.eventLayer)
          point.setFields({
            event_id: event.event_id
          })
          this.eventPoints.push(point)
        })

        this.eventLayer.redraw()
      }
    },
    trafficEvents () {
      // Every time the traffic events update, redraw each of the points.
      if (this.map && this.map._isReady) {
        this.removeTrafficPoints()
        this.trafficEvents.forEach(trafficEvent => {
          const point = this.map.createPoint(trafficEvent.coordinates.coordinates[1], trafficEvent.coordinates.coordinates[0], this.trafficLayer)
          point.setFields({
            traffic_id: trafficEvent.traffic_id
          })
          this.trafficPoints.push(point)
        })

        this.trafficLayer.redraw()
      }
    },
    organiserLocation (value) {
      if (this.map && this.map._isReady) {
        if (value) {
          const { latitude, longitude } = value
          if (this.organiserLocationPoint) {
            this.organiserLocationPoint.setCoordinates(longitude, latitude)
            this.organiserLocationLayer.redraw()
          } else {
            this.organiserLocationPoint = this.map.createPoint(longitude, latitude, this.organiserLocationLayer)
            this.organiserLocationLayer.redraw()
          }
        } else {
          this.organiserLocationPoint.remove()
          this.organiserLocationLayer.redraw()
        }
      }
    },
    userLocation (value) {
      if (this.map && this.map._isReady && value) {
        if (value) {
          const { latitude, longitude } = value
          if (this.userLocationPoint) {
            this.userLocationPoint.setCoordinates(longitude, latitude)
            this.userLocationLayer.redraw()
          } else {
            this.userLocationPoint = this.map.createPoint(longitude, latitude, this.userLocationLayer)
            this.userLocationLayer.redraw()
          }
        } else {
          this.userLocationPoint.remove()
          this.userLocationLayer.redraw()
        }
      }
    }
  },
  computed: {
    durationValue: {
      get () {
        return Event.getters('getDuration')
      },
      set (value) {
        Event.dispatch('setDuration', value)
      }
    },
    distanceValue: {
      get () {
        return Event.getters('getDistance')
      },
      set (value) {
        Event.dispatch('setDistance', value)
      }
    },
    speedValue: {
      get () {
        return Event.getters('getSpeed')
      },
      set (value) {
        Event.dispatch('setSpeed', value)
      }
    },
    selectedEvent () {
      return Event.query().with(['organiser', 'participants', 'weather']).find(this.selectedEventId)
    },
    selectedTraffic () {
      return Traffic.find(this.selectedTrafficId)
    },
    events () {
      if (this.durationValue == null || this.distanceValue == null || this.speedValue == null) {
        return Event.all()
      } else {
        return Event.query()
          .where('duration', (value) => value >= (this.durationValue[0] * 3600) && value <= (this.durationValue[1] * 3600))
          .where('distance', (value) => value >= (this.distanceValue[0] * 1000) && value <= (this.distanceValue[1] * 1000))
          .where('average_speed', (value) => value >= this.speedValue[0] && value <= this.speedValue[1])
          .get()
      }
    },
    trafficEvents () {
      return Traffic.all()
    },
    organiserLocation () {
      return Event.getters('organiserLocation')
    },
    userLocation () {
      return User.getters('getLocation')
    },
    currentEvent () {
      return Event.getters('getCurrentEvent')
    }
  },
  methods: {
    resetFilter () {
      this.distanceValue = null
      this.durationValue = null
      this.speedValue = null
    },
    filterEvents (filterValues) {
      this.distanceValue = filterValues.distanceValue
      this.durationValue = filterValues.durationValue
      this.speedValue = filterValues.speedValue
    },
    ...mapActions({
      watchLocation: 'map/watchLocation',
      clearWatcher: 'map/clearWatcher',
      getLocation: 'map/getLocation'
    }),
    loadMapworks () {
      // Get mapworks instance from window
      this.map = window.map

      // Create layer for events with event_id field
      this.eventLayer = new Studio.core.entity.TreeVectorLayerEntity({
        visible: true,
        title: 'Events'
      }, { map: this.map })

      this.eventLayer.setFields([{
        name: 'event_id',
        title: 'event_id',
        type: Studio.core.entity.LayerFieldEntity.TypeMap.VARCHAR
      }])

      // Create layer for traffic events with traffic_id field.
      this.trafficLayer = new Studio.core.entity.TreeVectorLayerEntity({
        visible: true,
        title: 'Traffic'
      }, { map: this.map })

      this.trafficLayer.setFields([{
        name: 'traffic_id',
        title: 'traffic_id',
        type: Studio.core.entity.LayerFieldEntity.TypeMap.VARCHAR
      }])

      // Style icons and lines
      const layerStyles = new Studio.core.entity.LayerStylesEntity({
        myStyle: {
          default: {
            pointWidth: 20,
            pointFill: '#FF7F50',
            pointLineWidth: 1,
            pointLineFill: '#FF0000',
            pointIcon: `${process.env.MIX_APP_URL || 'http://localhost:8080'}/static/application/images/map-marker-icon.png`,
            polygonOpacity: 0.5,
            lineWidth: [2],
            lineFill: '#0000CD',
            polygonFill: '#00FA9A'
          }
        }
      })

      const trafficLayerStyles = new Studio.core.entity.LayerStylesEntity({
        myStyle: {
          default: {
            pointWidth: 20,
            pointFill: '#FF7F50',
            pointLineWidth: 1,
            pointLineFill: '#FF0000',
            pointIcon: `${process.env.MIX_APP_URL || 'http://localhost:8080'}/static/application/images/traffic-marker.png`,
            polygonOpacity: 0.5,
            lineWidth: [2],
            lineFill: '#0000CD',
            polygonFill: '#00FA9A'
          }
        }
      })

      // Set the style and add layer
      this.eventLayer.setStyles(layerStyles)
      this.map.getTree().add(this.eventLayer)

      // Set the style and add layer for traffic markers.
      this.trafficLayer.setStyles(trafficLayerStyles)
      this.map.getTree().add(this.trafficLayer)

      // On event clicks, set selectedEventId and show modal
      this.map.listenTo(this.map, 'feature:mouseclick', (mouseClickEvent) => {
        const feature = mouseClickEvent.getFeature()
        if (feature && feature.attributes.layer.cid === this.eventLayer.cid) {
          this.selectedEventId = feature.attributes.fields.event_id
          this.showEventModal = true
        } else if (feature && feature.attributes.layer.cid === this.trafficLayer.cid) {
          this.selectedTrafficId = feature.attributes.fields.traffic_id
          feature.zoom().then(() => {
            this.showTrafficModal = true
          })
        }
      })

      // When map pan stops, get bounding box and request nearby events
      this.map.listenTo(this.map, 'navigation:stabilised', (ev) => {
        const coords = ev.getEnd()._bounds.megaCast.c
        const sw = [
          coords[0],
          coords[1]
        ]
        const ne = [
          coords[2],
          coords[3]
        ]
        // Remove nearby for previous bounding box excluding the selected event, then request next set
        Event.dispatch('removeNearby', [this.selectedEventId]).then(() => {
          Event.dispatch('getNearbyBox', { ne, sw })
        })

        Traffic.dispatch('removeNearbyTraffic', { selected_id: this.selectedTrafficId }).then(() => {
          Traffic.dispatch('getTraffic', { ne, sw })
        })
      })

      // Draw initial pointers for events that are in state already.
      this.events.forEach(event => {
        const point = this.map.createPoint(event.starting_location.coordinates[0], event.starting_location.coordinates[1], this.eventLayer)
        point.setFields({
          event_id: event.event_id
        })
        this.eventPoints.push(point)
      })

      // Draw intial points for traffic events that are in state already.
      this.trafficEvents.forEach(trafficEvent => {
        const point = this.map.createPoint(trafficEvent.coordinates.coordinates[1], trafficEvent.coordinates.coordinates[0], this.trafficLayer)
        point.setFields({
          traffic_id: trafficEvent.traffic_id
        })
        this.trafficPoints.push(point)
      })

      // If there is an event ID hash in the url, then draw the route for it.
      if (this.$route.hash) {
        const eventId = this.$route.hash.substring(1)
        if (eventId) {
          this.drawEventRoute(eventId)
        }
      }

      // Organiser location layer
      this.organiserLocationLayer = new Studio.core.entity.TreeVectorLayerEntity({
        visible: true,
        title: 'Organiser Location'
      }, { map: this.map })

      const organiserLocationStyles = new Studio.core.entity.LayerStylesEntity({
        myStyle: {
          default: {
            pointWidth: 20,
            pointFill: '#FF0000',
            pointLineWidth: 1,
            pointLineFill: '#FF0000',
            polygonOpacity: 0.5,
            lineWidth: [2],
            lineFill: '#0000CD',
            polygonFill: '#00FA9A'
          }
        }
      })

      // Set the style and add layer
      this.organiserLocationLayer.setStyles(organiserLocationStyles)
      this.map.getTree().add(this.organiserLocationLayer)

      // User location layer
      this.userLocationLayer = new Studio.core.entity.TreeVectorLayerEntity({
        visible: true,
        title: 'Organiser Location'
      }, { map: this.map })

      const userLocationStyles = new Studio.core.entity.LayerStylesEntity({
        myStyle: {
          default: {
            pointWidth: 20,
            pointFill: '#0022CC',
            pointLineWidth: 1,
            pointLineFill: '#0022CC'
          }
        }
      })

      // Set the style and add layer
      this.userLocationLayer.setStyles(userLocationStyles)
      this.map.getTree().add(this.userLocationLayer)

      // Set the initial location for Mapworks.
      if (this.userLocation) {
        this.map.setViewCenter(this.userLocation.longitude, this.userLocation.latitude, 30000)
        this.userLocationPoint = this.map.createPoint(this.userLocation.longitude, this.userLocation.latitude, this.userLocationLayer)
      } else {
        this.map.setViewCenter(115.85541616994009, -31.954543192882383, 30000)
      }
    },
    updateEvent (eventId) {
      this.$router.push({ name: 'PlanARoute', hash: `#${eventId}` })
    },
    startEvent (eventId) {
      Event.dispatch('startEvent', eventId).then(() => {
        window.swal.fire({
          title: 'Event started!',
          icon: 'success',
          confirmButtonText: 'Okay'
        }).then(() => {
          NotificationModel.dispatch('requestNotificationPermission').then(() => {
            this.watchLocation({
              callback (latitude, longitude) {
                console.log('broadcasting location', { latitude, longitude, event_id: eventId })
                User.dispatch('broadcastLocation', { latitude, longitude, event_id: eventId })
                User.dispatch('setLocation', { latitude, longitude })
              },
              swalConfig: {
                title: 'Would you like to enable location tracking?',
                icon: 'question',
                showDenyButton: true,
                confirmButtonText: 'Yes',
                denyButtonText: 'No.'
              }
            })
          })
        })
      }).catch((error) => {
        console.log(error)
        window.swal.fire({
          title: 'Failed to start event!',
          text: error.data.error,
          icon: 'error',
          confirmButtonText: 'Okay'
        })
      })
    },
    finishEvent (eventId) {
      Event.dispatch('finishEvent', eventId)
      this.clearWatcher()
    },
    deleteEvent (eventId) {
      this.showEventModal = false
      Event.dispatch('deleteEvent', eventId)
    },
    leaveEvent (eventId) {
      Event.dispatch('leaveEvent', eventId).then(({ event: [event] }) => {
        ChatMessage.delete((message) => {
          return message.event_id === event.event_id
        })
      })
    },
    attendEvent (eventId) {
      Event.dispatch('attendEvent', eventId).then(({ event: [event] }) => {
        ChatMessage.dispatch('getMessagesForEvent', { eventId: event.event_id })
      })
    },
    checkInEvent (eventId) {
      Event.dispatch('checkInEvent', eventId).then(() => {
        User.dispatch('setHasShownDistanceAlert', true)
      })
    },
    closeModal () {
      this.showEventModal = false
      this.selectedEventId = null
    },
    closeTrafficModal () {
      this.showTrafficModal = false
      this.selectedTrafficId = null
    },
    removePoints () {
      this.eventPoints.forEach(point => {
        point.removeFromLayer()
      })
      this.eventLayer.redraw()
    },
    removeTrafficPoints () {
      this.trafficPoints.forEach(point => {
        point.removeFromLayer()
      })
      this.trafficLayer.redraw()
    },
    drawEventRoute (eventId) {
      const event = Event.find(eventId)
      if (event) {
        if (this.eventRoute) {
          this.eventRoute.removeFromLayer()
        }
        const [x, y] = event.route_coordinates.coordinates[0]
        this.showEventModal = false
        this.map.setViewCenter(x, y, 30000)
        this.map.panTo(x, y)
        this.eventRoute = this.map.createPolyline(event.xCoordinates, event.yCoordinates, event.route_coordinates.coordinates.length, this.eventLayer)
        this.eventLayer.redraw()
      } else {
        Event.dispatch('getEventDetails', eventId).then((details) => {
          // getEventDetails will return { user: [], event: []}
          // destructure return value to get the event
          const { event: [event] } = details
          if (this.eventRoute) {
            this.eventRoute.removeFromLayer()
          }
          const [x, y] = event.route_coordinates.coordinates[0]
          this.showEventModal = false
          this.map.panTo(x, y)
          this.eventRoute = this.map.createPolyline(event.xCoordinates, event.yCoordinates, event.route_coordinates.coordinates.length, this.eventLayer)
          this.eventLayer.redraw()
        })
      }
    },
    getUserLocation () {
      this.getLocation({
        callback: (latitude, longitude) => {
          this.map.setViewCenter(longitude, latitude, 30000)
          this.userLocationPoint = this.map.createPoint(longitude, latitude, this.userLocationLayer)
          this.userLocationLayer.redraw()
        },
        error: () => {
          this.map.setViewCenter(115.85541616994009, -31.954543192882383, 30000)
        },
        swalConfig: {
          title: 'Go to current location?',
          icon: 'question',
          confirmButtonText: 'Okay',
          showCancelButton: true,
          showCloseButton: true
        }
      })
    }
  }
}
</script>
