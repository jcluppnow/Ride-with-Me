import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import ormStore from './orm-store'
import map from './modules/map'
import files from './modules/files'

Vue.use(Vuex)

// Configure VueX store
const persistedState = createPersistedState({
  key: 'ride_with_me_v1',
  paths: ['database']
})

export default new Vuex.Store({
  modules: {
    map,
    files
  },
  plugins: [ormStore, persistedState]
})
