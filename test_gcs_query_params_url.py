try:
    from mock import patch, MagicMock

except ImportError:
    from unittest.mock import patch, MagicMock

import sys
import os

sys.modules["Foundation"] = MagicMock()

from middleware_gcs import gcs_query_params_url  # noqa E402


@patch("middleware_gcs._read_cfpref_keystore")
@patch("middleware_gcs.time")
def test_gcs_query_params_url(time_mock, cfpref_mock):
    time_mock.mktime.return_value = 1572662148
    cfpref_mock.return_value = (None, None)
    test = gcs_query_params_url("http://test")

    assert test == (
        "https://storage.googleapis.com?GoogleAccessId=readonly@double.iam.gserviceaccount.com&Expires=1572662148&Signature=vE7BV6l%2FulKh9Iz71GqvOpn6wiDU7m5PNQfvkcISSWLa4pI2Qqx4UTSBnJNEO2HAKtLpHo%2BM9xqFErdsxczrpjaT2oboF3oCqd8nqVa3MT31OtWyIY3ENlK%2BVO7BLncczbe46PdRed4F5VW4DWI4QBmEPKB%2FtcNVEtvHQ4aOBDnEe5Q96sD2wRaM5mG4aSnmDsMClSBvAjLKWmpCIEx8spVA5yMqCRceDrEQNRfBf1qDtKExhcne2CFNenBzWjwKwFHlvVFOzUppcrxTpNHmf1%2FKELpK%2BDqJVaigYrRmPI%2Bnl%2B%2BqrLL2kCk5%2BbbNp%2BfOeh5qcov4tplUzN28pEVYfw%3D%3D"
    )


@patch("middleware_gcs._read_cfpref_keystore")
@patch("middleware_gcs.time")
def test_gcs_query_params_url_doesnt_read_json_when_prefs_present(time_mock, cfpref_mock):
    time_mock.mktime.return_value = 1572662148
    os.remove("gcs.json")
    cfpref_mock.return_value = ("readonly@double.iam.gserviceaccount.com", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQDHKwHZ7i5V+w6U\n0ku/XhYE2/PYgV9Yrgtso3LNaA4uHJjvO5JCdcM7wje1hLKI6ANZfQ/bKXghPq8M\nSVgfUZUYOe97ztmJlVe+LvhIyTY9eyk9NDBytAvrARKn+ceGiac8S3QUDXYlGif1\nUIUdFsuLKSbtnibOWztV4gjYFE/Yw9mrjADq4S4e/8BZVSEpPOct2hcEXR+1ixzG\nlwFaUY5WlaxonazyKZ40p+Evu6T4fCLP71Uo9ewXjeHy7vqL4dHpfxVBXecUVaMK\n5XC0FAKNTZDrEjbVqXmSNRnOw46DjYyOYfvaOFhBoSBpRX/gzOZgyZsvqqgAl3Qr\nTXe3xdm5AgMBAAECggEBAJuYNq8Jiztykfajv7d2Cl+rcfm/QDyoY5ZwrpxX4VQW\n1Ud4U5AGLgq+dQUi8NNR5mP/9uYxpH7cWKaRmf2Fn6O4hyZC9+GrQUv7p849G1m2\noQYGgp7pl7H1OZzu3vh1C6hoDfwodBcSMwtL52JNT6Cc+qOB/TETRuyWVHByldpx\n7N/Ud7hfjV2bJxFG5d33Io0lYB6l/179jZCLow33hkSfQBfsgdP75WWl8nB7pLMj\nbwJlu3j2NhMIXRIWOuc+QPP13qbg+nqnOlBQjoh7UYqI2bACYyERFpWYygsTQR1N\nrLE8kbsj91twRLboEpt+gKY0veItlLIp3zsNEKkMmh0CgYEA9N8Twb6dFX+BYs0g\n0NaXSHx/sFZRfIzFbvIN/HbjTGxvE32e3Fq3FtF/sgelV3flUBgN+tRKUjhNd/wD\nYHB1wvGLcPe5cyQdFGsaU2mZPocwJ8FYm/vUZK1LNw2HTyQ/ELntQDfAzX6DJ6tM\n9cPYB3lW5VR2bYkZ1gqE+KjIPwsCgYEA0DgzOkia7d8Tx6wvZd+6zX9OuXs6l9le\n+q+sarKG3y1POsPmz4JVVh0YCJBNwgaSM8k4z2ogl9nPL6qIRmxRYci7UAWz8kcV\nhs+zMyBMqioDfTqlHSGVKYBMvpb873Pz+hpSL/u9fvR1vNM1E/96+40VmR25Fiwd\nyzltXGmNFMsCgYEA03IZrlA5doneoQE+V/clNUuEOzGeNa2dArtzhlDm32Q22h68\nYczXkpWe7Y0aohf+5JWQ5MoRz0Oc6YGtLMaPeaF35jmTYrCJh8sgNWzXDh5QX9Pd\n/vuLINBfRY+iCp3i8z+Jdc1u6ENZX5TU5NeTIIkPlwHDLbyYmbIFtm6QU5cCgYEA\nhdO5STqlKUH5qppGlImpvK6YYKqNTE/Ptfv3K1S3TvYGOFT1ImY4hvKIIejtsUkb\n6uDn/JfPfwnlGlPW5rxzyg+EJLiloZCCi3UvTiryW2RJfdGVkhWlk1j8+np880Jp\ni1QjguegMdrZWZW+Ra4s00UonpL2BQQx2g589ap5nOUCgYEAqlnyM6s4BhNSB2aj\nzgq3xJsxNkwulIeNu8+oic65G/I5VhTTwsOE9sM97kEWJ3XZorIAnEK/LhQhADpF\nvfEjbm0riFBGrr97mqjpZxNbnrgXVEpwCTw1sPzdOjZ0/iHjA9Q+O8Euuq1ODzxA\naC+Vqg2/bx7djcVtTp0KqyFwuHY=\n-----END PRIVATE KEY-----\n")
    test = gcs_query_params_url("http://test")

    assert test == (
        "https://storage.googleapis.com?GoogleAccessId=readonly@double.iam.gserviceaccount.com&Expires=1572662148&Signature=vE7BV6l%2FulKh9Iz71GqvOpn6wiDU7m5PNQfvkcISSWLa4pI2Qqx4UTSBnJNEO2HAKtLpHo%2BM9xqFErdsxczrpjaT2oboF3oCqd8nqVa3MT31OtWyIY3ENlK%2BVO7BLncczbe46PdRed4F5VW4DWI4QBmEPKB%2FtcNVEtvHQ4aOBDnEe5Q96sD2wRaM5mG4aSnmDsMClSBvAjLKWmpCIEx8spVA5yMqCRceDrEQNRfBf1qDtKExhcne2CFNenBzWjwKwFHlvVFOzUppcrxTpNHmf1%2FKELpK%2BDqJVaigYrRmPI%2Bnl%2B%2BqrLL2kCk5%2BbbNp%2BfOeh5qcov4tplUzN28pEVYfw%3D%3D"
    )
