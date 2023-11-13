import logging


class PAIURIs:
    def __init__(self, url=None, scheme=None, host=None, port=None, **kwargs):
        if url:
            self._pai_uri = url
        elif scheme and host:
            self.valid_schemes = ["http", "https"]
            scheme = scheme.split("://")[0]
            if scheme not in self.valid_schemes:
                raise ValueError(
                    f"Scheme must be one of the following: {', '.join(self.valid_schemes)}"
                )
            port = f":{port}" if port else ""
            self._pai_uri = f"{scheme}://{host}{port}"
        else:
            raise ValueError(
                "PAIClient needs either a url, or a scheme and host to initialize. You can find more information on which url to use here: https://docs.private-ai.com/thin-client/"
            )

    @property
    def pai_uri(self):
        return self._pai_uri

    @property
    def api_version(self):
        return "v3"

    @property
    def bleep(self):
        return self._create_uri(self.pai_uri, self.api_version, "bleep")

    @property
    def health(self):
        return self._create_uri(self.pai_uri, "healthz")

    @property
    def metrics(self):
        return self._create_uri(self.pai_uri, "metrics")

    @property
    def diagnostics(self):
        return self._create_uri(self.pai_uri, "diagnostics")

    @property
    def process_text(self):
        return self._create_uri(self.pai_uri, self.api_version, "process", "text")

    @property
    def process_files_uri(self):
        return self._create_uri(
            self.pai_uri, self.api_version, "process", "files", "uri"
        )

    @property
    def reidentify_text(self):
        return self._create_uri(
            self.pai_uri, self.api_version, "process", "text", "reidentify"
        )

    @property
    def process_files_base64(self):
        return self._create_uri(
            self.pai_uri, self.api_version, "process", "files", "base64"
        )

    @property
    def version(self):
        return self._create_uri(self.pai_uri, "")

    def _create_uri(self, *args):
        return "/".join([x.strip("/") for x in args])
