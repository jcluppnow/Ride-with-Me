// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
})

import { MockSocket } from "../plugins/socket.js"

describe('Event Chat', () => {
  beforeEach(() => {
    cy.registerAppLoad()
    cy.seed()
    cy.fixture('events.json').then(events => {
        let event = events[0]
        cy.request({ url: '/__cypress__/create_message_batch', body: {
            batch_size: 30,
            event_id: event.pk
        }, timeout: 180000 })

        cy.fixture('users.json').then(users => {
            const user = users[0]
            cy.loginAs(user).then(() => {
                cy.visit("/")
            })
        })
      })
  })

  it('Can scroll to paginate', () => {
    cy.visit("/chat")
    cy.waitForAppLoad()

    cy.intercept('/api/v1/events/*/chat**').as('paginateMessages')

    cy.cytag('messageFrame').scrollTo('top')

    cy.wait('@paginateMessages').then(intercept => {
      cy.expect(intercept.request.url.slice(-1)).to.equal('2')
      cy.window().its('app.$children.0.$children.2.$children.1.$children.0').then(component => {
          expect(component.page).to.eq(2)
          cy.cytag('messageFrame').scrollTo('top')
      })
    })

    cy.wait('@paginateMessages').then(intercept => {
      cy.expect(intercept.request.url.slice(-1)).to.equal('3')
      cy.cytag('messageFrame').scrollTo('bottom')
    })

    cy.wait('@paginateMessages').then(intercept => {
      cy.expect(intercept.request.url.slice(-1)).to.equal('2')
    })
  })
})
