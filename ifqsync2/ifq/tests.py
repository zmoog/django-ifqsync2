from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from .client import Client

import os
from datetime import date


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

    def setUp(self):

        self.client = Client(
            username=get_env_variable('IFQ_USERNAME'), 
            password=get_env_variable('IFQ_PASSWORD')
        )


    def tearDown(self):
        # TODO: logout maybe?
        self.client = None       


    def test_login_on_the_website(self):

        self.assertIs(self.client.is_logged(), False)

        self.client.login()

        self.assertIs(self.client.is_logged(), True)
    

    def test_logout_from_the_website(self):
        
        self.assertIs(self.client.is_logged(), False)

        self.client.login()

        self.assertIs(self.client.is_logged(), True)

        self.client.logout()

        self.assertIs(self.client.is_logged(), False)


    def test_search_for_existing_issue(self):
        """
        """

        self.client.login()

        result = self.client.exists_issue(pub_date=date(2014, 11, 23))

        self.assertIsNotNone(result)
        
        self.assertIs(result, True)


    def test_search_for_a_not_existing_issue(self):
        """
        """

        self.client.login()

        result = self.client.exists_issue(pub_date=date(2001, 9, 11))

        self.assertIsNotNone(result)
        
        self.assertIs(result, False)


    def test_download_issue(self):
        
        self.client.login()

        file_path = self.client.download(pub_date=date(2014, 11, 6)) # 4,1 MB PDF file

        self.assertTrue(os.path.isfile(file_path))

        self.assertEqual(os.path.getsize(file_path), 4303574)

