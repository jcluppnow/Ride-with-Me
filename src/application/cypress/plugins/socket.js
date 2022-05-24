import { Server, WebSocket } from 'mock-socket';

window.sockets = {}
window.messages = []
function mockServer() {
    window.sockets.mockServer = new Server("ws://localhost:8080/ws/ridewithme")

    window.sockets.mockServer.on("connection", socket => {
        window.sockets.server = socket
        // on message, log to array to perform assertions on later
        socket.on("message", data => {
            window.messages.push(data)
        })
    })
}

function initServer() {
  // Reset socket connections
  for (const socket of Object.values(window.sockets)) {
    socket.close()
  }

  mockServer()
}

let getServers = () => {
  return window.sockets
}

let MockSocket = {
    onBeforeLoad(win) {
        initServer()
        cy.stub(win, "WebSocket", url => new WebSocket(url))
    }
}

export {
    MockSocket,
    getServers
}


Cypress.Commands.add("assertSocketEmpty", (data) => {
    cy.wrap(messages).as('MessageData')

    let messageExists = false
    let dataString = JSON.stringify(data)

    cy.get('@MessageData').should('have.length', 0)
})

Cypress.Commands.add("assertSocketReceived", (requestType, data) => {
    cy.wrap(window.messages).as('MessageData')
    let messageExists = false
    let dataString = JSON.stringify(data)
    dataString = dataString.substr(1).slice(0, -1)
    cy.get('@MessageData', { timeout: 10000 }).should('have.length.gte', 1).then(data => {
        data.forEach((message) => {
            if (message.includes(requestType) && message.includes(dataString)) {
                messageExists = true
            }
        })
        expect(messageExists).to.be.true
    })
})
