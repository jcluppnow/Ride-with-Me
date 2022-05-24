// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
import 'cypress-file-upload';

Cypress.Commands.add("seed", () => {
    cy.request({ url: '__cypress__/seed', timeout: 120000 })
})

Cypress.Commands.add("cytag", (selector) => {
    return cy.get(`[cy=${selector}]`)
})

Cypress.Commands.add("assertPathIs", (path) => {
    cy.location().should((loc) => {
        expect(loc.pathname).to.eq(path)
    })
})

Cypress.Commands.add("loginMapworks", () => {
    cy.get("#login").click()
    cy.wait(1000)
})

Cypress.Commands.add("closeMapworks", () => {
    cy.get("#studio-overlay-container > div.modal.fade.in > div > div > div.modal-header > div > a", { timeout: 10000 }).click()
    cy.wait(200)
})

Cypress.Commands.add("loginAs", (user, password = 'password') => {
    cy.request('accounts/login/')
       .its('body')
       .then((body) => {

         const $html = Cypress.$(body)
         const csrf = $html.find('input[name=csrfmiddlewaretoken]').val()
         cy.request({
          method: 'POST',
          url: '/accounts/login/',
          failOnStatusCode: true,
          followRedirects: false,
          form: true,
          body: {
              username: user.fields.email,
              password,
              csrfmiddlewaretoken: csrf,
          },
        }).then((resp) => {

            expect(resp.status).to.eq(302)

            const cookie = resp.headers['set-cookie'][1].split(';')[0].split('=')[1]
            cy.setCookie('sessionid', cookie, { httpOnly: true, path: '/'})
            cy.request('/api/v1/profile').then((response) => {
                expect(response.status).to.eq(200)
            }).as('profile')
            cy.get('@profile')
            cy.visit('/')
          })
     })
})

Cypress.Commands.add("confirmSwal", (path) => {
    cy.get('.swal2-confirm').click()
})

Cypress.Commands.add("cancelSwal", (path) => {
    cy.get('.swal2-cancel').click()
})

Cypress.Commands.add("denySwal", (path) => {
    cy.get('.swal2-deny').click()
})

Cypress.Commands.add("registerAppLoad", (path) => {
    cy.intercept('api/v1/events/attending').as('attending')
    cy.intercept('api/v1/events/organising').as('organising')
    cy.intercept('api/v1/events/chat').as('chat')
})

Cypress.Commands.add("waitForAppLoad", (path) => {
    cy.window().its('appReady').then(ready => {
        expect(ready).to.eq(true)
    })
    cy.wait(['@attending', '@organising', '@chat'])
})
