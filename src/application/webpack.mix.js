let mix = require('laravel-mix')
require('mix-env-file')
require('laravel-mix-eslint')
require('mix-tailwindcss')
require('laravel-mix-svg-vue')

mix.env('../.env.readonly')

mix.js('vue/app.js', 'static/application/compiled')
.vue()
.eslint({
    fix: true,
    extensions: ['js','vue']
  })
  .postCss('css/app.css', 'static/application/compiled')
  .tailwind('./tailwind.config.js')
.scripts('vue/service-worker/sw.js', 'templates/application/sw.js')
.setPublicPath('')
.alias({
    '@': '/vue',
}).svgVue({
    svgPath: 'vue/vectors'
});

if (process.env.NODE_ENV === 'development') {
    mix.sourceMaps();
}
