import logging 
from typing import Union
from components import PAIGetRequests, PAIPostRequests, MetricsResponse, TextResponse, PAIURIs, ProcessTextRequest

logger = logging.getLogger(__name__)




class PAIClient:
    """
    Client used to connect to private-ai's deidentication service   
    """
    def __init__(self, pai_uri, api_key=None):
        # Add source url
        self.uris = PAIURIs(pai_uri)
        self.get = PAIGetRequests(self.uris)
        self.post = PAIPostRequests(api_key, self.uris)
        self.last_response = None
        self._text_response = TextResponse()
        self._metric_response = MetricsResponse()
        # Hit the health endpoint to verify the connection
        self.ping()

    @property
    def response(self):
        return self.last_response

    def _set_response(self, response_class, response):
        response_class.response = response
        self.last_response = response_class


    def ping(self):
        """
        Makes a call to the Private-AI service's health endpoint. 
        Can be used as a validator to ensure the service is running.
        """
        response = self.get.health()
        if response.status_code != 200:
            logger.warning(f"The Private AI server cannot be reached")
            return False
        logger.info(f"Connected to {self.uris.pai_uri}")
        return True

    def get_metrics(self):
        """
        Returns information about the Private-AI's server
        """
        self._set_response(self._metric_response, self.get.metrics())
        return self.last_response
    
    def process_text_request(self, request_object: Union[dict, ProcessTextRequest]):
        """
        Used to deidentify text 
        """
        print(type(request_object))
        if type(request_object) is ProcessTextRequest:
            self._set_response(self._text_response, self.post.process_text(request_object.to_dict()))
        elif type(request_object) == dict:
            self._set_response(self._text_response, self.post.process_text(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a ProcessTextRequest class")
        return self.last_response

    

    








