// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')
window.datetTimeLocalString = (hours = 0, days = 0) => {
    const time = new Date()
    time.setMonth(time.getMonth() + 1)
    time.setDate(time.getDate() + days)
    time.setHours(time.getHours() + hours)
    const month = `${time.getMonth()}`.padStart(2, '0')
    const day = `${time.getDate()}`.padStart(2, '0')
    const hour = `${time.getHours()}`.padStart(2, '0')
    const minute = `${time.getMinutes()}`.padStart(2, '0')
    const dateTimeString = `${time.getFullYear()}-${month}-${day}T${hour}:${minute}`
    return dateTimeString
}
