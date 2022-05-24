<template>
  <div
    class="h-screen w-full"
    ref="wrapper"
  >
    <div
      id="mapworksEmbed"
      ref="mapworksEmbed"
    />
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'MapworksEmbed',
  computed: {
    ...mapGetters({
      getMapEmbed: 'map/getMapEmbed'
    })
  },
  mounted () {
    if (!this.getMapEmbed) {
      // Configure mapworks
      const { Studio } = window
      const { id = 'AXhI8CSUAAA2ac12AAAA' } = Studio._.urlParamObj()

      const config = {
        map: id,
        mapworksPath: 'https://amristar.mapworks.io',
        access: Studio.core.Map.Access.ANONYMOUS,
        appNavigationControl: false,
        navigationControl: false,
        scaleControl: false,
        toolbarControl: false,
        zoomControl: false,
        tooltipControl: false,
        mapworksLoginProvider: {
          client_id: '307u62uqvt7iid9ldii08qpguf',
          // Callback url, where we have openId.html stored in our static files.
          popup_redirect_uri: `${process.env.MIX_APP_URL || 'http://localhost:8080'}/static/application/mapworks/openId.html`,
          anonymousIdp: 'Public-Access'
        }
      }

      Studio.app.App._initSearch = function () {}
      window.map = Studio.init('#mapworksEmbed', config).once('ready', () => {
        window.map.off('fetch:failed')

        this.setMapEmbed(this.$refs.mapworksEmbed)

        this.$emit('ready')
      })
    } else {
      this.$refs.mapworksEmbed.replaceWith(this.getMapEmbed)
      this.$emit('ready')
    }
  },
  methods: {
    ...mapMutations({
      setMapEmbed: 'map/setMapEmbed',
      setMapworks: 'map/setMapworks'
    })
  }
}
</script>
