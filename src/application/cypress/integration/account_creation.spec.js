// Prevent mapworks popup from stopping tests
Cypress.on('uncaught:exception', (err, runnable) => {
    return false
  })

describe('Account_Creation', () => {
  beforeEach(() => {
    cy.visit('/')
    cy.seed()
  })

  it('Fail on empty form', () => {
    cy.visit('/accounts/register/')
    cy.cytag('email').should('have.value', '')
    cy.cytag('full_name').should('have.value', '')
    cy.cytag('password1').should('have.value', '')
    cy.cytag('password2').should('have.value', '')
    cy.cytag('create-account').click()
  })

  it('Fail on invalid email', () => {
    cy.visit('/accounts/register/')
    cy.cytag('email').type('email')
    cy.cytag('full_name').type('Johnny Good')
    cy.cytag('password1').type('Howdydoodily1')
    cy.cytag('password2').type('Howdydoodily1')
    cy.cytag('create-account').click()
  })

  it('Fail on invalid password', () => {
    cy.visit('/accounts/register/')
    cy.cytag('email').type('email@email.com')
    cy.cytag('full_name').type('Johnny Good')
    cy.cytag('password1').type('pass')
    cy.cytag('password2').type('pass')
    cy.cytag('create-account').click()
  })

  it('Fail on different passwords', () => {
    cy.visit('/accounts/register/')
    cy.cytag('email').type('email@email.com')
    cy.cytag('full_name').type('Johnny Good')
    cy.cytag('password1').type('Cypress1')
    cy.cytag('password2').type('Cypress2')
    cy.cytag('create-account').click()
  })

  it('Can create account', () => {
    cy.visit('/accounts/register/')
    cy.cytag('email').type('email@email.com')
    cy.cytag('full_name').type('Emilio Gonsalves')
    cy.cytag('password1').type('Cypress1')
    cy.cytag('password2').type('Cypress1')
    cy.cytag('create-account').click()
  })
})
