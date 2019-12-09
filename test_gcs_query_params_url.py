import datetime

try:
    from datetime import timezone
except ImportError:
    import pytz as timezone
try:
    from mock import patch

except ImportError:
    from unittest.mock import patch

from middleware_gcs import gcs_query_params_url  # noqa E402


@patch("middleware_gcs.time")
def test_gcs_query_params_url(time_mock):
    time_mock.mktime.return_value = 1572662148
    test = gcs_query_params_url('http://test')

    assert test == ('https://storage.googleapis.com?GoogleAccessId=readonly@double.iam.gserviceaccount.com&Expires=1572662148&Signature=vE7BV6l%2FulKh9Iz71GqvOpn6wiDU7m5PNQfvkcISSWLa4pI2Qqx4UTSBnJNEO2HAKtLpHo%2BM9xqFErdsxczrpjaT2oboF3oCqd8nqVa3MT31OtWyIY3ENlK%2BVO7BLncczbe46PdRed4F5VW4DWI4QBmEPKB%2FtcNVEtvHQ4aOBDnEe5Q96sD2wRaM5mG4aSnmDsMClSBvAjLKWmpCIEx8spVA5yMqCRceDrEQNRfBf1qDtKExhcne2CFNenBzWjwKwFHlvVFOzUppcrxTpNHmf1%2FKELpK%2BDqJVaigYrRmPI%2Bnl%2B%2BqrLL2kCk5%2BbbNp%2BfOeh5qcov4tplUzN28pEVYfw%3D%3D')