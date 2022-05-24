<template>
  <div>
    <div
      class="relative h-screen flex"
    >
      <!-- Toggle sidebar when show is emitted. -->
      <Navbar
        @show="show = !show"
        @close="show = false"
      />
      <transition
        name="slide-menu"
        enter-active-class="animate__animated animate__slideInLeft animate__faster"
        leave-active-class="animate__animated animate__slideOutLeft animate__faster"
      >
        <!-- Display the sidebar if the show property is true. -->
        <Sidebar
          v-if="show"
          @close="closeSidebar"
        />
      </transition>
      <div
        v-if="this.$isMobile() && show"
        class="absolute h-screen w-screen bottom-0 left-0 z-10"
        @click.prevent="show = false"
      />
      <!-- Display vue component for route. -->
      <router-view class="overflow-y-auto w-screen" />
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/navigation/Navbar'
import Sidebar from '@/components/navigation/Sidebar'

export default {
  name: 'App',
  data () {
    return {
      show: false
    }
  },
  components: {
    Navbar,
    Sidebar
  },
  methods: {
    closeSidebar () {
      if (this.$isMobile()) {
        this.show = false
      }
    }
  },
  created () {
    // if on desktop, set show to true, if on mobile set show to false
    this.show = !this.$isMobile()
  }
}
</script>
