#!/bin/bash


## LOCALDEV settings for django `x_project`
##
## This file is loaded by `env/bin/activate` when running locally...
## ...and by `project/config/passenger_wsgi.py` on our servers.
##
## When deploying on our servers, copy this file to the appropriate place, edit it, 
## ...and point to it from activate and the apache <Location> entry.


## ============================================================================
## standard project-level settings
## ============================================================================

export DJ_TMPLT32__SECRET_KEY="example_secret_key"

export DJ_TMPLT32__DEBUG_JSON="true"

export DJ_TMPLT32__ADMINS_JSON='
    [
      [
        "exampleFirst exampleLast",
        "example@domain.edu"
      ]
    ]
    '

export DJ_TMPLT32__ALLOWED_HOSTS_JSON='["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "localhost:8000"]'  # must be json

export DJ_TMPLT32__DATABASES_JSON='
    {
      "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "HOST": "",
        "NAME": "../DB/x_project_files.sqlite3",
        "PASSWORD": "",
        "PORT": "",
        "USER": ""
      }
    }
    '

export DJ_TMPLT32__STATIC_URL="/static/"
export DJ_TMPLT32__STATIC_ROOT="/static/"

export DJ_TMPLT32__EMAIL_HOST="localhost"
export DJ_TMPLT32__EMAIL_PORT="1026"  # will be converted to int in settings.py
export DJ_TMPLT32__SERVER_EMAIL="donotreply_x-project@domain.edu"

export DJ_TMPLT32__LOG_PATH="../logs/x_project.log"
export DJ_TMPLT32__LOG_LEVEL="DEBUG"

export DJ_TMPLT32__CSRF_TRUSTED_ORIGINS_JSON='["localhost", "127.0.0.1"]'

## https://docs.djangoproject.com/en/3.2/topics/cache/
## - TIMEOUT is in seconds (0 means don't cache); CULL_FREQUENCY defaults to one-third
export DJ_TMPLT32__CACHES_JSON='
{
  "default": {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": "../cache_dir",
    "TIMEOUT": 0,
    "OPTIONS": {
        "MAX_ENTRIES": 1000
    }
  }
}
'

## ============================================================================
## app
## ============================================================================

export DJ_TMPLT32__README_URL="https://github.com/birkin/django_template_32_project/blob/main/README.md"

## auth -------------------------------------------------------------

export DJ_TMPLT32__SUPER_USERS_JSON='[
]'

export DJ_TMPLT32__STAFF_USERS_JSON='
[
  "eppn@domain.edu"
]'

export DJ_TMPLT32__STAFF_GROUPER_GROUP="the:group"

export DJ_TMPLT32__TEST_META_DCT_JSON='{
  "Shibboleth-eppn": "eppn@brown.edu",
  "Shibboleth-brownNetId": "First_Last",
  "Shibboleth-mail": "first_last@domain.edu",
  "Shibboleth-givenName": "First",
  "Shibboleth-sn": "Last",
  "Shibboleth-isMemberOf": "aa:bb:cc;dd:ee:ff;the:group;gg:hh"
}'

export DJ_TMPLT32__LOGIN_PROBLEM_EMAIL="x_project_problems@domain.edu"


## end --------------------------------------------------------------
