from .base_processor import BaseProcessor


class RehydratePIIProcessor(BaseProcessor):
    def __init__(self):
        """
        Initialize the RehydratePIIProcessor.
        """
        super().__init__()
        self._can_process_textresp = True

    def __call__(self, entity: dict) -> str:
        """
        Process PII back into the redacted text.

        Args:
            entity: an individual entity returned by the DEID container.

        """
        value = entity.get("text", {})
        return value
