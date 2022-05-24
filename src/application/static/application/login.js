let hidden = 0

function togglePasswordEventHandler () {
  //Fetch password and icons from dom.
  const password = document.querySelector('.js-password')
  const passwordIcon = document.querySelector('.js-password-icon')

  // If hidden is 0, then we invert it and make the password visible.
  if (hidden === 0) {
    //Set condition.
    hidden = 1
    //Reverse the type.
    password.type = 'text'
    //Update the icon.
    passwordIcon.src = visibleEyeUrl
  } else {
    //Set condition.
    hidden = 0
    //Reverse the type.
    password.type = 'password'
    //Update the icon.
    passwordIcon.src = invisibleEyeUrl
  }
}
