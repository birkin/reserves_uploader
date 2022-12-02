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

export RSRVS_UPLDR__SECRET_KEY="example_secret_key"

export RSRVS_UPLDR__DEBUG_JSON="true"

export RSRVS_UPLDR__ADMINS_JSON='
    [
      [
        "exampleFirst exampleLast",
        "example@domain.edu"
      ]
    ]
    '

export RSRVS_UPLDR__ALLOWED_HOSTS_JSON='["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "localhost:8000"]'  # must be json

export RSRVS_UPLDR__DATABASES_JSON='
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

export RSRVS_UPLDR__STATIC_URL="/static/"
export RSRVS_UPLDR__STATIC_ROOT="/static/"

export RSRVS_UPLDR__EMAIL_HOST="localhost"
export RSRVS_UPLDR__EMAIL_PORT="1026"  # will be converted to int in settings.py
export RSRVS_UPLDR__SERVER_EMAIL="donotreply_x-project@domain.edu"

export RSRVS_UPLDR__LOG_PATH="../logs/x_project.log"
export RSRVS_UPLDR__LOG_LEVEL="DEBUG"

export RSRVS_UPLDR__CSRF_TRUSTED_ORIGINS_JSON='["localhost", "127.0.0.1"]'

## https://docs.djangoproject.com/en/3.2/topics/cache/
## - TIMEOUT is in seconds (0 means don't cache); CULL_FREQUENCY defaults to one-third
export RSRVS_UPLDR__CACHES_JSON='
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

export RSRVS_UPLDR__README_URL="https://github.com/birkin/django_template_32_project/blob/main/README.md"

## auth -------------------------------------------------------------

export RSRVS_UPLDR__SUPER_USERS_JSON='[
]'

export RSRVS_UPLDR__STAFF_USERS_JSON='
[
  "eppn@domain.edu"
]'

export RSRVS_UPLDR__STAFF_GROUPER_GROUP="the:group"

export RSRVS_UPLDR__TEST_META_DCT_JSON='{
  "Shibboleth-eppn": "eppn@brown.edu",
  "Shibboleth-brownNetId": "First_Last",
  "Shibboleth-mail": "first_last@domain.edu",
  "Shibboleth-givenName": "First",
  "Shibboleth-sn": "Last",
  "Shibboleth-isMemberOf": "aa:bb:cc;dd:ee:ff;the:group;gg:hh"
}'

export RSRVS_UPLDR__LOGIN_PROBLEM_EMAIL="x_project_problems@domain.edu"


## end --------------------------------------------------------------
