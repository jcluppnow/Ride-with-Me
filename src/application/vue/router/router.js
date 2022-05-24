import Vue from 'vue'
import Router from 'vue-router'

import Account from '../views/Account'
import Dashboard from '../views/Dashboard'
import Notifications from '../views/Notifications'
import Events from '../views/Events'
import PlanARoute from '../views/PlanARoute'
import Chat from '../views/chat/Chat'
import Logout from '../views/Logout'
import MobileChatList from '../views/chat/mobile/MobileChatList'
import MobileChat from '../views/chat/mobile/MobileChat'

Vue.use(Router)

// Configure the router
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/account',
      name: 'Account',
      component: Account,
      meta: {
        name: 'Account'
      }
    },
    {
      path: '/events',
      name: 'Events',
      component: Events,
      meta: {
        name: 'Events'
      }
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
      meta: {
        name: 'Chat'
      }
    },
    {
      path: '/notifications',
      name: 'Notifications',
      component: Notifications
    },
    {
      path: '/planroute',
      name: 'PlanARoute',
      component: PlanARoute
    },
    {
      path: '/chat/events',
      name: 'MobileChatList',
      component: MobileChatList,
      meta: {
        name: 'Chat'
      }
    },
    {
      path: '/chat/event/:eventId',
      name: 'MobileChat',
      component: MobileChat,
      meta: {
        name: 'Chat'
      }
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout
    }
  ],
  base: '/',
  mode: 'history'
})
