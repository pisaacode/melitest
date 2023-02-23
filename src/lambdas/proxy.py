import requests
import logging
from src.utils import Utils
from src.constants import SERVERS
from src.exceptions import MalformedRequest, ErrorBuildingResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    The lambda_handler function is the entry point for the AWS Lambda function.
    It receives a ReST request and returns a ReST response.


    :param event: Pass data to the handler
    :param context: Pass information about the invocation,
    :return: A dict with the following keys:
    """

    try:
        data = Utils.clean_request(event)

        # Build url
        url = SERVERS.get('api_mercadolibre') + data.get('path')

        # Send data to target server
        resp = requests.request(
            method=data.get('method'),
            url=url,
            headers=data.get('headers'),
            data=data.get('body')
        )

        # build response to client
        response = Utils.build_response(resp)

    except MalformedRequest as exception:
        response = Utils.error_response(status_code=501,
                                        message="Internal Error.",
                                        causes=exception)

    except ErrorBuildingResponse as exception:
        response = Utils.error_response(status_code=501,
                                        message="Internal Error.",
                                        causes=exception)
    except Exception as exception:
        logger.error(f"Error critical: {exception}")
        response = Utils.error_response(status_code=501,
                                        message="Internal Error.",
                                        causes=exception)

    # return request to client
    return response
