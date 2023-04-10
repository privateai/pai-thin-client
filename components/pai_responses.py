from requests import Response



class BaseResponse:

    def __init__(self, response_object, body_type):
        self._response = response_object
        # Should be json or text
        self.body_type = body_type

    def __call__(self):
        return self.response

    @property
    def response(self):
        return self._response

    @property
    def status_code(self):
        return self.response.status_code
    
    @property
    def body(self):
        if self.body_type == "json":
            return self.response.json() 
        elif self.body_type == "text":
            return self.response.text
        else:
            return None
        
    
    @response.setter
    def response(self, new_response):
        if type(new_response) is not Response:
            raise ValueError("response must be a Response object")
        self._response = new_response

    def get_attribute_entries(self, name):
        # Used for any nested data in the response body
        if self.body_type != "json": 
            raise ValueError("get_attribute_entries needs a response of type 'json'")
        attributes = [row.get(name) for row in self.response.json()]
        # Might be more intuitive to just handle receiving a list only 
        return attributes[0] if len(attributes) == 1 else attributes


class MetricsResponse(BaseResponse):

    def __init__(self, response_object: Response=None):
        super(MetricsResponse, self).__init__(response_object, 'text')


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
    
    