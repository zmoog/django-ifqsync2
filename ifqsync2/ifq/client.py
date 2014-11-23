# -*- config: utf-8 -*-

import requests
import os
import logging

URL_LOGIN = 'https://shop.ilfattoquotidiano.it/login/?action=login'
URL_LOGOUT = 'http://www.ilfattoquotidiano.it/logout/'
URL_SEARCH = 'https://shop.ilfattoquotidiano.it/wp-content/plugins/ifq-searchpdf/get_risultatopdf.php?id=%d-%m-%Y'
URL_DOWNLOAD = 'http://pdf.ilfattoquotidiano.it/openpdf/?n=%Y%m%d'

CANARY_COOKIE = 'disqus-sso-email' # or 'wordpress_logged_in'


logger = logging.getLogger(__name__)


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

        response = self._session.post(URL_LOGIN, data=payload)


    def logout(self):
        """
        Logout from the website using the appropriate URL.
        """

        self._session.get(URL_LOGOUT)


    def is_logged(self):
        """
        Check if we're logged in the current session.

        The actual check is based on the presence of a cookie named with 
        the 'wordpress_logged_in' prefix.

        I don't really know if it's adeguate, but is working.

        """
        return any(
            key.startswith(CANARY_COOKIE) for key in self._session.cookies.iterkeys()
            )


    def exists_issue(self, pub_date):
        """
        Search th IFQ archive on the web for the issue published in the 
        given pub_date.

        The pub_date parameter MUST be a 'datetime.date'.

        """

        search_url = self._build_search_url(pub_date)
        download_url = self._build_download_url(pub_date)

        response = self._session.get(search_url)

        print('download_url: %s' % (download_url))
        print('response.text: %s' % (response.text))

        if response.status_code == 200 and download_url in response.text:
            return True

        return False



    def download(self, pub_date):
        """
        """

        import tempfile

        download_url = self._build_download_url(pub_date)

        logger.info('download_url: %s' % (download_url))
        print('download_url: %s' % (download_url))

        response = self._session.get(download_url, stream=True)

        assert(response.headers['Content-Type'] == 'application/pdf')


        print('headers: %s' % (response.headers))

        assert(response.status_code == 200)

        local_filename = os.path.join(tempfile.gettempdir(), pub_date.strftime('ifq-%Y%m%d.pdf'))

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()


        assert(os.path.getsize(local_filename) == int(response.headers['Content-Length']))

        return local_filename



    def _build_search_url(self, pub_date):
        return pub_date.strftime(URL_SEARCH)

    def _build_download_url(self, pub_date):
        return pub_date.strftime(URL_DOWNLOAD)