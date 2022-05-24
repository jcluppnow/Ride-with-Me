
// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
  return false
})

describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.seed()
  })

  it('Fail on empty form', () => {
    cy.visit('/accounts/login/')
    cy.cytag('username').should('have.value', '')
    cy.cytag('password').should('have.value', '')
    cy.cytag('sign-in').click()
    cy.contains('Username and password didn\'t match. Please try again.')
  })

  it('Can log in', () => {
    cy.fixture('users.json').then((users) => {
      const user = users[0]
      cy.visit('/accounts/login/')
      cy.cytag('username').type(user.fields.email)
      cy.cytag('password').type('password')
      cy.cytag('sign-in').click()
      cy.assertPathIs('/')
    })
  })

  it('Can log in with request', () => {
  cy.fixture('users.json').then((users) => {
    const user = users[0]
      cy.loginAs(user).then(() => {
        cy.visit('/events')
        cy.assertPathIs('/events')
      })
    })
  })
})
