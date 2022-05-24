<template>
  <AppFileInput
    class="cursor-pointer border-2 border-gray-400 border-dashed flex flex-col items-center w-full h-full rounded"
    :class="{ 'border-red-300':errors.hero_image }"
    cy="photoInput"
    @change="fileUploaded"
    :attributes="{ accept: 'image/png, image/jpeg, image/gif' }"
    :base-errorless-classes="['flex', 'flex-col', 'items-center', 'justify-center', 'w-full', 'h-full']"
    :base-error-classes="['flex', 'flex-col', 'items-center', 'justify-center', 'w-full', 'h-full']"
    :disable-br="true"
    :error="errors.hero_image ? 'Error with image file' : ''"
  >
    <template #button>
      <!-- Upload vector -->
      <svg-vue
        icon="event/create-event-modal/upload-new-icon"
        class="stroke-current text-gray-500 h-6 md:h-10 w-12"
      />

      <span class="text-sm md:text-base text-gray-700"><span class="text-sm md:text-base font-medium text-blue-600">Upload a file </span>or drag and drop</span>
      <span class="text-sm md:text-base text-gray-700">PNG, JPG, GIF up to 10MB</span>
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
