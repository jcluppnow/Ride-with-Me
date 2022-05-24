import { Model } from '@vuex-orm/core'
import User from '@/store/models/user'
import Event from '@/store/models/event'

export default class Notification extends Model {
  // Name used as module name in store
  static entity = 'notifications'

  static primaryKey = 'notification_id'

  // Schema for model with their defaults
  static fields () {
    return {
      notification_id: this.attr(null),
      content: this.attr(''),
      event_id: this.attr(null),
      event: this.belongsTo(Event, 'event_id'),
      notifier_id: this.attr(null),
      notifier: this.belongsTo(User, 'notifier_id'),
      link: this.attr(null),
      created_at: this.attr(null),
      read_at: this.attr(null)
    }
  }

  /**
   * Return starting time as a date object
   */
  get createdAtDate () {
    return new Date(this.created_at)
  }
}
