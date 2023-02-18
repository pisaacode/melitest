import logging
import json
from src.exceptions import MalformedRequest, ErrorBuildingResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Utils:

    @staticmethod
    def clean_request(event):
        """
        The clean_request function takes in the event dictionary and returns a new dictionary with
        the following keys: method, path, headers, body.

        :param event: Get the data from the request
        :return: A dictionary containing the http method, path, headers and body of the request
        """
        # Get data original request
        try:
            method = event['httpMethod']
            path = event['path']

            event['headers'].pop('Host')
            headers = event['headers']
            body = event.get('body', None)

            data = {'method': method,
                    'path': path,
                    'headers': headers,
                    'body': body}
        except Exception as e:
            logger.error(f"Error getting request, Error: {e}")
            raise MalformedRequest("Error getting request")

        return data

    @staticmethod
    def build_response(resp):
        """
        The build_response function takes a requests.Response object and returns a dictionary containing the response
        status code, headers, and body.

        :param resp: Store the response from the api gateway
        :return: A dictionary:
        """
        try:
            headers = dict(resp.headers)
            body = resp.content
            response = {
                'statusCode': resp.status_code,
                'headers': headers,
                'body':  body
            }
        except Exception as e:
            logger.error(f"Error building response, Error: {e}")
            raise ErrorBuildingResponse("Error building response")

        return response

    @staticmethod
    def error_response(status_code, message, causes):
        response = {
            'statusCode': status_code,
            'body': json.dumps({
                "message": message,
                "causes": str(causes)
            })
        }
        return response
