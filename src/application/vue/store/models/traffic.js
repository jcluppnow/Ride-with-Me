import { Model } from '@vuex-orm/core'

export default class Traffic extends Model {
  // Name used as module name in store
  static entity = 'traffic'

  // Define which field is the primary key
  static primaryKey = 'traffic_id'

  // Schema for model with their defaults
  static fields () {
    return {
      traffic_id: this.attr(''),
      description: this.attr(''),
      start_date: this.attr(null),
      end_date: this.attr(null),
      last_updated: this.attr(null),
      road_closed: this.boolean(false),
      severity: this.number(0),
      traffic_type: this.number(0),
      verified: this.boolean(false),
      coordinates: this.attr(null)
    }
  }
}
