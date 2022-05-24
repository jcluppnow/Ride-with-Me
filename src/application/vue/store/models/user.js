import { Model } from '@vuex-orm/core'
import Event from '@/store/models/event'
import Participates from '@/store/models/participates'

export default class User extends Model {
  // Name used as module name in store
  static entity = 'user'

  // Schema for model with their defaults
  static fields () {
    return {
      id: this.attr(0),
      full_name: this.attr(''),
      profile: this.attr(''),
      events: this.belongsToMany(Event, Participates, 'user_id', 'event_id')
    }
  }
}
