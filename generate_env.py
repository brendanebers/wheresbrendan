#!/bin/env python
"""Generates environment configuration files for the current user."""

import argparse
import getpass
import os
import platform


def ParseArgs():
	"""Parses command line arguments."""
	parser = argparse.ArgumentParser()
	parser.add_argument('--user', default=getpass.getuser(),
		help='username for configuration files. Defaults to current user.')

	parser.add_argument('--dbname', default='wheres', help='database name. Defaults to "wheres"')
	parser.add_argument('--dbuser', default='wheres',
		help='database user name. Defaults to "wheres".')
	parser.add_argument('--dbport', type=int, default=5432,
		help='database port. Defaults to 5432.')

	parser.add_argument('google_key', default='GOOGLE', help='secret Google API key')
	parser.add_argument('forecast_key', default='FORECASTIO', help='secret Forecast.io API key')

	parser.add_argument('twillio_sid', default='TWILLIO_SID', help='Twillio SID')
	parser.add_argument('twillio_token', default='TWILLIO_TOKEN', help='Twillio auth token')
	parser.add_argument('twillio_number', default='TWILLIO_NUMBER', help='Twillio phone number')

	return parser.parse_args()


def GetStringKeyValue(is_windows, key, value):
	"""Creates an os-specific key/value environment variable.

	Args:
		is_windows: boolean indicating whether or not this running on Windows
		key: environment variable name
		value: environment variable value

	Returns:
		String in the format of 'set FOO="bar"' or 'export FOO="bar"'
	"""		
	export = 'set' if is_windows else 'export'
	return '%s %s="%s"' % (export, key, value)


def Writeln(f, text):
	"""Writes a line of text including the platform appropriate new line separator(s).

	Args:
		f: open text file
		text: string to write to the file
	"""
	f.write(text)
	f.write('\n')


def WriteShellFileHeader(f):
	"""Writes the appropriate Bash shell header line to a shell script file.

	Args:
		f: open file
	"""
	Writeln(f, '!/bin/sh')


def WriteEnvConfigBody(f, is_windows, args, host, dbname):
	"""Writes the body of an environment specific config file.

	Args:
		f: open file
		is_windows: boolean indicating whether or not this running on Windows
		args: command line arguments parsed by ArgumentParser
		host: name of database host
		dbname: name of the database
	"""
	Writeln(f, '# Database')
	
	database_url = ('postgresql://%s:PASSWORD@%s:%d/%s' % 
		(args.dbuser, host, args.dbport, dbname))
	Writeln(f, GetStringKeyValue(is_windows, 'DATABASE_URL', database_url))

	Writeln(f, '')

	if is_windows:
		Writeln(f, 'call %s.bat' % args.user)
	else:
		Writeln(f, 'DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )')
		Writeln(f, 'source $DIR/%s.sh' % args.user)


def WriteMainConfigBody(f, is_windows, args):
	"""Writes the body of the primary config file.

	Args:
		f: open file
		is_windows: boolean indicating whether or not this running on Windows
		args: command line arguments parsed by ArgumentParser
	"""
	Writeln(f, '# Flask')
	Writeln(f, GetStringKeyValue(is_windows, 'SECRET_KEY', args.user))
	Writeln(f, '')
	Writeln(f, '# Celery')
	Writeln(f, GetStringKeyValue(is_windows, 'CELERY_BROKER_URL', 'sqla+$DATABASE_URL'))
	Writeln(f, GetStringKeyValue(is_windows, 'CELERY_RESULT_BACKEND', 'db+$DATABASE_URL'))
	Writeln(f, '')
	Writeln(f, '# Google API')
	Writeln(f, GetStringKeyValue(is_windows, 'GOOGLE_API_KEY', args.google_key))
	Writeln(f, '')
	Writeln(f, '# Forecast IO')
	Writeln(f, GetStringKeyValue(is_windows, 'FORECAST_IO_API_KEY', args.forecast_key))
	Writeln(f, '')
	Writeln(f, '# Twillio')
	Writeln(f, GetStringKeyValue(is_windows, 'TWILIO_ACCOUNT_SID', args.twillio_sid))
	Writeln(f, GetStringKeyValue(is_windows, 'TWILIO_AUTH_TOKEN', args.twillio_token))
	Writeln(f, GetStringKeyValue(is_windows, 'TWILIO_NUMBER', args.twillio_number))
	Writeln(f, '')

def main():
	args = ParseArgs()

	is_windows =  platform.system().startswith('Windows')
	file_extension = 'bat' if is_windows else 'sh'

	filename = '%s.%s' % (args.user, file_extension)
	pathname = os.path.join('environments', filename)
	print 'Creating main environment config in %s' % pathname
	with open(pathname, 'w') as f:
		if not is_windows:
			WriteShellFileHeader(f)

		WriteMainConfigBody(f, is_windows, args)

	filename = '%s-local.%s' % (args.user, file_extension)
	pathname = os.path.join('environments', filename)
	print 'Creating local environment config in %s' % pathname
	with open(pathname, 'w') as f:
		if not is_windows:
			WriteShellFileHeader(f)

		WriteEnvConfigBody(f, is_windows, args, 'localhost', '%s_local' % args.dbname)

	filename = '%s-heroku.%s' % (args.user, file_extension)
	pathname = os.path.join('environments', filename)
	print 'Creating Heroku environment config in %s' % pathname
	with open(pathname, 'w') as f:
		if not is_windows:
			WriteShellFileHeader(f)

		WriteEnvConfigBody(f, is_windows, args, 'REMOTE_HOST', args.dbname)


if __name__ == '__main__':
	main()