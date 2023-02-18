import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import requests_mock
from tests.samples_json import CORRECT_REQUEST, CORRUPT_REQUEST
from src.lambdas.proxy import lambda_handler


def test_corrupt_request():
    """
    The test_corrupt_request function tests the Lambda function's ability to handle a corrupt request.
    It does this by passing in a request that is not valid JSON, which should cause the Lambda function
    to return an HTTP status code of 501 (not implemented). The test then checks that this is indeed what happens.

    :return: A status code of 501
    """
    resp = lambda_handler(CORRUPT_REQUEST, {})
    assert resp.get('statusCode') == 501


def test_ok_request():
    """
    The test_ok_request function tests the lambda_handler function by mocking a ReST call to the
    API Gateway. The test passes if it returns a 200 status code.

    :return: A 200 status code
    """
    with requests_mock.Mocker() as mock_request:
        mock_request.get(requests_mock.ANY, text="Ok!", status_code=200)
        resp = lambda_handler(CORRECT_REQUEST, {})
        assert resp.get('statusCode') == 200
