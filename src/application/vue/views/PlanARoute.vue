<template>
  <!-- Container for Mapworks. -->
  <div class="relative">
    <!-- Component to enter event details. -->
    <CreateEventModal
      v-if="showCreateEventModal"
      :event="selectedEvent"
      @draw="hideInputModal"
      @close="$router.push({ name: 'Dashboard' })"
    />

    <div
      v-if="showDetailsButton"
      class="fixed bottom-0 flex justify-center w-screen z-10 left-0"
    >
      <button
        @click.prevent="showInputModal"
        type="button"
        class="w-screen sm:w-1/2 p-4 bg-white flex flex-row rounded-t space-x-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 15l7-7 7 7"
          />
        </svg>
        <div>
          Event details
        </div>
      </button>
    </div>

    <MapworksEmbed
      @ready="loadMapworks"
      ref="mapworks"
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
import CreateEventModal from '@/components/event/create-event-modal/CreateEventModal'
import Event from '@/store/models/event'
import MapworksEmbed from '@/components/MapworksEmbed'
import TrafficModal from '@/components/traffic/TrafficModal'
import Traffic from '@/store/models/traffic'

export default {
  name: 'PlanARoute',
  components: {
    CreateEventModal,
    MapworksEmbed,
    TrafficModal
  },
  data () {
    return {
      map: null,
      showCreateEventModal: false,
      showDetailsButton: false,
      showTrafficModal: false,
      selectedEvent: null,
      selectedTrafficId: null,
      trafficLayer: null,
      routeLayer: null,
      routeLine: null,
      lineId: 0,
      xCoords: [],
      yCoords: [],
      points: [],
      trafficPoints: [],
      pointId: 0
    }
  },
  computed: {
    routeCoordinates: {
      get () {
        return Event.getters('getNewEvent').route_coordinates
      },
      set (value) {
        Event.dispatch('updateNewEvent', { routeCoordinates: value })
      }
    },
    startingLocation: {
      get () {
        return Event.getters('getNewEvent').starting_location
      },
      set (value) {
        Event.dispatch('updateNewEvent', { startingLocation: value })
      }
    },
    selectedTraffic () {
      return Traffic.find(this.selectedTrafficId)
    },
    trafficEvents () {
      return Traffic.all()
    }
  },
  beforeDestroy () {
    // Clean up events that were binded to in this component.
    this.map.off('navigation:stabilised')
    this.map.off('feature:mouseclick')

    // Clear route layer and traffic layer.
    this.map.getTree().nodes().models.forEach((node) => {
      if (node && ((this.routeLayer && node.cid === this.routeLayer.cid) || (this.trafficLayer && node.id === this.trafficLayer.cid))) {
        node.empty()
        node.remove()
      }
    })
  },
  mounted () {
    if (this.$route.hash) {
      const eventId = this.$route.hash.substring(1)
      if (eventId) {
        const hashEvent = Event.find(eventId)
        if (hashEvent) {
          this.selectedEvent = hashEvent
          Event.dispatch('setNewEvent', hashEvent)
          const time = hashEvent.startingTimeDate
          const month = `${time.getMonth() + 1}`.padStart(2, '0')
          const day = `${time.getDate()}`.padStart(2, '0')
          const hour = `${time.getHours()}`.padStart(2, '0')
          const minute = `${time.getMinutes()}`.padStart(2, '0')
          const dateTimeString = `${time.getFullYear()}-${month}-${day}T${hour}:${minute}`
          Event.dispatch('updateNewEvent', { starting_time: dateTimeString })
        }
      }
    } else {
      Event.dispatch('resetNewEvent')
      Event.dispatch('resetErrors')
    }

    this.$nextTick(() => {
      this.showCreateEventModal = true
    })
  },
  watch: {
    routeCoordinates (value) {
      // Every time the event updates, draw each of their points
      if (this.map && this.map._isReady) {
        this.points.forEach((point) => {
          point.removeFromLayer()
        })

        this.xCoords = []
        this.yCoords = []
        this.points = []

        this.routeCoordinates.coordinates.forEach((coordinates) => {
          this.xCoords.push(coordinates[0])
          this.yCoords.push(coordinates[1])

          const point = this.map.createPoint(coordinates[0], coordinates[1], this.routeLayer)

          this.pointId++
          point.setFields({
            point_id: this.pointId
          })
          this.points.push(point)
        })

        this.drawRouteLine()
        this.routeLayer.redraw()
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
    }
  },
  methods: {
    hideInputModal () {
      this.showDetailsButton = true
      this.showCreateEventModal = false
    },
    showInputModal () {
      this.showDetailsButton = false
      this.showCreateEventModal = true
    },
    loadMapworks () {
      // Get mapworks instance from window
      this.map = window.map
      this.map.setViewCenter(115.85541616994009, -31.954543192882383, 30000)

      this.routeLayer = new Studio.core.entity.TreeVectorLayerEntity({
        visible: true,
        title: 'Route Layer'
      }, { map: this.map })

      this.routeLayer.setFields([{
        name: 'point_id',
        title: 'point_id',
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
            pointFill: '#000000',
            pointLineWidth: 1,
            pointLineFill: '#FF0000',
            polygonOpacity: 0.5,
            lineWidth: [5],
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

      // Set the style and add layer for route line and markers.
      this.routeLayer.setStyles(layerStyles)
      this.map.getTree().add(this.routeLayer)

      // Set the style and add layer for traffic markers.
      this.trafficLayer.setStyles(trafficLayerStyles)
      this.map.getTree().add(this.trafficLayer)

      this.routeCoordinates.coordinates.forEach((coordinates) => {
        this.xCoords.push(coordinates[0])
        this.yCoords.push(coordinates[1])
        const point = this.map.createPoint(coordinates[0], coordinates[1], this.routeLayer)
        this.pointId++
        point.setFields({
          point_id: this.pointId
        })
        this.points.push(point)
      })

      this.drawRouteLine()

      this.map.listenTo(this.map, 'feature:mouseclick', (mouseClickEvent) => {
        const feature = mouseClickEvent.getFeature()
        const coordinates = this.map.getCoordinates(mouseClickEvent.getX(), mouseClickEvent.getY(), false)

        if (feature && feature.attributes.layer.cid === this.trafficLayer.cid) {
          this.selectedTrafficId = feature.attributes.fields.traffic_id
          feature.zoom().then(() => {
            this.showTrafficModal = true
          })
        } else if (feature && feature.attributes.fields.point_id) {
          feature.removeFromLayer()
          const index = this.points.findIndex(point => point.attributes.fields.point_id === feature.attributes.fields.point_id)
          this.xCoords.splice(index, 1)
          this.yCoords.splice(index, 1)
          this.points.splice(index, 1)
          Event.dispatch('removeFromNewRouteCoordinates', { index }).then(() => {
            if (this.routeCoordinates.coordinates.length === 0) {
              this.startingLocation.coordinates = []
            }
          })

          this.drawRouteLine()
        } else if (mouseClickEvent.getFeature() && mouseClickEvent.getFeature().id === this.lineId) {
          const xPixel = mouseClickEvent.getX()
          const yPixel = mouseClickEvent.getY()
          const x = coordinates[0]
          const y = coordinates[1]
          let index = -1
          // determine which pair of points the new point is inserted between
          for (let i = 0; i < this.xCoords.length - 1; i++) {
            const startCoord = [this.xCoords[i], this.yCoords[i]]
            const endCoord = [this.xCoords[i + 1], this.yCoords[i + 1]]
            const startPixelCoords = this.map.getCoordinates(startCoord[0], startCoord[1], true)
            const endPixelCoords = this.map.getCoordinates(endCoord[0], endCoord[1], true)
            // x goes left and right negative -> positive
            // y goes up and down negative -> positive
            // Determine the quadrant that the new coordinate is in
            const gtX = ((startPixelCoords[0] - 5) < xPixel && xPixel < (endPixelCoords[0] + 5))
            const gtY = ((startPixelCoords[1] + 5) > yPixel && yPixel > (endPixelCoords[1] - 5))
            const ltX = ((startPixelCoords[0] + 5) > xPixel && xPixel > (endPixelCoords[0] - 5))
            const ltY = ((startPixelCoords[1] - 5) < yPixel && yPixel < (endPixelCoords[1] + 5))
            if (endCoord[0] > startCoord[0] && endCoord[1] > startCoord[1]) {
              if (gtX && gtY) {
                if (index < i) {
                  index = i
                }
              }
            } else if (endCoord[0] < startCoord[0] && endCoord[1] < startCoord[1]) {
              if (ltX && ltY) {
                if (index < i) {
                  index = i
                }
              }
            } else if (endCoord[0] > startCoord[0] && endCoord[1] < startCoord[1]) {
              if (gtX && ltY) {
                if (index < i) {
                  index = i
                }
              }
            } else if (endCoord[0] < startCoord[0] && endCoord[1] > startCoord[1]) {
              if (ltX && gtY) {
                if (index < i) {
                  index = i
                }
              }
            }
          }
          if (index !== -1) {
            this.xCoords.splice(index + 1, 0, x)
            this.yCoords.splice(index + 1, 0, y)
            const point = this.map.createPoint(coordinates[0], coordinates[1], this.routeLayer)

            Event.dispatch('insertNewRouteCoordinates', { coordinates: [coordinates[0], coordinates[1]], index: index + 1 })

            this.pointId++
            point.setFields({
              point_id: this.pointId
            })
            this.points.splice(index + 1, 0, point)
          }
        } else {
          this.xCoords.push(coordinates[0])
          this.yCoords.push(coordinates[1])
          const point = this.map.createPoint(coordinates[0], coordinates[1], this.routeLayer)
          Event.dispatch('addNewRouteCoordinates', [coordinates[0], coordinates[1]])

          if (this.startingLocation.coordinates.length === 0) {
            this.startingLocation.coordinates = [coordinates[0], coordinates[1]]
          }

          this.pointId++
          point.setFields({
            point_id: this.pointId
          })
          this.points.push(point)
        }
        if (this.xCoords.length > 1) {
          this.drawRouteLine()
        }
        this.routeLayer.redraw()
      })

      // When map pan stops, get bounding box and request nearby traffic.
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
        // Remove nearby traffic for previous bounding box excluding the next set of traffic events.
        Traffic.dispatch('removeNearbyTraffic', { selected_id: this.selectedTrafficId }).then(() => {
          Traffic.dispatch('getTraffic', { ne, sw })
        })
      })

      // Draw intial points for traffic events that are in state already
      this.trafficEvents.forEach(trafficEvent => {
        const point = this.map.createPoint(trafficEvent.coordinates.coordinates[1], trafficEvent.coordinates.coordinates[0], this.trafficLayer)
        point.setFields({
          traffic_id: trafficEvent.traffic_id
        })
        this.trafficPoints.push(point)
      })

      // If there is an event ID hash in the url, then draw the route for it
      if (this.$route.hash) {
        const eventId = this.$route.hash.substring(1)
        if (eventId) {
          const hashEvent = Event.find(eventId)
          if (hashEvent) {
            this.selectedEvent = hashEvent
          }
        }
        this.showCreateEventModal = true
      }
    },
    drawRouteLine () {
      if (this.routeLine) {
        this.routeLine.removeFromLayer()
      }
      this.routeLine = this.map.createPolyline(this.xCoords, this.yCoords, this.xCoords.length, this.routeLayer)
      this.lineId = this.routeLine.id
    },
    closeTrafficModal () {
      this.showTrafficModal = false
      this.selectedTrafficId = null
    },
    removeTrafficPoints () {
      this.trafficPoints.forEach(point => {
        point.removeFromLayer()
      })
      this.trafficLayer.redraw()
    }
  }
}
</script>
