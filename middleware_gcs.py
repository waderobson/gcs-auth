#!/usr/local/munki/munki-python
"""
Generate signed URLs for your munki repo
This module is using munki middleware
https://github.com/munki/munki/wiki/Middleware
Alot of this code was lifted from google's examples or from gsutil.
"""

import base64
import datetime
import json
import time
import os
from asn1crypto import pem, keys
from oscrypto.asymmetric import rsa_pkcs1v15_sign, load_private_key
from urllib.parse import urlparse, quote_plus
from Foundation import CFPreferencesCopyAppValue

__version__ = '3.0'
# Our json keystore file
JSON_FILE = 'gcs.json'
JSON_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), JSON_FILE))

BUNDLE_ID = 'ManagedInstalls'
def pref(pref_name):
    """Return a preference. See munkicommon.py for details
    """
    pref_value = CFPreferencesCopyAppValue(pref_name, BUNDLE_ID)
    return pref_value

def uri_from_url(url):
    parse = urlparse(url)
    return parse.path

def get_managed_keys():
    # Use base64 encoded version of the full SA json
    if pref('GCSJson'):
        full_json = json.loads(base64.b64decode(pref('GCSJson')))
        client_email = full_json['client_email']
        key = full_json['private_key']
    # Or just the keys we need
    # Private key is base64 encoded to preserve formatting, not really for security
    elif pref('GCSClientEmail') and pref('GCSPrivateKey'):
        client_email = pref('GCSClientEmail')
        key = base64.b64decode(pref('GCSPrivateKey')).decode('utf-8')
    return key, client_email


def get_json_keys():
    # Load SA from local json file
    ks = json.loads(open(JSON_FILE_PATH, 'rb').read().decode('utf-8'))
    if "client_email" not in ks or "key" not in ks:
        print('JSON keystore doesn\'t contain required fields')
        return None, None
    client_email = ks['client_email']
    key = ks['private_key']
    return key, client_email

def get_keys():
    # User mangaged prefs if available
     key, client_email = get_managed_keys()
     if not all([key, client_email]):
         key, client_email = get_json_keys()
     return key, client_email


def read_json_keystore():
    key, client_email = get_keys()
    
    # Validate private key and load it
    private_key = key.encode()
    if pem.detect(private_key):
        type_name, headers, der_bytes = pem.unarmor(private_key)
    else:
        print("No PEM Private Key Found")
    
    object = keys.PrivateKeyInfo.load(der_bytes)
    key = load_private_key(object, password=None)

    return key, client_email


def gen_signed_url(gcs_path):
    """Construct a string to sign with the provided key and returns \
    the complete url."""
    expiration = (datetime.datetime.now() + datetime.timedelta(minutes=15))
    expiration = int(time.mktime(expiration.timetuple()))

    key,client_id = read_json_keystore()
    canonicalized_resource = '{}'.format(gcs_path)

    tosign = ('{}\n{}\n{}\n{}\n{}'
              .format('GET', '', '',
                      expiration, canonicalized_resource))

    # Sign the message with the private key
    signature = base64.b64encode(rsa_pkcs1v15_sign(key, tosign.encode('utf-8'), 'sha256')).decode('utf-8')

    # Build the url
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