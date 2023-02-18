import requests
from src.utils import Utils
from src.constants import SERVERS
from src.exceptions import MalformedRequest, ErrorBuildingResponse


def lambda_handler(event, context):

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
                                        message="Error internal.",
                                        causes=exception)

    except ErrorBuildingResponse as exception:
        response = Utils.error_response(status_code=501,
                                        message="Error internal.",
                                        causes=exception)
    except Exception as exception:
        response = Utils.error_response(status_code=501,
                                        message="Internal Error.",
                                        causes=exception)

    # return request to client
    return response
