import requests

def lambda_handler(event, context):

    # Get data original request
    request = event['requestContext']['http']
    method = request['method']
    path = request['path']

    event['headers'].pop('host')
    headers = event['headers']
    body = request.get('body', None)

    # Build url
    url = 'https://api.mercadolibre.com' + path
    print(url)

    # Send data to target server
    resp = requests.request(
        method=method,
        url=url,
        headers=headers)

    # return request to client
    headers = dict(resp.headers)
    body = resp.content

    print(resp)
    response = {
        'statusCode': resp.status_code,
        'headers': headers,
        'body': body
    }
    return response

