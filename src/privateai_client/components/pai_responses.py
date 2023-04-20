from requests import Response



class BaseResponse:

    def __init__(self, response_object: Response, json_response:bool =True):
        self._response = response_object
        # Should be json or text
        self._json_response = json_response

    def __call__(self):
        return self.response

    @property
    def json_response(self):
        return self._json_response

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
        if self._json_response:
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
        if not self._json_response: 
            raise ValueError("get_attribute_entries needs a response of type json")
        body = self.body
        if type(body) is list:
            return [row.get(name) for row in self().json()]
        elif type(body) is dict:
            return body.get(name)


class MetricsResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(MetricsResponse, self).__init__(response_object, False)

class VersionResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(VersionResponse, self).__init__(response_object, True)

    @property
    def app_version(self):
        return self.get_attribute_entries('app_version')

class DemiTextResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(DemiTextResponse, self).__init__(response_object, True)

    @property
    def processed_text(self):
        return self.get_attribute_entries("processed_text")
    
    @property
    def entities(self):
        return self.get_attribute_entries("entities")
    
    @property
    def entities_present(self):
        return self.get_attribute_entries("entities_present")

class TextResponse(DemiTextResponse):

    def __init__(self, response_object: Response=None):
        super(TextResponse, self).__init__(response_object)
    
    @property
    def characters_processed(self):
        return self.get_attribute_entries("characters_processed")
    
    @property
    def languages_detected(self):
        return self.get_attribute_entries("languages_detected")
    
class FilesUriResponse(DemiTextResponse):

    def __init__(self, response_object: Response = None):
        super(FilesUriResponse, self).__init__(response_object)

    @property
    def result_uri(self):
        return self.get_attribute_entries("result_uri")
    
class FilesBase64Response(DemiTextResponse):

    def __init__(self, response_object: Response = None):
        super(FilesBase64Response, self).__init__(response_object)

    @property
    def processed_file(self):
        return self.get_attribute_entries("processed_file")
    
class BleepResponse(BaseResponse):

    def __init__(self, response_object: Response = None):
        super(BleepResponse, self).__init__(response_object, True)
    
    @property
    def bleeped_file(self):
        return self.get_attribute_entries("bleeped_file")
        
