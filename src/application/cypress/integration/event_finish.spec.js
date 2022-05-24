// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
})

import { MockSocket } from "../plugins/socket.js"

describe('Event Finish', () => {
  beforeEach(() => {
    cy.seed()
    cy.registerAppLoad()
    cy.fixture('users.json').then((users) => {
      const user = users[0]
      cy.request('/__cypress__/create_event', {
        organiser_id: user.pk,
        starting_time: window.datetTimeLocalString(-8), // set to our time zone
        started: true,
        finished: false
      }).as('create_event')
      cy.get('@create_event').then((resp) => {
        cy.wrap(resp.body.create_event).as('new_event_0')
      })

      cy.request('/__cypress__/create_event', {
        organiser_id: user.pk,
        starting_time: window.datetTimeLocalString(-8), // set to our time zone
        started: false
      }).as('create_event')
        cy.get('@create_event').then((resp) => {
        cy.wrap(resp.body.create_event).as('new_event_1')
      })

      cy.loginAs(user).then(() => {
        cy.visit("/")
      })
    })
  })

  it('Can finish an event', () => {
    cy.intercept('/api/v1/events/*/finish').as('eventFinish')
    cy.visit("/events", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('event-card-1').scrollIntoView().click()
    cy.cytag('finish-event').click()
    cy.wait('@eventFinish').its('response').then((response) => {
      expect(response.statusCode).to.eq(200)
      // cy.get('@new_event_0').then((event) => {
      //     cy.assertSocketReceived("send_location", { event_id: event.event_id })
      // })
    })
    cy.assertPathIs("/events")
  })

  it('Cannot finish an event that is not started', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.visit("/events")
    cy.waitForAppLoad()

    cy.cytag('event-card-2').scrollIntoView().click()
    cy.cytag('finish-event').should('not.exist')
  })
})
