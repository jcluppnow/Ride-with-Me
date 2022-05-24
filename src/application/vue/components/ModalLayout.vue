<template>
  <div
    @keyup.esc="$emit('close')"
    tabindex="0"
  >
    <div
      class="fixed bottom-0 left-0 z-50 flex justify-center items-center sm:m-4 inset-0"
      @mousedown="$emit('close')"
    >
      <div
        class="flex flex-col md:max-w-3xl shadow-xl bg-gray-200 h-screen sm:h-full lg:h-auto sm:rounded"
        :class="[{'lg:h-screen': isNestHub }, externalClasses]"
        @mousedown.stop=""
      >
        <!-- HEADER -->
        <div class="relative min-h-content rounded-t-lg border-b border-gray-300">
          <!-- Close button -->
          <button
            class="group absolute z-50 right-0 m-2"
            @click.prevent="$emit('close')"
          >
            <svg-vue
              icon="modal/close-icon"
              class="h-6 w-6 group text-white hover:text-red-600"
            />
          </button>

          <slot name="header">
            Header
          </slot>
        </div>

        <!-- BODY -->
        <div class="flex p-2 sm:p-4 h-full overflow-y-auto bg-gray-200">
          <slot name="body">
            Body
          </slot>
        </div>

        <!-- FOOTER -->
        <div class="border-t-2 border-gray-300 bg-gray-200 sm:rounded-b sm:border-t min-h-3">
          <slot name="footer">
            Footer
          </slot>
        </div>
      </div>
    </div>

    <div
      class="opacity-25 fixed inset-0 z-40 bg-black"
      @click.prevent="$emit('close')"
    />
  </div>
</template>

<script>
export default {
  name: 'ModalLayout',
  props: {
    externalClasses: {
      type: String,
      default: ''
    }
  },
  computed: {
    isNestHub () {
      return window.innerHeight <= 600
    }
  }
}
</script>
