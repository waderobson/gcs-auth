import datetime
try:
    from mock import patch

except ImportError:
    from unittest.mock import patch

from middleware_gcs import gcs_query_params_url  # noqa E402


@patch("middleware_gcs.datetime")
def test_gcs_query_params_url(datetime_mock):
    datetime_mock.datetime.now.return_value = datetime.datetime(2019, 11, 1, 18, 20, 48, 963798)
    datetime_mock.timedelta.return_value = datetime.timedelta(0, 900)
    test = gcs_query_params_url('http://test')
    assert test == ('https://storage.googleapis.com?'
                    'GoogleAccessId=readonly@double.iam.gserviceaccount.com'
                    '&Expires=1572658548'
                    '&Signature=b%27CpiEd6cjovh59LfmkJQpWkXPCwlSKKXmFCiyIS'
                    '%2Fvok3lb9DqJsSYkSQAMgy5vcL9W3fussTWjxYHmhYiLtKAOMryRb'
                    'fuKfOIkegup8hqjbF%2BQx3ersJcu0NjE3vq%2B91AuYiDXyUQa1Yo%2Ff94'
                    'YOOmdsd9xDwRqkzYl6jxykC9fr9iKKUqTJjvOk2xoJh'
                    'z7s0MT3aou7WZwqF26Q%2F9YoExIgtWtw9cfKJ'
                    'VapSvYdqBjdtSzKypPh4JYEtpRpW%2BEhfpR74yk3DHYmIG'
                    'rDQjM2StVH%2B3y%2B39qWPR8X5qct75Llj1hGobKK6J4zPWmklt09W'
                    '5uV8DRfQWVdbbFdGsKeN60w%3D%3D%27')
