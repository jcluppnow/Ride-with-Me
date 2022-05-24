<template>
  <div>
    <!-- Guest user -->
    <a
      class="hover:bg-indigo-700 flex justify-center my-4 mx-auto w-full p-3 bg-indigo-900 text-gray-100 font-semibold rounded-lg shadow-lg sm:w-1/2"
      href="/accounts/register/"
    >
      Register to Attend
    </a>
  </div>
</template>

<script>

export default {
  name: 'UnauthenticatedEventButtons',
  props: {
    event: {
      required: true,
      type: Object
    }
  }
}
</script>
