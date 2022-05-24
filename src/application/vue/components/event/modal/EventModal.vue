<template>
  <ModalLayout
    :external-classes="'w-screen'"
    @close="$emit('close')"
  >
    <template #header>
      <EventModalHeaderDetails
        :event="event"
        @update="$emit('update', event.event_id)"
        @delete="$emit('delete', event.event_id)"
        @showInfo="toggleInfo"
        @showParticipants="toggleParticipants"
      />
    </template>

    <template #body>
      <EventModalParticipantsDetails
        v-if="showParticipants"
        :event="event"
      />
      <EventModalDescriptionDetails
        v-else-if="!showInfo"
        :event="event"
      />
      <EventModalDetails
        v-else
        @viewOnMap="$emit('viewOnMap', event.event_id)"
        :event="event"
        class="w-full"
      />

      <div class="hidden sm:block sm:border-r border-gray-300 min-h-full" />

      <div class="hidden font-semibold text-gray-900 pl-4 sm:block w-max">
        <EventModalDetails
          @viewOnMap="$emit('viewOnMap', event.event_id)"
          :event="event"
        />
      </div>
    </template>

    <template #footer>
      <EventModalButtons
        :event="event"
        @leave="$emit('leave', event.event_id)"
        @attend="$emit('attend', event.event_id)"
        @checkIn="$emit('checkIn', event.event_id)"
        @start="$emit('start', event.event_id)"
        @finish="$emit('finish', event.event_id)"
      />
    </template>
  </modallayout>
</template>

<script>
import ModalLayout from '@/components/ModalLayout'
import EventModalButtons from './EventModalButtons'
import EventModalDetails from './EventModalDetails'
import EventModalHeaderDetails from './EventModalHeaderDetails'
import EventModalDescriptionDetails from './EventModalDescriptionDetails'
import EventModalParticipantsDetails from './EventModalParticipantsDetails'

export default {
  name: 'EventModal',
  components: {
    ModalLayout,
    EventModalButtons,
    EventModalDetails,
    EventModalHeaderDetails,
    EventModalDescriptionDetails,
    EventModalParticipantsDetails
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
      showInfo: false
    }
  },
  methods: {
    toggleInfo () {
      this.showParticipants = false
      this.showInfo = !this.showInfo
    },
    toggleParticipants () {
      this.showInfo = false
      this.showParticipants = !this.showParticipants
    }
  }
}
</script>
