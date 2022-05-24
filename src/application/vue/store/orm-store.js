
import VuexORM from '@vuex-orm/core'

import User from '@/store/models/user'
import user from '@/store/modules/user'

import Participates from '@/store/models/participates'
import participates from '@/store/modules/participates'

import EventModel from '@/store/models/event'
import eventState from '@/store/modules/event'

import ChatMessage from '@/store/models/chat_message'
import chat from '@/store/modules/chat_message'

import Weather from '@/store/models/weather'
import weather from '@/store/modules/weather'

import Traffic from '@/store/models/traffic'
import traffic from '@/store/modules/traffic'

import NotificationModel from '@/store/models/notification'
import notificationState from '@/store/modules/notification'

// Configure VueX ORM store
const database = new VuexORM.Database()

// Register models and relationships to database.
database.register(User, user)
database.register(EventModel, eventState)
database.register(Participates, participates)
database.register(ChatMessage, chat)
database.register(Weather, weather)
database.register(Traffic, traffic)
database.register(NotificationModel, notificationState)

export default VuexORM.install(database, { namespace: 'database' })
