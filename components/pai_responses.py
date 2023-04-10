from requests import Response



class BaseResponse:

    def __init__(self, response_object: Response, json_response:bool =True):
        self._response = response_object
        # Should be json or text
        self._json_response = json_response

    def __call__(self):
        return self.response

    @property
    def response(self):
        return self._response

    @property
    def ok(self):
        return self().ok

    @property
    def status_code(self):
        return self().status_code
    
    @property
    def body(self):
        if self._json_response == "json":
            return self().json() 
        else:
            return self().text

    @response.setter
    def response(self, new_response):
        if type(new_response) is not Response:
            raise ValueError("response must be a Response object")
        self._response = new_response

    def get_attribute_entries(self, name):
        # Used for any nested data in the response body
        if not self.json_response: 
            raise ValueError("get_attribute_entries needs a response of type 'json'")
        return [row.get(name) for row in self().json()]

class MetricsResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(MetricsResponse, self).__init__(response_object, 'text')

class VersionResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(VersionResponse, self).__init__(response_object, 'text')

    @property
    def app_version(self):
        return self.body.get('app_version')

class TextResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(TextResponse, self).__init__(response_object, 'json')

    @property
    def processed_text(self):
        return self.get_attribute_entries("processed_text")
    
    @property
    def entities(self):
        return self.get_attribute_entries("entities")
    
    @property
    def entities_present(self):
        return self.get_attribute_entries("entities_present")
    
    @property
    def characters_processed(self):
        return self.get_attribute_entries("characters_processed")
    
    @property
    def languages_detected(self):
        return self.get_attribute_entries("languages_detected")
    
