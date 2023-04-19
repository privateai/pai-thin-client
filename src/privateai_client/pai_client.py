import logging 
from typing import Union
from .components import *




class PAIClient:
    """
    Client used to connect to private-ai's deidentication service   
    """
    def __init__(self, scheme:str, host: str, port:str = None):
        # Add source url
        self.uris = PAIURIs(scheme, host, port)
        self.get = PAIGetRequests(self.uris)
        self.post = PAIPostRequests(self.uris) 

    def ping(self):
        """
        Makes a call to the Private-AI service's health endpoint. 
        Can be used as a validator to ensure the service is running.
        """
        response = self.get.health()
        if response.status_code != 200:
            logging.warning(f"The Private AI server cannot be reached")
            return False
        return True

    def get_metrics(self):
        """
        Returns information about the Private-AI's server
        """
        return MetricsResponse(self.get.metrics(), json_response=False)
    
    def get_version(self):
        """
        Returns the version of the container application code
        """
        return VersionResponse(self.get.version)
    
    def process_text(self, request_object: Union[dict, ProcessTextRequest]):
        """
        Used to deidentify text 
        """
        if type(request_object) is ProcessTextRequest:
            response = TextResponse(self.post.process_text(request_object.to_dict()))
        elif type(request_object) is dict:
            response = TextResponse(self.post.process_text(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a ProcessTextRequest object")
        return response
    
    def process_files_uri(self, request_object: Union[dict, ProcessFileUriRequest]):
        """
        Used to deidentify files by uri
        """
        if type(request_object) is ProcessFileUriRequest:
            response = FilesUriResponse(self.post.process_files_uri(request_object.to_dict()))
        elif type(request_object) is dict:
            response = FilesUriResponse(self.post.process_files_uri(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a ProcessFileUriRequest object")
        return response

    def process_files_base64(self, request_object: Union[dict, ProcessFileBase64Request]):
        """
        Used to deidentify base64 files
        """
        if type(request_object) is ProcessFileBase64Request:
            response = FilesBase64Response(self.post.process_files_base64(request_object.to_dict()))
        elif type(request_object) is dict:
            response = FilesBase64Response(self.post.process_files_base64(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a ProcessFileBase64Request object")
        return response
    
    def bleep(self, request_object: Union[dict, BleepRequest]):
        """
        Used to deidentify files by uri
        """
        if type(request_object) is BleepRequest:
            response = BleepResponse(self.post.bleep(request_object.to_dict()))
        elif type(request_object) is dict:
            response = BleepResponse(self.post.bleep(request_object))
        else:
            raise ValueError("request_object can only be a dictionary or a BleepRequest object")
        return response

    

    








