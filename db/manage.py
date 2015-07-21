#!/usr/bin/env python

import os

from migrate.versioning.shell import main


if __name__ == '__main__':
	db_uri = os.environ.get('DATABASE_URL')
	main(url=db_uri, debug='False', repository='db')
