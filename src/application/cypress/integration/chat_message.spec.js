// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
})

import { MockSocket, getServers } from "../plugins/socket.js"

describe('Event Chat', () => {
  beforeEach(() => {
    cy.seed()
    cy.registerAppLoad()
    cy.fixture('users.json').then(users => {
        const user = users[0]
        cy.loginAs(user).then(() => {
            cy.visit("/")
        })
      })
    })

  it('Can send a message to the socket', () => {
    cy.visit("/chat", MockSocket)
    cy.waitForAppLoad()

    cy.cytag('messageInput').clear().type('New Message{enter}')
    cy.wait(1000)
    cy.fixture('events.json').then(events => {
      const event = events[0]
      cy.assertSocketReceived("send_message", { event_id: event.event_id })
    })
  })

  it('Can receive a message from the socket', () => {
    cy.visit("/chat", MockSocket)
    cy.waitForAppLoad()

    cy.fixture('events.json').then(events => {
      const event = events[0]
      let timestamp = new Date().toISOString()
      let message = `{"event": "chatmessage", "data": {"message_id": 99, "sender_id": 20, "created_at": "${timestamp}", "content": "Message from socket", "sender": {"id": 20, "full_name": "Brandon Orr", "profile": "/static/uploads/default.png"}, "event_id": "${event.pk}"}}`
      cy.wrap(getServers()).its('server').then(server => {
        expect(server).to.not.eq(null)
        window.sockets.server.send(message)
      })
      cy.wait(1000)
      cy.contains('Message from socket')
    })
  })

  it('Can send a message', () => {
    cy.visit("/chat")
    cy.waitForAppLoad()

    cy.cytag('messageInput').clear().type('New Message{enter}')

    cy.contains('New Message')
  })
})
