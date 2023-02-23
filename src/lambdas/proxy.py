import requests
import logging
from src.utils import Utils
from src.constants import SERVERS
from src.exceptions import MalformedRequest, ErrorBuildingResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SERVER_URL = SERVERS.get('api_mercadolibre')


def lambda_handler(event, context):
    """
    The lambda_handler function is the entry point for the AWS Lambda function.
    It receives a ReST request and returns a ReST response.


    :param event: Pass data to the handler
    :param context: Pass information about the invocation,
    :return: A dict with the following keys:
    """

    try:
        request_data = Utils.clean_request(event)

        # Build url
        # Build URL
        url = f"{SERVER_URL}{request_data.get('path')}"

        # Send data to target server
        resp = requests.request(
            method=request_data.get('method'),
            url=url,
            headers=request_data.get('headers'),
            data=request_data.get('body')
        )

        # build response to client
        response_data = Utils.build_response(resp)

        # Return response to client
        return response_data

    except MalformedRequest as exception:
        return Utils.error_response(status_code=400,
                                    message="Internal Error.",
                                    causes=exception)

    except ErrorBuildingResponse as exception:
        return Utils.error_response(status_code=500,
                                    message="Internal Error.",
                                    causes=exception)
    except Exception as exception:
        logger.error(f"Error critical: {exception}")
        return Utils.error_response(status_code=500,
                                    message="Internal Error.",
                                    causes=exception)
