<template>
  <!-- Container for the AppTextInput -->
  <div>
    <!-- Input field for Text input. -->
    <input
      :name="inputName"
      :placeholder="placeholder"
      :class="[hasError ? [baseErrorClasses, additionalErrorClasses] : [baseErrorlessClasses, additionalErrorlessClasses], additionalInputClasses]"
      :value="value"
      @input="emitInput"
      @keyup.enter="$emit('enter', $event.target.value)"
      :type="inputType"
      :cy="cy"
      v-bind="attributes"
      ref="input"
    >
    <!-- Spacer -->
    <br v-if="!disableBr">
    <!-- Small text for error message -->
    <small
      v-if="hasError"
      :class="[baseErrorTextClasses, additionalErrorTextClasses]"
    >
      <!-- Output error -->
      {{ error }}
    </small>
  </div>
</template>

<script>
export default {
  name: 'AppTextInput',
  props: {
    // Cypress tag prop
    cy: {
      type: String,
      required: false,
      default: ''
    },
    // Input type prop to customize type
    inputType: {
      type: String,
      required: false,
      default: 'text'
    },
    // Name of the input itself
    inputName: {
      type: String,
      required: false,
      default: 'input-text'
    },
    // Value for the modal field
    value: {
      required: false,
      type: [String, Number],
      default: undefined
    },
    // Placeholder within the input field itself
    placeholder: {
      type: [String, Number],
      required: false,
      default: ''
    },
    // Any additional styling for the input field
    additionalInputClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Any styling for errorless state
    baseErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return ['cursor-text', 'appearance-none', 'border-2', 'rounded', 'focus:outline-none',
          'border-gray-300', 'bg-gray-100', 'focus:border-blue-500', 'focus:bg-white', 'shadow-inner', 'focus:shadow-none']
      }
    },
    // Any additional styling for errorless state
    additionalErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base styling for errors
    baseErrorClasses: {
      type: Array,
      required: false,
      default () {
        return ['cursor-text', 'appearance-none', 'border-2', 'rounded', 'focus:outline-none',
          'border-red-500', 'bg-red-100', 'focus:border-red-300', 'focus:bg-white', 'shadow-lg']
      }
    },
    // Any additional styling for errors
    additionalErrorClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Any styling for error text
    baseErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return ['text-red-500', 'font-semibold']
      }
    },
    // Any additional styling for error text
    additionalErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Error message itself
    error: {
      type: String,
      required: false,
      default: ''
    },
    // Attributes for input
    attributes: {
      type: Object,
      required: false,
      default () {
        return {}
      }
    },
    // Prop for whether the spacer appears
    disableBr: {
      type: Boolean,
      required: false,
      default: false
    },
    // define debounce delay for input
    debounce: {
      type: Number,
      required: false,
      default: 0
    }
  },
  data () {
    return {
      timeout: null
    }
  },
  computed: {
    // Checks if an error has occurred
    hasError () {
      return this.error !== ''
    }
  },
  methods: {
    emitInput (ev) {
      if (!window.disableDebounce && this.debounce > 0) {
        if (this.timeout) {
          clearTimeout(this.timeout)
        }
        this.timeout = setTimeout(() => {
          this.$emit('input', ev.target.value)
        }, this.debounce)
      } else {
        this.$emit('input', ev.target.value)
      }
    },
    focus () {
      this.$refs.input.focus()
    }
  }

}
</script>
