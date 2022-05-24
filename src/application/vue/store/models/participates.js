import { Model } from '@vuex-orm/core'

// User-Event relationship
export default class Participates extends Model {
  // Name used as module name in store
  static entity = 'participates'

  static primaryKey = ['event_id', 'user_id']

  // Schema for model with their defaults
  static fields () {
    return {
      event_id: this.attr(null),
      user_id: this.attr(null),
      checked_in: this.attr(null)
    }
  }
}
