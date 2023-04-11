import logging 
from typing import Union
from components import PAIGetRequests, PAIPostRequests, MetricsResponse, TextResponse, VersionResponse, PAIURIs, ProcessTextRequest, ProcessFilesUriRequest

logger = logging.getLogger(__name__)




class PAIClient:
    """
    Client used to connect to private-ai's deidentication service   
    """
    def __init__(self, schema:str = "http", pai_uri: str ="localhost", port:str = "8080"):
        # Add source url
        self.uris = PAIURIs(schema, pai_uri, port)
        self.get = PAIGetRequests(self.uris)
        self.post = PAIPostRequests(self.uris) 
        # Hit the health endpoint to verify the connection
        self.ping()

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

    def get_metrics_request(self):
        """
        Returns information about the Private-AI's server
        """
        return MetricsResponse(self.get.metrics(), json_response=False)
    
    def get_version_request(self):
        """
        Returns the version of the container application code
        """
        return VersionResponse(self.get.version)
    
    def process_text_request(self, request_object: Union[dict, ProcessTextRequest]):
        """
        Used to deidentify text 
        """
        if type(request_object) is ProcessTextRequest:
            response = TextResponse(self.post.process_text(request_object.to_dict()))
        elif type(request_object) is dict:
            response = TextResponse(self.post.process_text(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a ProcessTextRequest class")
        return response
    
    def process_files_uri_request(self, request_object: Union[dict, ProcessFilesUriRequest])

    

    








