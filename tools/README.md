## generate_env.py

This script generates two shell/bash scripts in the `environments` folder plus a shared config file. Run the appropriate script to setup the development environment to run the webapp either locally or on Heroku:

* Local config - Local database configuration
* Heroku config - Heroku database configuration
* common config - All the various API keys

By default, the script generates files using the current username. For example, if the current user is mephistopheles, the script will generate the following files:

* `mephistopheles.sh`
* `mephistopheles-local.sh`
* `mephistopheles-heroku.sh`

Usage:

```
usage: generate_env.py [-h] [--user USER] [--dbname DBNAME] [--dbuser DBUSER]
                       [--dbport DBPORT]
                       google_key forecast_key twillio_sid twillio_token
                       twillio_number

positional arguments:
  google_key       secret Google API key
  forecast_key     secret Forecast.io API key
  twillio_sid      Twillio SID
  twillio_token    Twillio auth token
  twillio_number   Twillio phone number

optional arguments:
  -h, --help       show this help message and exit
  --user USER      username for configuration files. Defaults to current user.
  --dbname DBNAME  database name. Defaults to "wheres"
  --dbuser DBUSER  database user name. Defaults to "wheres".
  --dbport DBPORT  database port. Defaults to 5432.
```
