class JuspayException(Exception):

    def __init__(self, http_status=None, message=None,
                 json_body=None, headers=None, request_params= None):
        super(JuspayException, self).__init__(json_body)

        self._message = message
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.request_params = request_params

    def __str__(self):
        if self._message is not None and self.http_status is not None:
            error_response = "ERROR - Request failed with httpResponseCode : {0}.\nerrorMessage : {1}".format(self.http_status, self._message)
        elif self._message is not None:
            error_response =  "ERROR - Request failed. Message : {0}".format(self._message)
        elif self.json_body is not None:
            error_response = "ERROR - Request failed with httpResponseCode : {0}\n{1}".format(self.http_status, self.json_body)
        else:
            error_response = "ERROR - Request failed with unknown reason, please contact support@juspay.in."
        if self.request_params:
            error_response = "\n{0}\nRequest Parameters : {1}".format(error_response, self.request_params)
        return error_response or {}

class InvalidRequestException(JuspayException):
    pass

class AuthenticationException(JuspayException):
    pass

class APIException(JuspayException):
    pass

class APIConnectionException(JuspayException):
    pass

class InvalidArguementException(JuspayException):
    def __init__(self, message=None):
        super(InvalidArguementException, self)\
            .__init__(message=message or "Please pass requiered parameters.")
