// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
  })

describe('Event Creation', () => {
  beforeEach(() => {
    cy.seed()
    cy.registerAppLoad()
    cy.fixture('users.json').then((users) => {
      const user = users[0]
      cy.loginAs(user).then(() => {
        cy.visit('/')
      })
    })
  })

  it('Fail on empty form', () => {
    cy.visit('/planroute')
    cy.waitForAppLoad()
    cy.closeMapworks()
    cy.cytag("eventNameInput").should('have.value', '')
    cy.cytag('eventDateInput').should('have.value', '')
    cy.cytag('photoInput').should('have.value', '')
    cy.cytag('routeFileInput').should('have.value', '')
    cy.cytag('maxParticipantsInput').should('have.value', 1)
    cy.cytag('averageSpeedInput').should('have.value', 1)
    cy.cytag('descriptionInput').should('have.value', '')
    cy.cytag('publicRadioInput').should('have.value', 'false')
    cy.cytag('privateRadioInput').should('have.value', 'true')
    cy.cytag('publishButton').click()
    cy.contains('Failed to create event!')
  })

  it('Can create an event', () => {
    cy.intercept('/api/v1/events/').as('createEvent')
    cy.visit('/planroute')
    cy.waitForAppLoad()
    cy.closeMapworks()
    cy.cytag("eventNameInput").type('test')
    cy.cytag('eventDateInput').type(window.datetTimeLocalString(0, 3))
    cy.cytag('photoInput').attachFile('TestPhoto.jpeg')
    cy.cytag('routeFileInput').attachFile('TestPath.gpx')
    cy.cytag('maxParticipantsInput').clear().type(5)
    cy.cytag('averageSpeedInput').clear().type(5)
    cy.cytag('descriptionInput').type('Test Description')
    cy.cytag('publishButton').click()
    cy.wait('@createEvent').then((interception) => {
      expect(interception.response.statusCode).to.eq(201)
    })
    cy.confirmSwal()
    cy.assertPathIs('/')
  })

  it('Can create a private event', () => {
    cy.intercept('/api/v1/events/').as('createEvent')
    cy.visit('/planroute')
    cy.waitForAppLoad()
    cy.closeMapworks()
    cy.cytag("eventNameInput").type('test')
    cy.cytag('eventDateInput').type(window.datetTimeLocalString(0, 3))
    cy.cytag('photoInput').attachFile('TestPhoto.jpeg')
    cy.cytag('routeFileInput').attachFile('TestPath.gpx')
    cy.cytag('maxParticipantsInput').clear().type(5)
    cy.cytag('averageSpeedInput').clear().type(5)
    cy.cytag('descriptionInput').type('Test Description')
    cy.cytag('privateRadioInput').check()
    cy.cytag('publishButton').click()
    cy.wait('@createEvent').then((interception) => {
      expect(interception.response.body.is_private).to.be.true
    })
    cy.confirmSwal()
    cy.assertPathIs('/')
  })
})
