let hidden = 0
let hiddenConfirmation = 0

function togglePasswordEventHandler () {
  const password = document.querySelector('.js-password')
  const passwordIcon = document.querySelector('.js-password-icon')

  // If hidden is 0, then we invert it and make the password visible.
  if (hidden === 0) {
    hidden = 1
    password.type = 'text'
    passwordIcon.src = visibleEyeUrl
  } else {
    hidden = 0
    password.type = 'password'
    passwordIcon.src = invisibleEyeUrl
  }
}

function togglePasswordConfirmationEventHandler () {
  const password = document.querySelector('.js-password2')
  const passwordIcon = document.querySelector('.js-password-icon2')

  // If hidden is 0, then we invert it and make the password visible.
  if (hiddenConfirmation === 0) {
    hiddenConfirmation = 1
    password.type = 'text'
    passwordIcon.src = visibleEyeUrl
  } else {
    hiddenConfirmation = 0
    password.type = 'password'
    passwordIcon.src = invisibleEyeUrl
  }
}
