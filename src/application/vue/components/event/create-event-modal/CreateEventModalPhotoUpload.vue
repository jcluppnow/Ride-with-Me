<template>
  <div class="mt-2 w-full max-h-32">
    <label class="text-sm md:text-base font-semibold text-gray-700">Photo</label>

    <div
      v-if="eventImage"
      class="flex h-full pb-6 sm:pb-4"
    >
      <div class="cursor-pointer border-2 border-gray-400 border-dashed flex flex-col items-center w-1/2 h-full rounded">
        <img
          id="heroImage"
          ref="heroImage"
          class="h-full"
          :src="eventImage"
        >
      </div>
      <div class="ml-2 w-1/2 flex flex-end flex-col justify-between">
        <div class="h-1/2">
          <div
            v-if="imageFileName"
            class="text-sm md:text-base text-gray-700 truncate"
          >
            File name: {{ imageFileName }}
          </div>

          <div
            v-if="imageSize"
            class="text-sm md:text-base text-gray-700"
          >
            File size: {{ imageSize }} MB
          </div>
        </div>

        <CreateEventModalPhotoUploadAnother
          @imageRead="setImageData"
          :errors="errors"
        />
      </div>
    </div>

    <div
      v-else
      class="pb-6 sm:pb-4 h-full"
    >
      <CreateEventModalPhotoUploadNew
        @imageRead="setImageData"
        :errors="errors"
      />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Event from '@/store/models/event'
import CreateEventModalPhotoUploadNew from './CreateEventModalPhotoUploadNew'
import CreateEventModalPhotoUploadAnother from './CreateEventModalPhotoUploadAnother'

export default {
  props: {
    errors: {
      required: true,
      type: Object
    }
  },
  components: {
    CreateEventModalPhotoUploadAnother,
    CreateEventModalPhotoUploadNew
  },
  data () {
    return {
      imageData: null
    }
  },
  computed: {
    imageSize () {
      return this.imageFile ? (this.imageFile.size / (1024 * 1024)).toFixed(2) : 0
    },
    eventImage () {
      return this.imageData || Event.getters('getNewEvent').hero_image
    },
    imageFileName () {
      return this.imageFile ? this.imageFile.name : ''
    },
    ...mapState({
      imageFile: state => state.files.imageFile
    })
  },
  methods: {
    setImageData (imageData) {
      this.imageData = imageData
    }
  },
  created () {
    if (this.imageFile) {
      const reader = new FileReader()

      reader.onload = (ev) => {
        this.imageData = ev.target.result
      }

      reader.readAsDataURL(this.imageFile)
    }
  }
}
</script>
