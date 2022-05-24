<template>
  <div
    class="h-12 fixed font-bold leading-none w-full z-50 text-gray-400 bg-rwmLighterBlue sm:hidden"
  >
    <!-- Toggle whole div containing text and buttons -->
    <div
      v-if="!show"
      class="flex justify-between items-center h-12 fixed font-bold leading-none w-full"
    >
      <!-- Menu button -->
      <button
        type="button"
        class="cursor-pointer rounded ml-3 mr-3 text-white hover:bg-rwmDarkBlue hover:bg-opacity-50 focus:outline-none lg:hidden "
        @click="$emit('show')"
      >
        <svg-vue
          icon="navigation/menu-icon"
          class="h-6 w-6 text-white"
        />
      </button>

      <h1 class="text-white">
        {{ $route.meta.name ? $route.meta.name : 'Dashboard' }}
      </h1>

      <!-- Search button -->
      <button
        @click="showSearchBar"
        class="text-white mr-3 ml-3"
      >
        <svg-vue
          icon="navigation/search-icon"
          class="h-4 w-4 text-white"
        />
      </button>
    </div>
    <!-- Animation for close and open. -->
    <transition
      name="slide-menu"
      enter-active-class="animate__animated animate__slideInRight animate__faster"
      leave-active-class="animate__animated animate__slideOutRight animate__faster"
    >
      <SearchBar
        v-if="show"
        ref="searchBar"
        class="h-full w-screen"
        @selectEvent="selectEvent"
        @selectSearched="selectEvent"
        @close="show = !show"
      />
    </transition>
  </div>
</template>

<script>
import SearchBar from '../event/SearchBar'

export default {
  name: 'Navbar',
  components: {
    SearchBar
  },
  data () {
    return {
      show: false
    }
  },
  methods: {
    showSearchBar () {
      this.show = !this.show
      this.$emit('close', false)
      if (this.show) {
        this.$nextTick(() => {
          this.$refs.searchBar.focusInput()
        })
      }
    },
    selectEvent (eventId) {
      this.show = false
      if (this.$route.name === 'Events') {
        if (this.$route.hash.substring(1) !== eventId) {
          this.$router.replace({ hash: `#${eventId}` })
        }
      } else {
        this.$router.push({ name: 'Events', hash: `#${eventId}` })
      }
    }
  }
}
</script>
