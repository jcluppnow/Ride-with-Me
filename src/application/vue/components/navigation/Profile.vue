<template>
  <!-- Main container for profile information. -->
  <div class="bg-rwmLighterBlue flex items-center absolute bottom-0 h-15 py-2 w-full">
    <!-- Div for image. -->
    <div class="pl-3">
      <!-- Vector asset for profile picture. Will change to load depending on if a
      profile picture is set. -->
      <!-- <svg-vue
        icon="navigation/sidebar/default-profile-icon"
        class="h-10 w-10"
      /> -->
      <img
        v-if="authenticated"
        class="h-10 w-10"
        :src="authenticatedUser.profile"
      >
      <svg-vue
        v-else
        icon="navigation/sidebar/default-profile-icon"
        class="h-10 w-10"
      />
    </div>

    <!-- Container to hold account information. -->
    <div class="pl-2 space-y-0 flex-grow leading-none">
      <!-- Container to hold account name. -->
      <div
        v-if="authenticated"
        class="pt-2 leading-none"
      >
        <!-- Default information for user. -->
        <span class="text-sm text-white">{{ authenticatedUser.full_name }}</span>
      </div>

      <!-- Container to hold router links for logout and account. -->
      <div class="flex items-center leading-none pb-2">
        <span v-if="authenticated">
          <!-- Router link to access account information for the logged in user. -->
          <router-link
            v-if="$isMobile()"
            class="cursor-pointer"
            :to="{ name: 'Account', params: {} }"
          >
            <!-- Router link title. -->
            <span class="text-xs text-gray-300">My Account</span>
          </router-link>
          <button
            v-else
            @click.prevent="showModal = true"
          >
            <!-- Router link title. -->
            <span class="text-xs text-gray-300">My Account</span>
          </button>
        </span>
        <a
          v-else
          href="/accounts/register/"
        >
          <!-- Router link title. -->
          <span class="text-xs text-gray-300 hover:text-#FCA311">Register</span>
        </a>

        <!-- Divider vector between router links. -->
        <svg-vue
          icon="navigation/sidebar/profile-divider-icon"
          class="h-1.5 w-1.5 mx-1 mt-1 fill-current text-gray-300"
        />

        <!-- Router link to log the current user out. -->
        <router-link
          v-if="authenticated"
          class="cursor-pointer"
          :to="{ name: 'Logout', params: {} }"
        >
          <!-- Router link title. -->
          <span class="text-xs text-gray-300 hover:text-#FCA311">Logout</span>
        </router-link>

        <!-- Router link to log the current user out. -->
        <a
          v-else
          href="/accounts/login/"
        >
          <!-- Router link title. -->
          <span class="text-xs text-gray-300 hover:text-#FCA311">Login</span>
        </a>
      </div>
    </div>

    <ProfileModal
      v-if="showModal"
      @close="showModal = false"
    />
  </div>
</template>

<script>
import ProfileModal from './ProfileModal'
import User from '@/store/models/user'

export default {
  name: 'Profile',
  components: {
    ProfileModal
  },
  data () {
    return {
      showModal: false,
      name: 'Tim Mellows'
    }
  },
  computed: {
    authenticatedUser () {
      return User.getters('authenticatedUser')
    },
    authenticated () {
      return User.getters('isAuthenticated')
    }
  }
}
</script>
