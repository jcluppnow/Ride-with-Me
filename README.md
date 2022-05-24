# Ride with Me
[![Django CI](https://github.com/Ride-With-Me/ride_with_me/actions/workflows/django.yml/badge.svg)](https://github.com/Ride-With-Me/ride_with_me/actions/workflows/django.yml)
[![Vue CI](https://github.com/Ride-With-Me/ride_with_me/actions/workflows/vue.yml/badge.svg)](https://github.com/Ride-With-Me/ride_with_me/actions/workflows/vue.yml)

## Set up for development
* Clone repo
* Make a copy of `.env.example` and rename to `.env`
    * Update `SECRET_KEY=random-50-char-string`
    * Make a copy of the updated `.env` and rename to `.env.testing`
        * Update `.env.testing`
            * `ENV=testing`
            * `DB_ENGINE=sqlite`
* Run `docker compose up` in the project root directory (may take up to 10 minutes on initial builds)
* Visit localhost:8080

### Fix exec user process caused: no such file or directory
* Go to project root directory
* Run `find . -path ./src/application/node_modules -prune -o -type f -print0 | xargs -0 dos2unix`
* Set your text editor line ending to lf/unix style endings
* Rebuild the images `docker compose up web --build`

## Testing

## Switching between local and testing environments
If you are switching from local to testing or vice versa then you will need to add `--build`
when running docker compose up. This will switch the environment file for Django.

## Integration testing
* Run `docker compose -f test-docker-compose.yml up web --build` in the project root directory (may take up to 10 minutes on initial builds)
* Connect to the web image through the docker ui or through `docker exec -it <container id> /bin/bash`
* Run `dj test`

### Writing an integration test
* Create a test file in `src/application/tests`, ensure the filename starts with `test_`
* Create a test case class
* Create a test case function for each test

```python
from django.test import TestCase

class EventIntegrationTestCases(TestCase):

    def test_my_test_case():
        pass

```

## Cypress
* Run `find . -path ./src/application/node_modules -prune -o -type f -print0 | xargs -0 dos2unix`
* Ensure the web image is building and running correctly
    * Run `docker compose -f test-docker-compose.yml up web` in the project root directory (may take up to 10 minutes on initial builds)
### Headless/Docker
* Run `docker compose -f test-docker-compose.yml up` in the project root directory (may take up to 10 minutes on initial builds)
### Headed
* Run `docker compose -f test-docker-compose.yml up web` in the project root directory (may take up to 10 minutes on initial builds)
* `cd src/application`
* Run `npx cypress install`
    * Ensure nodejs is installed
* Run `npx cypress open`

### Writing a browser test
* Add html attribute `cytag` to elements that need to be selected within the test case
* Use `cy.cytag('cytag-attribute')` to select elements
* The database will dumped into fixtures. You may access them via `cy.fixture('filename')`
* Add the following to the top of each spec.js file to prevent mapworks from crashing tests
```
Cypress.on('uncaught:exception', (err, runnable) => {
  return false
})
```

### Adding data to the seed
* Edit seed_db function in `src/application/management/commands/seed.py`
* Ensure it does not affect any other tests

# Set up for Staging/Production
* Clone repo
* Make a copy of `.env.example` and rename to `.env`
* Change .env variables according to local environment
    * At least change `ENV=production`, `DEBUG=False`, `STATIC_ROOT=static` and `UPLOADS_ROOT=/var/www/uploads`
* Run `docker-compose -f prod-docker-compose.yml up`
* Ensure the Django server can be seen on `localhost:8080`
* Configure nginx to pass through to the Django server
    * `/static/` will need to point to `/var/www/static`
    * `/uploads/` will need to point to `/var/www/uploads`
    * Ensure the following configuration options are present in the server block, to enable WebSocket connections:
      ```nginx
      proxy_http_version 1.1;
      proxy_set_header Host $http_host;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      ```

# Directory structure explained
* `.docker` — the docker images and their boot scripts files except for the docker-compose files.
* `src` — the Django application
    * `/application` — all core code related to ride_with_me
        * `/css` — all css files for the application
        * `/cypress` — the cypress browser tests
        * `/factories` — the model factories used for seeding
        * `/management` — custom django commands
        * `/migrations` — the database migrations
        * `/models` — the models for the application
        * `/static` — images, static javascript and compiled javascript and css
        * `/templates` — html files for authentication and the single page application
        * `/tests` — the django integration tests
        * `/views` — the controllers/views for django
        * `/vue` — all front-end javascript, the core layout and the main javascript file
            * `/components` — vue components
            * `/router` — Vue router files
            * `/services` — files that define the API for the front-end
            * `/store` — Vuex state
                * `/models` — Vuex ORM models
                * `/modules` — Vuex ORM state modules that each model will use
            * `/views` — Vue pages for Vue router
