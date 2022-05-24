import { Model } from '@vuex-orm/core'
import Participates from '@/store/models/participates'
import User from '@/store/models/user'
import Weather from '@/store/models/weather'

export default class Event extends Model {
  // Name used as module name in store
  static entity = 'event'

  // Define which field is the primary key
  static primaryKey = 'event_id'

  // Schema for model with their defaults
  static fields () {
    return {
      event_id: this.attr(''),
      average_speed: this.attr(0),
      route_coordinates: this.attr([]),
      name: this.attr(''),
      max_participants: this.number(0),
      participants: this.belongsToMany(User, Participates, 'event_id', 'user_id'),
      description: this.attr(''),
      attending: this.attr(false),
      checked_in: this.attr(false),
      starting_time: this.attr(null),
      is_private: this.boolean(false),
      distance: this.number(0),
      duration: this.number(0),
      is_full: this.boolean(false),
      started: this.boolean(false),
      finished: this.boolean(false),
      organiser_id: this.attr(null),
      organiser: this.belongsTo(User, 'organiser_id'),
      starting_location: this.attr(null),
      location_string: this.attr(''),
      hero_image: this.attr(''), // could change this to a default image url
      created_at: this.attr(null),
      weather_id: this.attr(null),
      weather: this.belongsTo(Weather, 'weather_id')
    }
  }

  /**
   * Return distance in KM
   */
  get distanceInKm () {
    return this.distance / 1000
  }

  /**
   * Return duration in hour
   */
  get durationinHr () {
    return this.duration / 3600
  }

  /**
   * Return starting time as a date object
   */
  get startingTimeDate () {
    return new Date(this.starting_time)
  }

  /**
   * Return whether the event has been started or if the starting time has been reached
   */
  get hasStarted () {
    return this.started || this.startingTimeDate < new Date()
  }

  /**
   * Get all X coordinates in route_coordinates
   */
  get xCoordinates () {
    const coordinates = []

    this.route_coordinates.coordinates.forEach(coord => {
      coordinates.push(coord[0])
    })

    return coordinates
  }

  /**
   * Get all Y coordinates in route_coordinates
   */
  get yCoordinates () {
    const coordinates = []

    this.route_coordinates.coordinates.forEach(coord => {
      coordinates.push(coord[1])
    })

    return coordinates
  }

  get WindDirection () {
    const windDirection = this.weather.wind_direction
    let direction = ''

    switch (windDirection) {
    case 0:
      direction = 'N'
      break

    case 90:
      direction = 'E'
      break

    case 180:
      direction = 'S'
      break

    case 270:
      direction = 'W'
      break

    default:
      if (windDirection > 0 && windDirection < 90) direction = 'NE'
      else if (windDirection > 90 && windDirection < 180) direction = 'SE'
      else if (windDirection > 180 && windDirection < 270) direction = 'SW'
      else direction = 'NW'
    }

    return direction
  }
}
