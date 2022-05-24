import { Model } from '@vuex-orm/core'
import Event from '@/store/models/event'
import User from '@/store/models/user'

export default class ChatMessage extends Model {
  // Name used as module name in store
  static entity = 'chat_message'

  // Define which field is the primary key
  static primaryKey = 'message_id'

  // Schema for model with their defaults
  static fields () {
    return {
      message_id: this.attr(''),
      content: this.attr(''),
      sender_id: this.attr(null),
      sender: this.belongsTo(User, 'sender_id'),
      event_id: this.attr(null),
      event: this.belongsTo(Event, 'event_id'),
      created_at: this.attr(null)
    }
  }

  /**
   * Return created_at time as a date object
   */
  get createdAtDate () {
    return new Date(this.created_at)
  }
}
