<template>
  <AppFileInput
    class="w-full"
    cy="photoInput"
    @change="fileUploaded"
    :attributes="{ accept: 'image/png, image/jpeg, image/gif' }"
    :additional-input-classes="['flex', 'items-center', 'py-2', 'pr-2', 'w-full']"
    :base-errorless-classes="['text-white', 'bg-rwmDarkBlue', 'hover:bg-rwmOrange', 'hover:text-white', 'rounded', 'inline-flex', 'items-center', 'justify-center']"
    :base-error-classes="['text-white', 'bg-rwmDarkBlue', 'hover:bg-rwmOrange', 'hover:text-white', 'rounded', 'inline-flex', 'items-center', 'justify-center']"
    :disable-br="true"
    :error="errors.hero_image ? 'Error with image file' : ''"
  >
    <template #button>
      <!-- Upload vector -->
      <svg-vue
        icon="event/create-event-modal/upload-another-icon"
        class="ml-2 xl:ml-1 2xl:ml-1 h-5 w-5"
      />

      <span class="text-sm md:text-base ml-1">Upload another</span>
    </template>
  </AppFileInput>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: {
    errors: {
      required: true,
      type: Object
    }
  },
  methods: {
    ...mapActions({
      setImageFile: 'files/setImageFile'
    }),
    fileUploaded (files) {
      const selectedFile = files[0]

      this.setImageFile(selectedFile)

      const reader = new FileReader()

      reader.onload = (ev) => {
        this.$emit('imageRead', ev.target.result)
      }

      reader.readAsDataURL(selectedFile)
    }
  }
}
</script>
