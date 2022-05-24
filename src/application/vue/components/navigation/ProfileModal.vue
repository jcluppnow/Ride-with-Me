<template>
  <!-- Uses Modal Layout template. -->
  <ModalLayout @close="$emit('close')">
    <template #header>
      <h1 class="ml-2 mt-2 text-lg leading-tight font-semibold">
        Update Account Details
      </h1>
    </template>

    <!-- Body of template. -->
    <template #body>
      <div class="relative z-1">
        <div class="flex justify-center pt-3">
          <div class="relative">
            <img
              v-if="user"
              class="rounded-full h-28 w-28 shadow-lg"
              :src="user ? user.profile : ''"
              alt=""
            >
            <svg-vue
              v-else
              icon="navigation/sidebar/default-profile-icon"
              class="h-10 w-10"
            />
            <button
              class="absolute top-0 right-0 rounded-full bg-rwmOrange h-10 w-10 flex items-center"
              @click.prevent="$refs.profileInput.click()"
            >
              <svg-vue
                icon="navigation/sidebar/profile-icon"
                class="h-6 w-6 mx-auto"
              />
            </button>
            <!-- Button to upload photo. -->
            <input
              ref="profileInput"
              type="file"
              class="hidden"
              name="profile"
              @change="fileUploaded"
            >
            <AppFileInput
              class="w-full"
              cy="photoInput"
              @change="fileUploaded"
              :attributes="{ accept: 'image/png, image/jpeg, image/gif' }"
              :base-errorless-classes="['text-white', 'bg-rwmDarkBlue', 'hover:bg-rwmOrange', 'justify-center', 'absolute', 'top-0', 'right-0', 'rounded-full', 'bg-rwmOrange', 'h-10', 'w-10', 'flex', 'items-center']"
              :disable-br="true"
            >
              <template #button>
                <svg-vue
                  icon="navigation/sidebar/profile-icon"
                  class="h-6 w-6 mx-auto"
                />
              </template>
            </AppFileInput>
          </div>
        </div>

        <!-- Container for error or success messages on upload. -->
        <div class="flex flex-col items-center">
          <!-- Display user properties. -->
          <div class="mx-auto w-64">
            <div class="mt-3">
              Full Name
              <input
                id="username"
                type="text"
                class="block w-full h-8 py-1.5 px-3 text-base bg-white bg-clip-padding border border-solid rounded shadow-lg"
                name="username"
                placeholder="Username"
                v-model="user.full_name"
              >
            </div>
            <div class="mt-3">
              Email
              <input
                id="email"
                type="text"
                class="block w-full h-8 py-1.5 px-3 text-base bg-white bg-clip-padding border border-solid rounded shadow-lg"
                name="email"
                placeholder="Email"
                v-model="user.email"
              >
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Buttons to save or cancel changes. -->
    <template #footer>
      <div class="flex flex-col sm:flex-row m-4 space-x-2">
        <button
          class="w-1/2 bg-rwmDarkBlue hover:bg-rwmOrange text-white font-medium py-3 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
          type="button"
          @click.prevent="updateUserDetails"
        >
          Save
        </button>
        <button
          class="w-1/2 bg-rwmDarkBlue hover:bg-rwmOrange text-white font-medium py-3 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
          type="button"
          @click.prevent="$emit('close')"
        >
          Cancel
        </button>
      </div>
    </template>
  </ModalLayout>
</template>

<script>
import ModalLayout from '../ModalLayout'
import User from '@/store/models/user'

export default {
  name: 'ProfileModal',
  components: {
    ModalLayout
  },
  data () {
    return {
      user: null
    }
  },
  methods: {
    updateUserDetails () {
      User.dispatch('updateUserDetails', this.user).then(() => {
        this.user = User.getters('authenticatedUser')
        window.swal.fire({
          title: 'Profile updated!',
          icon: 'success'
        })
      }).catch(() => {
        this.user = User.getters('authenticatedUser')
        window.swal.fire({
          title: 'Failed to update details!',
          icon: 'error'
        })
      })
    },
    fileUploaded (files) {
      const formData = new FormData()

      formData.append('profile', files[0])

      User.dispatch('updateProfilePhoto', formData).then(() => {
        this.user = User.getters('authenticatedUser')
        this.saveSuccess = true
        window.swal.fire({
          title: 'Profile picture updated!',
          icon: 'success'
        })
      }).catch(() => {
        this.user = User.getters('authenticatedUser')
        window.swal.fire({
          title: 'Failed to upload picture!',
          icon: 'error'
        })
      })
    }
  },
  created () {
    this.user = Object.assign({}, User.getters('authenticatedUser'))
  }

}
</script>
