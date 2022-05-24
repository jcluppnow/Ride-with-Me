<template>
  <!-- Container for the whole sidebar. -->
  <div
    class="z-40 bg-rwmDarkBlue w-60 py-4 fixed inset-y-0 left-0 bottom-0 sm:w-72 sm:space-y-6 sm:relative"
  >
    <!-- Container for Ride with Me Header and Image. -->
    <div class="text-white flex justify-center space-x-2 mt-9 w-full sm:mt-0">
      <!-- Bike vector. -->
      <svg-vue
        icon="navigation/sidebar/bike-icon"
        class="h-8 w-8"
      />

      <!-- Application title. -->
      <span class="text-2xl font-bold">Ride with Me</span>
    </div>

    <!-- Container for route-link elements to navigate SPA. -->
    <div class="mt-1">
      <!-- List of all route links. -->
      <ul
        class="text-gray-300 px-2 sm:px-4"
        @click.prevent="$emit('close')"
      >
        <!-- List element for access to the Dashboard page. -->
        <router-link
          class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white rounded"
          tag="li"
          active-class="bg-rwmOrange text-white"
          exact-path
          :to="{ name: 'Dashboard', params: {} }"
        >
          <!-- Home vector to represent Dashboard. -->
          <svg-vue
            icon="navigation/sidebar/home-icon"
            class="transition duration-200 group-hover:text-white h-6 w-6"
          />

          <!-- Sidebar item title. -->
          <span>Dashboard</span>
        </router-link>

        <!-- List element for access to the Events page. -->
        <router-link
          v-if="authenticated"
          class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white rounded"
          tag="li"
          active-class="bg-rwmOrange text-white"
          exact-path
          :to="{ name: 'Events', params: {} }"
        >
          <!-- Calendar vector to represent Events. -->
          <svg-vue
            icon="navigation/sidebar/calendar-icon"
            class="group-hover:text-white h-6 w-6"
          />

          <!-- Sidebar item title. -->
          <span>Events</span>
        </router-link>

        <!-- List element for access to the Plan a route page. -->
        <router-link
          v-if="authenticated"
          class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white rounded"
          tag="li"
          active-class="bg-rwmOrange text-white"
          exact-path
          :to="{ name: 'PlanARoute', params: {} }"
        >
          <!-- Add vector to represent planning a route. -->
          <svg-vue
            icon="navigation/sidebar/add-icon"
            class="group-hover:text-white h-6 w-6"
          />

          <!-- Sidebar item title. -->
          <span>Plan a route</span>
        </router-link>

        <span v-if="authenticated">
          <!-- List element for access to the Chat page. -->
          <router-link
            v-if="$isMobile()"
            class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white active:bg-rwmOrange active:text-white rounded"
            tag="li"
            active-class="bg-rwmOrange text-white"
            exact-path
            :to="{ name: 'MobileChatList' }"
          >
            <!-- Message vector to represent chat. -->
            <svg-vue
              icon="navigation/sidebar/message-icon"
              class="group-hover:text-white group-active:text-white h-6 w-6"
            />

            <!-- Sidebar item title. -->
            <span>Chat</span>
          </router-link>

          <!-- List element for access to the Chat page. -->
          <router-link
            v-else
            class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white active:bg-rwmOrange active:text-white rounded"
            tag="li"
            active-class="bg-rwmOrange text-white"
            exact-path
            :to="{ name: 'Chat' }"
          >
            <!-- Message vector to represent chat. -->
            <svg-vue
              icon="navigation/sidebar/message-icon"
              class="group-hover:text-white group-active:text-white h-6 w-6"
            />

            <!-- Sidebar item title. -->
            <span>Chat</span>
          </router-link>
        </span>

        <!-- List element for access to the Notifications page. -->
        <router-link
          v-if="authenticated"
          class="cursor-pointer group block py-2 px-2 flex items-center space-x-2 transition duration-200 hover:bg-rwmOrange hover:text-white rounded"
          tag="li"
          active-class="bg-rwmOrange text-white"
          exact-path
          :to="{ name: 'Notifications', params: {} }"
        >
          <!-- Bell vector to represent notifications. -->
          <svg-vue
            icon="navigation/sidebar/bell-icon"
            class="group-hover:text-white h-6 w-6"
          />

          <!-- Sidebar item title. -->
          <span>Notifications</span>
        </router-link>
      </ul>
    </div>

    <!-- Component for Login Information. -->
    <Profile />
  </div>
</template>

<script>
// Import Profile component.
import Profile from './Profile'
import User from '@/store/models/user'

export default {
  name: 'Sidebar',
  components: {
    Profile
  },
  computed: {
    authenticated () {
      return User.getters('isAuthenticated')
    }
  }
}
</script>
