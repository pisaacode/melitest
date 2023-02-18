import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MalformedRequest(Exception):
    def __init__(self, causes):
        Exception.__init__(self, causes)


class ErrorBuildingResponse(Exception):
    def __init__(self, causes):
        Exception.__init__(self, causes)
