<template>
  <div>
    <div class="ml-3 mt-3">
      <div class="flex justify-between mb-1">
        <div class="font-bold text-2xl text-gray-800 mt-10 sm:px-2 sm:mt-0">
          My Events
        </div>
        <SearchBar
          @selectEvent="selectEvent"
          @selectSearched="selectSearchedEvent"
          class="hidden sm:block h-8 rounded"
        />
      </div>
    </div>
    <EventList
      v-if="myEvents.length"
      :events="myEvents"
      @eventClicked="selectEvent"
    />
    <div
      v-else
      class="font-semibold ml-3 text-center"
    >
      You are not attending any events, you can attend an event by clicking on an event and clicking attend.
    </div>

    <div class="font-bold text-2xl text-gray-800 py-2 sm:px-2 ml-3">
      Near Me
      <button
        type="button"
        @click.prevent="getNearby"
      >
        <svg-vue
          icon="event/location"
          class="h-5 w-5 text-black"
        />
      </button>
    </div>
    <EventList
      v-if="nearbyEvents.length"
      :events="nearbyEvents"
      @eventClicked="selectEvent"
    />
    <div
      v-else
      class="font-semibold ml-3 text-center"
    >
      No nearby events found, you can search for nearby events in the dashboard.
    </div>

    <!-- <div class="font-bold text-2xl text-gray-800 py-2 sm:px-2 sm:ml-2">
      Social Rides
    </div>
    <EventList :events="events" /> -->

    <!-- Modal that will show the event selected -->
    <EventModal
      v-if="showModal && selectedEvent"
      :event="selectedEvent"
      @close="closeModal"
      @leave="leaveEvent"
      @attend="attendEvent"
      @checkIn="checkInEvent"
      @viewOnMap="goToEventRoute"
      @delete="deleteEvent"
      @start="startEvent"
      @update="updateEvent"
      @finish="finishEvent"
    />
  </div>
</template>

<script>
import EventList from '@/components/event/EventList'
import SearchBar from '@/components/event/SearchBar'
import EventModal from '@/components/event/modal/EventModal'
import Event from '@/store/models/event'
import NotificationModel from '@/store/models/notification'
import User from '@/store/models/user'
import ChatMessage from '@/store/models/chat_message'
import Weather from '@/store/models/weather'
import { mapActions } from 'vuex'

export default {
  name: 'Events',
  components: {
    EventList,
    SearchBar,
    EventModal
  },
  data () {
    return {
      showModal: false,
      selectedEventId: null,
      searchedEventId: null
    }
  },
  computed: {
    shownEventId () {
      return this.searchedEventId || this.selectedEventId
    },
    selectedEvent () {
      return Event.query().with(['organiser', 'participants', 'weather']).find(this.shownEventId)
    },
    myEvents () {
      return Event.getters('myEvents')(['organiser'])
    },
    nearbyEvents () {
      return Event.getters('nearbyEvents')(['organiser'], [this.searchedEventId])
    },
    debugEventModel () {
      return Event
    },
    debugUserModel () {
      return User
    },
    debugWeatherModel () {
      return Weather
    }
  },
  watch: {
    $route (to, from) {
      if (to.hash) {
        const eventId = this.$route.hash.substring(1)
        if (eventId) {
          this.selectedEventId = eventId
          this.showModal = true
        }
      }
    }
  },
  methods: {
    ...mapActions({
      watchLocation: 'map/watchLocation',
      getLocation: 'map/getLocation'
    }),
    closeModal () {
      this.showModal = false
      Event.delete(this.searchedEventId)
      this.searchedEventId = null
      this.selectedEventId = null
      this.$router.replace({})
    },
    goToEventRoute (eventId) {
      this.$router.push({ name: 'Dashboard', hash: `#${eventId}` })
    },
    selectSearchedEvent (eventId) {
      this.searchedEventId = eventId
      this.showModal = true
    },
    selectEvent (eventId) {
      this.selectedEventId = eventId
      this.showModal = true
    },
    updateEvent (eventId) {
      this.$router.push({ name: 'PlanARoute', hash: `#${eventId}` })
    },
    startEvent (eventId) {
      Event.dispatch('startEvent', eventId).then(() => {
        window.swal.fire({
          title: 'Event started!',
          text: 'Taking you to the dashboard.',
          icon: 'success',
          confirmButtonText: 'Okay'
        }).then(() => {
          this.$router.push({ name: 'Dashboard', hash: `#${eventId}` })
          NotificationModel.dispatch('requestNotificationPermission').then(() => {
            this.watchLocation({
              callback (latitude, longitude) {
                User.dispatch('broadcastLocation', { latitude, longitude, event_id: eventId })
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
    deleteEvent (eventId) {
      this.showModal = false
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
        User.dispatch('setHasShownDistanceAlert', false)
      })
    },
    finishEvent (eventId) {
      Event.dispatch('finishEvent', eventId)
    },
    getNearby () {
      this.getLocation({
        callback (latitude, longitude) {
          Event.dispatch('getNearbyLocation', { lat: latitude, lon: longitude })
        },
        swalConfig: {
          title: 'Get events around your current location?',
          icon: 'question',
          confirmButtonText: 'Okay',
          showCancelButton: true,
          showCloseButton: true
        }
      })
    }
  },
  beforeDestroy () {
    Event.delete(this.searchedEventId)
  },
  mounted () {
    if (this.$route.hash) {
      const eventId = this.$route.hash.substring(1)
      if (eventId) {
        this.selectEvent(eventId)
      }
    }
  }
}
</script>
