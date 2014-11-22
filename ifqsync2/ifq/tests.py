from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from .client import Client

import os


def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


class ClientTest(TestCase):
	"""
	Test the IFQ client operations
	"""

	def test_login_on_the_website(self):

		client = Client(username=get_env_variable('IFQ_USERNAME'), password=get_env_variable('IFQ_PASSWORD'))

		self.assertFalse(client.is_logged())

		client.login()

		self.assertTrue(client.is_logged())
    
