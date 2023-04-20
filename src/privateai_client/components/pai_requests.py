import requests
from typing import Union
from .pai_uris import PAIURIs



class PAIRequests:
    
    def __init__(self, uris:PAIURIs):

        self._uris = uris

    @property
    def uris(self):
        return self._uris
    
    def make_request(self, request_type: Union[requests.get, requests.post], uri:str, payload: dict=None):
        return request_type(uri, json=payload)



class PAIGetRequests(PAIRequests):

    def __init__(self, uris:PAIURIs):
        """
        A class of get requests used by the client
        """
        self.request_type = requests.get
        super(PAIGetRequests, self).__init__(uris)
    

    def health(self):
        return self.make_request(self.request_type, self.uris.health)

    def metrics(self):
        return  self.make_request(self.request_type, self.uris.metrics)
    
    def version(self):
        return  self.make_request(self.request_type, self.uris.version)
    


class PAIPostRequests(PAIRequests):

    def __init__(self, uris:PAIURIs):
        self.request_type = requests.post
        super(PAIPostRequests, self).__init__(uris)

    def process_text(self, request_object):
        return self.make_request(self.request_type, self.uris.process_text, request_object)

    def process_files_uri(self, request_object):
        return self.make_request(self.request_type, self.uris.process_files_uri, request_object)
    
    def process_files_base64(self, request_object):
        return self.make_request(self.request_type, self.uris.process_files_base64, request_object)
    
    def bleep(self, request_object):
        return self.make_request(self.request_type, self.uris.bleep, request_object)
        
