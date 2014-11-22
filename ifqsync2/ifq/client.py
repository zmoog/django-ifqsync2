# -*- config: utf-8 -*-

import requests


PAGE_LOGIN = 'https://shop.ilfattoquotidiano.it/login/?action=login'


class Client(object):
	"""
	Il Fatto Quotidiano website Client.
	"""

	def __init__(self, username, password):

		self._username = username
		self._password = password

		self._session = requests.Session()


	def login(self):
		"""
		Log into the website using the given credentials.
		"""

		payload = {
			'log': self._username, 
			'pwd': self._password,
			'testcookie': 1, 
			'instance': '', 
			'redirect_to': '', 
			'wp-submit': 'Log in'
		}

		response = self._session.post(PAGE_LOGIN, data=payload)


	def is_logged(self):
		"""
		Check if we're logged in the current session.

		The actual check is based on the presence of a cookie named with 
		the 'wordpress_logged_in' prefix.

		I don't really know if it's adeguate, but is working.

		"""
		return any(
			key.startswith('wordpress_logged_in') for key in self._session.cookies.iterkeys()
			)

