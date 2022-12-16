# Google Calendar Metrics Service
The goal of this project is to demonstrate a simple Django application (using `DRF`) that integrates the Google Calendar API. Using this app, a user can create an entry into the `Postgres` database, and in doing so, will create a unique watch channel (web hook) with the Google Calendar API. After initial creation, if the user then edits their own Google Calendar, common metrics (the next 10 events) will be re-calculated and printed to the console in real-time. 


# Setting Up the Google Calendar API
## Preliminary Steps
1. Install `ngrok`: this allows us to link our localhost to the internet (requirement for Google API webhooks).
2. Install and configure [mkcert](https://timonweb.com/django/https-django-development-server-ssl-certificate/): allows Django to use `https` instead of `http` (requirement of Google API).
3. Setup a [Google service account](https://console.cloud.google.com/iam-admin/serviceaccounts/details/115677740474491534164?project=leafy-future-343501&supportedpurview=project)
4. Go to [Google Console](https://console.cloud.google.com/apis/credentials?project=leafy-future-343501)
    * Create an OAuth 2.0 Client under the `Credentials` tab and add `https://localhost:8080/` as an authorized redirect URI (exactly as is).
    * Make sure test user is added under the `OAuth consent screen` tab.
    * Download `credentials.json` for Google API usage and store in the root directory.
5. If needed:
    * You can manually get the API access token at [this link](https://developers.google.com/oauthplayground/).
    * [Documentation](https://developers.google.com/calendar/api/guides/push?hl=en) for creating a Google API webhook.

# Running the App
## Get Google Calendar ID
Go to the [Google Calendar](https://calendar.google.com/calendar) site, go to settings for one of the calendars, then select the `Integrate calendar` section. Set the Calendar ID as an environment variable with variable name `CAL_ID`.

## Run `ngrok`
Begin by running: `ngrok http --host-header="localhost:8000" https://localhost:8000`

This will create a public-facing URL that is linked to the localhost server running Django. Copy the URL given, you will need it for running this Django app.

## Run Django
Before running Django, check the `settings.py` module and replace the variable `CHANNEL_DESTINATION` with the `ngrok`-generated URL.

Once that is done, run in another terminal: `python manage.py runserver_plus --cert-file cert.pem --key-file key.pem`.

This will run the local django server using `https`.
