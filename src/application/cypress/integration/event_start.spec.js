// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
})

import { MockSocket } from "../plugins/socket.js"

describe('Event Start', () => {
  beforeEach(() => {
    cy.seed()
    cy.registerAppLoad()
    cy.fixture('users.json').then((users) => {
        const user = users[0]
        cy.request('/__cypress__/create_event', {
            organiser_id: user.pk,
            starting_time: window.datetTimeLocalString(-8), // set to our time zone
            started: false
        }).as('create_event')
        cy.get('@create_event').then((resp) => {
            cy.wrap(resp.body.create_event).as('new_event_0')
        })
        cy.request('/__cypress__/create_event', {
            organiser_id: user.pk,
            starting_time: window.datetTimeLocalString(-5), // 3 hours ahead of us
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

  it('Can start an event', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.visit("/events", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('event-card-1').click()
    cy.cytag('start-event').click()
    cy.confirmSwal()
    cy.wait('@eventStart').its('response').then((response) => {
    expect(response.statusCode).to.eq(200)
    // assert current event is set and the location is sent through the websocket
    cy.get('@new_event_0').then((event) => {
        cy.window().its('app.$store.state').then(state => {
            expect(state.database.event.currentEvent).to.eq(event.event_id)
        })
        cy.assertSocketReceived("send_location", { event_id: event.event_id })
      })
    })
    cy.assertPathIs("/")
  })

  it('Can persist a started event', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.visit("/events", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('event-card-1').click()
    cy.cytag('start-event').click()
    cy.wait('@eventStart').its('response').then((response) => {
      expect(response.statusCode).to.eq(200)
    })
    cy.reload()
    cy.get('@new_event_0').then((event) => {
      cy.window().its('app.$store.state').then(state => {
          expect(state.database.event.currentEvent).to.eq(event.event_id)
      })
    })
    cy.contains('This will mark the event as finished')
  })

  it('Can finish a persisted event', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.intercept('/api/v1/events/*/finish').as('eventFinish')
    cy.visit("/events", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('event-card-1').click()
    cy.cytag('start-event').click()
    cy.wait('@eventStart').its('response').then((response) => {
      expect(response.statusCode).to.eq(200)
    })
    cy.reload()
    cy.get('@new_event_0').then((event) => {
      cy.window().its('app.$store.state').then(state => {
          expect(state.database.event.currentEvent).to.eq(event.event_id)
      })
    })
    cy.contains('This will mark the event as finished')
    cy.confirmSwal()
    cy.wait('@eventFinish').its('response').then((response) => {
      expect(response.statusCode).to.eq(200)
    })
    cy.window().its('app.$store.state').then(state => {
      expect(state.database.event.currentEvent).to.eq(null)
    })
  })

  it('Can restart the location watcher for a persisted event', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.visit("/events", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('event-card-1').click()
    cy.cytag('start-event').click()
    cy.wait('@eventStart').its('response').then((response) => {
      expect(response.statusCode).to.eq(200)
    })
    cy.reload()
    cy.get('@new_event_0').then((event) => {
      cy.window().its('app.$store.state').then(state => {
          expect(state.database.event.currentEvent).to.eq(event.event_id)
      })
    })
    cy.contains('This will mark the event as finished')
    cy.denySwal()
    cy.contains('Would you like to re-enable location tracking')
    cy.confirmSwal()
    cy.window().its('app.$store.state').then(state => {
      expect(state.map.watcherId).to.not.eq(null)
    })
  })

  it('Cannot start an event that is not ready', () => {
    cy.intercept('/api/v1/events/*/start').as('eventStart')
    cy.visit("/events")
    cy.waitForAppLoad()
    cy.cytag('event-card-2').click()
    cy.cytag('start-event').should('not.exist')
  })
})
