# Where's Brendan

Personal project for storing [Spot](http://findmespot.com) GPS data, playing around with it, and displaying it in online.
This app runs a web dyno on [Heroku](http://heroku.com) and a worker dyno using [Celery](http://www.celeryproject.org/).

Many thanks to [Sinan](https://github.com/sinanuozdemir) for helping me get started.

## Development setup

### Prereqs

- [ ] Clone this project `git clone https://github.com/brendanebers/wheresbrendan.git`
- [ ] [virtualenv](https://pypi.python.org/pypi/virtualenv/1.8.2)
- [ ] PostgreSQL
    - On Mac try [Postgres.app](http://postgresapp.com/)
- [x] A dash of happiness with a sprinkle of rainbows

#### VirtualEnv on Mac

- Install [Homebrew](http://brew.sh/)
- Ensure Homebrew apps are in the local PATH by adding the following to `~/.bash_profile`:

```
# Ensure user-installed binaries take precedence
export PATH=/usr/local/bin:$PATH
```

- Install Python 2: `brew install python`
- Install virtualenv: `pip install virtualenv`

If virtualenv fails to install with errors about *unsupported hash type*, try:

```
brew install openssl
brew link openssl --force
brew uninstall python
brew install python --with-brewed-openssl
```

### Setup the Virtual Environment

In a shell, navigate to `wheresbrendan` and run

```bash
virtualenv
```

On Mac:

```bash
virtualenv .
```

Now you'll be able to load a clean little environment without mucking with different package versions on your system.


### Activate Virtual Environment

**You must do this every time you develop in a new shell.**

If you're on a **\*nix**, you've got it easy, run:

```bash
source bin/activate
```

If you're an unfortunate soul running **Windows** *cough* Brendan *cough*. You'll need to take care of execution policies ([directions here](https://pypi.python.org/pypi/virtualenv/1.8.2#activate-script)) and then run:

```bash
.\Scripts\activate
```

### Installing Packages

Now that you're in a virtual environment, get all the packages!

If you're on Mac, you need to configure the path to pg_config so that the installation of `psycopg2` can find it. Assuming you used Postgres.app, add the following to `~/.bash_profile`:

`PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"`

Adjust the path *before* running `pip`.

```bash
pip install -r requirements.txt
```

You'll need to do this anytime packages are added to or changed in [requirements.txt](/requirements.txt).


### Environment Variables

We don't really want to give you access to our database or let you play with our API keys,
so you'll need to supply your own environment variables.
See [scripts/generate_env.py](scripts/generate_env.py) and [scripts/README.md](scripts/README.md) for a tool to automatically generate environment-specific configuration scripts. 

## Database

### Setting up the Database
After installing the packages and loading your environment variables, create the local database user and database:

```
createuser -DELSP wheres_admin
createdb -O wheres_admin wheres_local
```

On Mac, the path to the Postgres utilities will be something like: `/Applications/Postgres.app/Contents/Versions/9.4/bin`.

Next, initialize the Migrate tables:

```
python scripts/db_create.py
```

### Apply Database Migrations

To apply all of the database migrations that have not been applied to the current database, run:

```
python db/manage.py upgrade
```

### Model Migrations
You can make changes to the DB model classes and easily generate new database migrations, without having to manually define the tables. Make changes to `app/models.py` and then run:

```
python scripts/db_migrate_models.py
```

That will generate a new migration script in `db/versions`. If you want to test your changes, be certain you are **NOT** pointing at the live database and run:

```
python db/manage.py test
```

Don't forget to apply the migrations, as shown above.

---
Content of this repository is copyright Brendan Ebers, 2015
