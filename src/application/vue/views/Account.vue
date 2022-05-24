<template>
  <div>
    <div class="flex h-screen">
      <div
        class="absolute top-0 left-0 bg-blue-800 h-3/5 w-screen"
        style="background-image: linear-gradient(#6085D4, #15223F)"
      />
      <div class="relative m-auto w-10/12 z-1">
        <!-- User profile image -->
        <div class="flex justify-center pt-3">
          <div class="relative">
            <img
              class="rounded-full h-28 w-28 shadow-lg"
              :src="user.profile"
              alt=""
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

        <!-- User details -->
        <div class="flex flex-col items-center bg-gray-300 h-96 mt-5 w-full mx-auto shadow-xl rounded-lg font-semibold">
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
          <div class="absolute bottom-0 w-64">
            <div>
              <button
                type="button"
                class="absolute bottom-3 w-full mt-4 p-3 bg-gray-800 text-gray-100 font-semibold rounded-lg shadow-lg"
                @click.prevent="updateUserDetails"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import User from '@/store/models/user'

export default {
  name: 'Account',
  data () {
    return {
      user: null
    }
  },
  methods: {
    updateUserDetails () {
      // Attempt to save user details
      User.dispatch('updateUserDetails', this.user).then(() => {
        // On success, refetch the authenticatedUser from state - it will be the updated user
        this.user = User.getters('authenticatedUser')
        // show success message
        window.swal.fire({
          title: 'Profile updated!',
          icon: 'success'
        })
      }).catch(() => {
        // on error, reset to authenticatedUser details from state
        this.user = User.getters('authenticatedUser')
        // show failed message
        window.swal.fire({
          title: 'Failed to update details!',
          icon: 'error'
        })
      })
    },
    fileUploaded (files) {
      // File upload will trigger an event that has the file
      const formData = new FormData()
      formData.append('profile', files[0])

      this.saveSuccess = false
      this.saveFailed = false
      // Attempt to upload the photo
      User.dispatch('updateProfilePhoto', formData).then(() => {
        this.user = User.getters('authenticatedUser')
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
    // Copy authenticated user details into user data
    this.user = User.getters('authenticatedUser')
  }
}
</script>
