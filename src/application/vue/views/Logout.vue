<template>
  <div>
    Logging you out...
  </div>
</template>

<script>
import User from '@/store/models/user'
import Event from '@/store/models/event'
import Participates from '@/store/models/participates'

export default {
  name: 'Logout',
  async created () {
    // Clear state
    await Promise.all([
      User.deleteAll(),
      User.commit((state) => {
        state.authenticatedUser = null
      }),
      Event.deleteAll(),
      Participates.deleteAll()
    ])
    // Ensure state is fully cleared from browser storage
    setTimeout(() => {
      window.location = '/accounts/logout/'
    }, 3000)
  }
}
</script>
