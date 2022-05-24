module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backgroundColor: {
        //Any colors we need can be added here with the format 'name': 'hex-code'.
        'rwmOrange': '#FCA311',   //Ride with Me orange on Figma.
        'rwmDarkBlue': '#14213D', //Purple Accent on Figma.
        'rwmLighterBlue': '#283F70',
        'rwmTextGray': '#A1A1AA',
      },
      maxWidth: {
        '3/2xl': '39rem',
        'xxs': '15rem'
      },
      minHeight: {
        '3': '3rem'
      },
    },
    fontFamily: {
      'display': ['Inter'],
      'body': ['Inter']
    },
  },
  variants: {
    extend: {
      dropShadow: ['hover'],
      backgroundColor: ['hover', 'active'],
      textColor: ['hover', 'active']
    },
  },
  plugins: [],
}
