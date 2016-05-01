"""
Generate signed URLc for your munki repo
This module is using munki middleware
https://github.com/munki/munki/wiki/Middleware

Alot of this code was lifted from google's examples or from gsutil.

"""


import base64
import datetime
import time
import json
import os

from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import load_privatekey
from OpenSSL.crypto import sign

from urlparse import urlparse
from urllib import quote_plus

#Our json keystore file
JSON_FILE = 'gcs.json'
JSON_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), JSON_FILE))

def uri_from_url(url):
    parse = urlparse(url)
    return parse.path


def read_json_keystore():
    ks = json.loads(open(JSON_FILE_PATH, 'rb').read())

    if 'client_email' not in ks or 'private_key' not in ks:
        print 'JSON keystore doesn\'t contain required fields'

    client_email = ks['client_email']
    key = load_privatekey(FILETYPE_PEM, ks['private_key'])

    return key, client_email


def gen_signed_url(gcs_path):
    """Construct a string to sign with the provided key and returns \
    the complete url."""
    expiration = (datetime.datetime.now() + datetime.timedelta(minutes=15))
    expiration = int(time.mktime(expiration.timetuple()))

    key, client_id = read_json_keystore()
    canonicalized_resource = '{}'.format(gcs_path)

    tosign = ('{}\n{}\n{}\n{}\n{}'
              .format('GET', '', '',
                      expiration, canonicalized_resource))
    signature = base64.b64encode(sign(key, tosign, 'RSA-SHA256'))

    final_url = ('https://storage.googleapis.com{}?'
                 'GoogleAccessId={}&Expires={}&Signature={}'
                 .format(gcs_path, client_id, expiration,
                         quote_plus(str(signature))))

    return final_url


def gcs_query_params_url(url):
    file_path = uri_from_url(url)
    url = gen_signed_url(file_path)
    return url

def process_request_options(options):
    """Make changes to options dict and return it."""
    if 'storage.googleapis.com' in options['url']:
        options['url'] = gcs_query_params_url(options['url'])
    return options
