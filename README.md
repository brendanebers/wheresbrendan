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

This is a little awkward.
We don't really want to give you access to our database or let you play with our API keys,
so you'll need to supply your own environment variables.
See [config.py](/config.py) for what's missing, or get a hold of us if you think you're special.


Content of this repository is copyright Brendan Ebers, 2015
