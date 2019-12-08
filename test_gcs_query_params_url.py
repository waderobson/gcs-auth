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


@patch("middleware_gcs.datetime")
def test_gcs_query_params_url(datetime_mock):
    datetime_mock.datetime.now.return_value = datetime.datetime(2019, 11, 1, 18, 20, 48, 963798, tzinfo=timezone.utc)
    datetime_mock.timedelta.return_value = datetime.timedelta(0, 900)
    test = gcs_query_params_url('http://test')

    assert test == ('https://storage.googleapis.com?'
                    'GoogleAccessId=readonly@double.iam.gserviceaccount.com&'
                    'Expires=1572633348&'
                    'Signature=b%27FAB3JUC1eUmF1z%2FJqa6Nxc0ksqn5luIqyv%2FK'
                    'BxR%2FN3u0P4nkIMK8whKZ0rtXhGvsBcN2%2BGDkjo4SXuds85Np9xo'
                    'GdT%2Bdk8nEKR2OZPVfBZAwV8I3THo6JtpvwDkFyfbp4oG4k%2Bmc5G'
                    'DBlBDnbxozI231xpc6K6ehY%2FK6WO0qftaxdXNYUdrljRAzdvsIjU%2F'
                    'irauEV1eAi6cBVce3VqqhgtCVbVh4vby9j7Bq%2BY2hjzWEigOYhh1S8'
                    'ivCMLPX78KnoX0Fx9717BbJPdpiku%2FqSY1JbcjFnUzeCCWjTk%2BV'
                    'qSO6e8YQ0eE4JaHKciHvEUt6t%2FJ%2B3KwZQ2skBOefvHGLJA%3D%3D%27')
