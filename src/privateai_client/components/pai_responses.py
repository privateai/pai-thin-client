from requests import HTTPError, Response

from .request_objects import Entity, ReidentifyTextRequest


class BaseResponse:
    def __init__(self, response_object: Response, json_response: bool = True):
        self._response = response_object
        # Should be json or text
        self._json_response = json_response
        if not self.response.ok:
            message = (
                f"The request returned with a {self.response.status_code} {self.reason}"
            )
            if self.response.status_code == 400:
                message += f" -- {self.body}"
            raise HTTPError(message)

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
    def reason(self):
        return self().reason

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
    def __init__(self, response_object: Response = None):
        super(MetricsResponse, self).__init__(response_object, False)


class VersionResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(VersionResponse, self).__init__(response_object, True)

    @property
    def app_version(self):
        return self.get_attribute_entries("app_version")


class DiagnosticResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(DiagnosticResponse, self).__init__(response_object, True)

    @property
    def get_platform(self):
        return self.get_attribute_entries("platform")

    @property
    def get_cpu_count(self):
        return self.get_attribute_entries("cpu_count")

    @property
    def get_container_version(self):
        return self.get_attribute_entries("container_version")

    @property
    def get_cpu_name(self):
        return self.get_attribute_entries("cpu_name")

    @property
    def get_gpu_info(self):
        return self.get_attribute_entries("gpu_info")


class DemiTextResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
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

    @property
    def best_labels(self):
        if type(self.body) == dict:
            best_labels = [entity["best_label"] for entity in self.entities]
        else:
            best_labels = [
                attr["best_label"] for entity in self.entities for attr in entity
            ]
        return best_labels

    def get_reidentify_entities(self):
        if type(self.body) == dict:
            entities = [
                Entity(entity["processed_text"], entity["text"])
                for entity in self.entities
            ]
        else:
            entities = [
                Entity(attr["processed_text"], attr["text"])
                for entity in self.entities
                for attr in entity
            ]
        return entities

    def get_reidentify_request(self):
        entities = self.get_reidentify_entities()
        return ReidentifyTextRequest(self.processed_text, entities)


class TextResponse(DemiTextResponse):
    def __init__(self, response_object: Response = None):
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


class ReidentifyTextResponse(BaseResponse):
    def __init__(self, response_object: Response = None):
        super(ReidentifyTextResponse, self).__init__(response_object, True)
