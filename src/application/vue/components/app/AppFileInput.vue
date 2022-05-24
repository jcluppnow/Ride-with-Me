<template>
  <!-- Main contianer for AppFileInput -->
  <div>
    <!-- Customizable button that conditionally loads error styling and input classes -->
    <button
      :class="[hasError ? [baseErrorClasses, additionalErrorClasses] : [baseErrorlessClasses, additionalErrorlessClasses], additionalInputClasses]"
      @click.prevent="$refs.fileInput.click()"
    >
      <!-- Slot for custom elements to be inserted. -->
      <slot name="button">
        Upload
      </slot>
    </button>

    <!-- File input, able to be customised using attributes value -->
    <input
      ref="fileInput"
      hidden
      :name="inputName"
      @change="$emit('change', $event.target.files)"
      type="file"
      :cy="cy"
      v-bind="attributes"
    >
    <!-- Conditional spacer -->
    <br v-if="!disableBr">

    <!-- Small text tag that can attach customisable error classes for styling -->
    <small
      v-if="hasError"
      :class="[baseErrorTextClasses, additionalErrorTextClasses]"
    >
      <!-- Link to error prop -->
      {{ error }}
    </small>
  </div>
</template>

<script>
export default {
  name: 'AppFileInput',
  props: {
    // Prop to specify cypress tag
    cy: {
      type: String,
      required: false,
      default: ''
    },
    // Prop to specify what input type the dom element is
    inputType: {
      type: String,
      required: false,
      default: 'text'
    },
    // Prop to customise the name attribute to be used in form submit
    inputName: {
      type: String,
      required: false,
      default: 'input-text'
    },
    // Placeholder to be inside input fields.
    placeholder: {
      type: [String, Number],
      required: false,
      default: ''
    },
    // Used if we do not want to override the base class of inputs, any extra
    // inputs can be added here
    additionalInputClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Returns styling for base error classes
    baseErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return ['text-white', 'bg-gray-600', 'hover:bg-gray-400',
          'hover:text-white', 'rounded', 'inline-flex', 'items-center', 'justify-center']
      }
    },
    // Used to add any extra error classes on top of base classes
    additionalErrorlessClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base styling for error classes
    baseErrorClasses: {
      type: Array,
      required: false,
      default () {
        return ['text-gray-800', 'bg-gray-200', 'hover:bg-gray-600',
          'hover:text-white', 'hover:text-white', 'rounded', 'inline-flex', 'items-center']
      }
    },
    // Add any additional classes beside base classes
    additionalErrorClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Base styling for error text classes
    baseErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return ['text-red-500', 'font-semibold']
      }
    },
    // Add any additional classes for error text beside base classes
    additionalErrorTextClasses: {
      type: Array,
      required: false,
      default () {
        return []
      }
    },
    // Prop for the error itself.
    error: {
      type: String,
      required: false,
      default: ''
    },
    // Prop for the attributes of a input files
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
    }
  },
  computed: {
    // Check if the error exists
    hasError () {
      return this.error !== ''
    }
  }

}
</script>
