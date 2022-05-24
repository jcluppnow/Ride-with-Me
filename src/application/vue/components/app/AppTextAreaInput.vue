<template>
  <!-- Container for AppTextAreaInput -->
  <div>
    <!-- Custom text input field. -->
    <textarea
      :name="inputName"
      :placeholder="placeholder"
      :class="[hasError ? [baseErrorClasses, additionalErrorClasses]: [baseErrorlessClasses, additionalErrorlessClasses],additionalInputClasses]"
      :value="value"
      @input="emitInput"
      :type="inputType"
      :cy="cy"
      v-bind="attributes"
    />

    <!-- Spacer -->
    <br v-if="!disableBr">

    <!-- Small text to conditional load error classes based on v-if -->
    <small
      v-if="hasError"
      :class="[baseErrorTextClasses, additionalErrorTextClasses]"
    >
      <!-- Prop for error message -->
      {{ error }}
    </small>
  </div>
</template>

<script>
export default {
  name: 'AppTextAreaInput',
  props: {
    // Prop for cypress input name
    cy: {
      type: String,
      required: false,
      default: ''
    },
    // Customisable input prop
    inputType: {
      type: String,
      required: false,
      default: 'text'
    },
    // Customisable name of input name
    inputName: {
      type: String,
      required: false,
      default: 'input-text'
    },
    // Value related to v-model
    value: {
      required: true,
      type: [String, Number]
    },
    // Placeholder for input
    placeholder: {
      type: [String, Number],
      required: false,
      default: ''
    },
    // Prop to extend any base input classes
    additionalInputClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base class for when no errors have occurred
    baseErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return ['cursor-text', 'appearance-none', 'border-2', 'rounded', 'focus:outline-none',
          'border-gray-300', 'bg-gray-100', 'focus:border-blue-500', 'focus:bg-white', 'shadow-inner', 'focus:shadow-none']
      }
    },
    // Prop to extend base errorless classes
    additionalErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base classes for styling errors
    baseErrorClasses: {
      type: Array,
      required: false,
      default () {
        return ['cursor-text', 'appearance-none', 'border-2', 'rounded', 'focus:outline-none',
          'border-red-500', 'bg-red-100', 'focus:border-red-300', 'focus:bg-white', 'shadow-lg']
      }
    },
    // Additional classes to extend error base class
    additionalErrorClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base class for error text styling
    baseErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return ['text-red-500', 'font-semibold']
      }
    },
    // Prop to extend error text classes
    additionalErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Error message prop
    error: {
      type: String,
      required: false,
      default: ''
    },
    // Attributes for input fields
    attributes: {
      type: Object,
      required: false,
      default () {
        return {}
      }
    },
    // Prop to track whether the break is disabled
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
    // Check if the error was set
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
    }
  }

}
</script>
