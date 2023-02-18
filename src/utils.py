import logging
import json
from src.exceptions import MalformedRequest, ErrorBuildingResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Utils:

    @staticmethod
    def clean_request(event):
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
