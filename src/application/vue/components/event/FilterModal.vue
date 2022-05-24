<template>
  <ModalLayout
    @close="$emit('close')"
    :external-classes="'w-96'"
  >
    <template #header>
      <h1 class="font-semibold text-2xl text-gray-700 h-8 py-2 pl-4 mb-3">
        Filter Events
      </h1>
    </template>

    <template #body>
      <div class="w-full">
        <p class="font-semibold text-gray-700">
          Distance <span class="text-xs text-gray-600">km</span>
        </p>

        <vue-slider
          v-model="distanceValue"
          ref="distanceSlider"
          class="vue-slider"
          :min="0"
          :max="50"
        />

        <p class="font-semibold mt-4 text-gray-700">
          Duration <span class="text-xs text-gray-600">hr</span>
        </p>

        <vue-slider
          v-model="durationValue"
          ref="durationSlider"
          class="vue-slider"
          :min="0"
          :max="10"
        />

        <p class="font-semibold mt-4 text-gray-700">
          Speed <span class="text-xs text-gray-600">km/h</span>
        </p>

        <vue-slider
          v-model="speedValue"
          ref="speedSlider"
          class="vue-slider"
          :min="0"
          :max="50"
        />
      </div>
    </template>

    <template #footer>
      <div class="flex space-x-2 mt-2 text-sm w-full px-2">
        <button
          @click.prevent="$emit('reset')"
          class="mb-2 hover:bg-rwmOrange items-center bg-rwmDarkBlue rounded px-5 py-2 font-semibold shadow-lg text-white w-1/2"
        >
          Reset
        </button>

        <button
          @click.prevent="applyFilter"
          class="mb-2 hover:bg-rwmOrange items-center bg-rwmDarkBlue rounded px-5 py-2 font-semibold shadow-lg text-white w-1/2"
        >
          Apply
        </button>
      </div>
    </template>
  </ModalLayout>
</template>

<script>
import ModalLayout from '../ModalLayout'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import Event from '@/store/models/event'

export default {
  components: {
    ModalLayout,
    VueSlider
  },
  computed: {
    durationValue: {
      get () {
        return Event.getters('getDuration')
      },
      set (value) {
        Event.dispatch('setDuration', value)
      }
    },
    distanceValue: {
      get () {
        return Event.getters('getDistance')
      },
      set (value) {
        Event.dispatch('setDistance', value)
      }
    },
    speedValue: {
      get () {
        return Event.getters('getSpeed')
      },
      set (value) {
        Event.dispatch('setSpeed', value)
      }
    }
  },
  methods: {
    applyFilter () {
      this.distanceValue = this.$refs.distanceSlider.getValue()
      this.speedValue = this.$refs.speedSlider.getValue()
      this.durationValue = this.$refs.durationSlider.getValue()
      this.$emit('close')
    }
  }
}
</script>

<style>
.vue-slider-dot-handle {
    height: 15px;
    width: 15px;
}

.vue-slider-rail {
    height: 5px;
}

.vue-slider-process {
    background-color: #283F70;
}
.vue-slider-dot-tooltip-inner {
    background-color: #283F70;
    border-color: #283F70;
}

</style>
