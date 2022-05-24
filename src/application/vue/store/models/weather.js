import { Model } from '@vuex-orm/core'

export default class Weather extends Model {
  // Name used as module name in store
  static entity = 'weather'

  // Define which field is the primary key
  static primaryKey = 'weather_id'

  // Schema for model with their defaults
  static fields () {
    return {
      weather_id: this.uid(),
      temperature: this.number(0),
      humidity: this.number(0),
      precipitation: this.number(0),
      wind_speed: this.number(0),
      wind_direction: this.number(0)
    }
  }
}
