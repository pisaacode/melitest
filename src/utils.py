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
            request = event['requestContext']['http']
            method = request['method']
            path = request['path']

            event['headers'].pop('host')
            headers = event['headers']
            body = request.get('body', None)

            data = {'method': method,
                    'path': path,
                    'headers': headers,
                    'body': body}
        except Exception as e:
            logger.error(f"Error getting request, Error: {e}")
            raise MalformedRequest("Client id was not found")

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
            raise ErrorBuildingResponse("Client id was not found")

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
