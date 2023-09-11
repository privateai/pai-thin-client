import logging
from typing import Union
from requests import HTTPError

from .components import *
from .components.llm_connector import LLMConnector


class PAIClient:
    """
    Client used to connect to private-ai's deidentication service
    """
    def __init__(
        self,
        scheme: str = None,
        host: str = None,
        port: str = None,
        url: str = None,
        **kwargs,
    ):
        # Add source url
        self.uris = PAIURIs(url, scheme, host, port)
        self.get = PAIGetRequests(self.uris)
        self.post = PAIPostRequests(self.uris)
        if "api_key" in kwargs.keys():
            self.add_api_key(kwargs["api_key"])
        elif "bearer_token" in kwargs.keys():
            self.add_bearer_token(kwargs["bearer_token"])

        self.llm_connector = LLMConnector()

    def _add_auth(self, auth_type, auth_val):
        auth_header = {}
        if auth_type == "api_key":
            auth_header = {"x-api-key": auth_val}
        elif auth_type == "bearer_token":
            auth_header = {"Authorization": f"Bearer {auth_val}"}
        else:
            raise ValueError(
                f"{auth_type} is not currently a supported method of authorization"
            )
        for subclass in [self.get, self.post]:
            subclass.headers = {**auth_header, **subclass.base_header}

    def add_api_key(self, api_key: str):
        self._add_auth("api_key", api_key)

    def add_bearer_token(self, token: str):
        self._add_auth("bearer_token", token)

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
        return MetricsResponse(self.get.metrics())

    def get_version(self):
        """
        Returns the version of the container application code
        """
        return VersionResponse(self.get.version())

    def get_diagnostics(self):
        """
        Returns diagnostic information about the Private-AI container host
        """
        return DiagnosticResponse(self.get.diagnostics())

    def process_text(self, request_object: Union[dict, ProcessTextRequest]):
        """
        Used to deidentify text
        """
        if type(request_object) is ProcessTextRequest:
            response = TextResponse(self.post.process_text(request_object.to_dict()))
        elif type(request_object) is dict:
            response = TextResponse(self.post.process_text(request_object))
        else:
            raise ValueError(
                "request_object can only be a dictionary or a ProcessTextRequest object"
            )
        return response

    def reidentify_text(self, request_object: Union[dict, ReidentifyTextRequest]):
        """
        Used to reidentify text
        """
        if type(request_object) is ReidentifyTextRequest:
            response = ReidentifyTextResponse(
                self.post.reidentify_text(request_object.to_dict())
            )
        elif type(request_object) is dict:
            response = ReidentifyTextRequest(self.post.process_text(request_object))
        else:
            raise ValueError(
                "request_object can only be a dictionary or a ReidentifyTextRequest object"
            )
        return response

    def process_files_uri(self, request_object: Union[dict, ProcessFileUriRequest]):
        """
        Used to deidentify files by uri
        """
        if type(request_object) is ProcessFileUriRequest:
            response = FilesUriResponse(
                self.post.process_files_uri(request_object.to_dict())
            )
        elif type(request_object) is dict:
            response = FilesUriResponse(self.post.process_files_uri(request_object))
        else:
            raise ValueError(
                "request_object can only be a dictionary or a ProcessFileUriRequest object"
            )
        return response

    def process_files_base64(
        self, request_object: Union[dict, ProcessFileBase64Request]
    ):
        """
        Used to deidentify base64 files
        """
        if type(request_object) is ProcessFileBase64Request:
            response = FilesBase64Response(
                self.post.process_files_base64(request_object.to_dict())
            )
        elif type(request_object) is dict:
            response = FilesBase64Response(
                self.post.process_files_base64(request_object)
            )
        else:
            raise ValueError(
                "request_object can only be a dictionary or a ProcessFileBase64Request object"
            )
        return response

    def bleep(self, request_object: Union[dict, BleepRequest]):
        """
        Used to deidentify audio files by uri
        """
        if type(request_object) is BleepRequest:
            response = BleepResponse(self.post.bleep(request_object.to_dict()))
        elif type(request_object) is dict:
            response = BleepResponse(self.post.bleep(request_object))
        else:
            raise ValueError(
                "request_object can only be a dictionary or a BleepRequest object"
            )
        return response
    
    def send_redacted_prompt(self, prompt: str, llm_model: str, **kwargs):
       """
       Used to send redacted prompts to LLMs
       """

       deidentify_request = ProcessTextRequest(text=[prompt])
       deidentified_response = self.process_text(deidentify_request)

       #Send prompt to LLM
       redacted_responses = self.llm_connector.send_redacted_prompt(prompt=deidentified_response.processed_text[0], llm_model=llm_model, **kwargs)

       #Create entities used for reidentification
       reid_entities = []
       if len(deidentified_response.entities) > 0:
            for entity in deidentified_response.entities[0]:
               reid_entities.append(Entity(entity["processed_text"], entity["text"]))

            #Reidentify request
            reidentified_responses = self.reidentify_text(request_object=ReidentifyTextRequest(redacted_responses, entities=reid_entities)).body

       return reidentified_responses
