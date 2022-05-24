// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
  })

describe('Event Update', () => {
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
        cy.visit('/')
      })
    })
  })

  it('Can update all event details', () => {
    cy.intercept('/api/v1/events/*/').as('eventUpdate')
    cy.visit('/events')
    cy.waitForAppLoad()
    cy.cytag('event-card-2').click()
    cy.cytag('update-event').click()
    cy.assertPathIs('/planroute')
    cy.closeMapworks()
    cy.get('@new_event_1').then((event) => {
      cy.cytag("eventNameInput").should('have.value', event.name)
    })

    cy.cytag("eventNameInput").clear().type('Updated event name')
    cy.cytag('maxParticipantsInput').clear().type(20)
    cy.cytag('averageSpeedInput').clear().type(5)
    cy.cytag('descriptionInput').clear().type('Updated Description')
    cy.cytag('updateButton').click()

    cy.wait('@eventUpdate').its('response.statusCode').should('eq', 200)
  })
})
