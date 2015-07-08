# Where's Brendan

Personal project for storing [Spot](http://findmespot.com) GPS data, playing around with it, and displaying it in online.
This app runs a web dyno on [Heroku](http://heroku.com) and a worker dyno using [Celery](http://www.celeryproject.org/).

Many thanks to [Sinan](https://github.com/sinanuozdemir) for helping me get started.

## Development setup

### Prereqs

- [ ] Clone this project `git clone https://github.com/brendanebers/wheresbrendan.git`
- [ ] [virtualenv](https://pypi.python.org/pypi/virtualenv/1.8.2)
- [x] A dash of happiness with a sprinkle of rainbows


### Setup the Virtual Environment

In a shell, navigate to `wheresbrendan` and run

```bash
virtualenv
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

```bash
pip install -r requirements.txt
```

You'll need to do this anytime packages are added to or changed in (requirements.txt)[/requirements.txt].

### Environment Variables

This is a little awkward.
We don't really want to give you access to our database or let you play with our API keys,
so you'll need to supply your own environment variables.
See (config.py)[/config.py] for what's missing, or get a hold of us if you think you're special.
