import logging
from typing import Union

from requests import HTTPError

from .components import *
from .__about__ import __version__


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
        self._uris = PAIURIs(url, scheme, host, port)
        self.get = PAIGetRequests(self._uris)
        self.post = PAIPostRequests(self._uris)
        if "api_key" in kwargs.keys():
            self.add_api_key(kwargs["api_key"])
        elif "bearer_token" in kwargs.keys():
            self.add_bearer_token(kwargs["bearer_token"])
        self._container_version = None

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

    def _version_warning(self) -> None:

        # only compare major and minor version numbers
        parsed_container_version = self._container_version.split('.')[:2]
        parsed_client_version = __version__.split('.')[:2]

        if parsed_container_version != parsed_client_version:
            logging.warning(f"Version mismatch: privateai_client {__version__} may be incompatible with PAI container "
                            f"{self._container_version}. Please install the appropriate client version!")

    def check_version_compatibility(self) -> None:

        if self._container_version is None:
            self.get_version()
        else:
            self._version_warning()

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
        self.check_version_compatibility()
        return MetricsResponse(self.get.metrics())

    def get_version(self):
        """
        Returns the version of the container application code
        """
        ret = VersionResponse(self.get.version())
        self._container_version = ret.app_version
        self._version_warning()
        return ret

    def get_diagnostics(self):
        """
        Returns diagnostic information about the Private-AI container host
        """
        self.check_version_compatibility()
        return DiagnosticResponse(self.get.diagnostics())

    def process_text(self, request_object: Union[dict, ProcessTextRequest]):
        """
        Used to deidentify text
        """
        if type(request_object) is ProcessTextRequest:
            self.check_version_compatibility()
            response = TextResponse(self.post.process_text(request_object.to_dict()))
        elif type(request_object) is dict:
            self.check_version_compatibility()
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
            self.check_version_compatibility()
            response = ReidentifyTextResponse(
                self.post.reidentify_text(request_object.to_dict())
            )
        elif type(request_object) is dict:
            self.check_version_compatibility()
            response = ReidentifyTextResponse(self.post.reidentify_text(request_object))
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
            self.check_version_compatibility()
            response = FilesUriResponse(
                self.post.process_files_uri(request_object.to_dict())
            )
        elif type(request_object) is dict:
            self.check_version_compatibility()
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
            self.check_version_compatibility()
            response = FilesBase64Response(
                self.post.process_files_base64(request_object.to_dict())
            )
        elif type(request_object) is dict:
            self.check_version_compatibility()
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
            self.check_version_compatibility()
            response = BleepResponse(self.post.bleep(request_object.to_dict()))
        elif type(request_object) is dict:
            self.check_version_compatibility()
            response = BleepResponse(self.post.bleep(request_object))
        else:
            raise ValueError(
                "request_object can only be a dictionary or a BleepRequest object"
            )
        return response
