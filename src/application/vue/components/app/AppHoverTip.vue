<template>
  <div class="relative tooltip-box group hover:opacity-100">
    <slot />
    <div
      class="rounded text-white absolute bg-rwmLighterBlue bottom-full left-1/2 w-32 -ml-16 text-center opacity-0 group-hover:opacity-100 z-10 mb-2"
    >
      <span
        class="text"
      >{{ text }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>

.text::after {
  content: " ";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #283F70 transparent transparent transparent;
}
</style>
