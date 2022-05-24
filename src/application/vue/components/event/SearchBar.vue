<template>
  <div class="relative w-96 right-0 mr-4">
    <div class="relative flex items-center bg-white text-gray-400 sm:shadow-md h-full rounded">
      <div class="absolute w-full top-3 flex justify-between sm:static">
        <AppTextInput
          :input-type="'text'"
          :input-name="'search'"
          :placeholder="'Search...'"
          :debounce="100"
          @enter="searchForEvents"
          v-model="searchText"
          :base-errorless-classes="['text-lg', 'ml-4', 'bg-transparent', 'h-full', 'leading-none', 'focus:outline-none']"
          ref="search"
        />

        <button
          class="right-0 mr-1 hidden sm:block"
        >
          <!-- Clear Icon -->
          <svg-vue
            icon="navigation/clear-icon"
            class="h-6 w-6"
          />
        </button>

        <button
          @click="$emit('close')"
          class="right-0 mr-1 sm:hidden"
        >
          <!-- Close Icon -->
          <svg-vue
            icon="navigation/close-icon"
            class="h-6 w-6"
          />
        </button>
      </div>
    </div>

    <SearchBarDropDown
      v-if="events.length"
      :events="events"
      @select="selectEvent"
    />
  </div>
</template>

<script>
import Event from '@/store/models/event'
import SearchBarDropDown from './SearchBarDropDown'

export default {
  name: 'SearchBar',
  components: {
    SearchBarDropDown
  },
  data () {
    return {
      searchText: '',
      events: []
    }
  },
  methods: {
    focusInput () {
      this.$refs.search.focus()
    },
    searchForEvents () {
      Event.dispatch('searchEvents', { query: this.searchText }).then((events) => {
        this.events = events
      }).catch(() => {
        this.searchText = ''
        window.swal.fire({
          title: 'It looks like there was an error processing your search results!',
          text: 'Please retry with a different query',
          icon: 'info',
          confirmButtonText: 'Okay'
        })
      })
    },
    selectEvent (eventId) {
      this.events = []
      if (Event.find(eventId)) {
        this.$emit('selectEvent', eventId)
      } else {
        Event.dispatch('getEventDetails', eventId).then(() => {
          this.$emit('selectSearched', eventId)
        })
      }
    }
  },
  watch: {
    searchText () {
      if (this.searchText.length > 3) this.searchForEvents()
      // Might add notification for length to be greater than 3.
    }
  }
}
</script>
