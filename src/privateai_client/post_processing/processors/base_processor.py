from abc import ABC


class BaseProcessor(ABC):
    def __init__(self):
        self._can_process_textresp = False

    def can_process_text_response(self) -> bool:
        """
        Indicates if a processor can be used to post-process a TextResponse
        """
        return self._can_process_textresp
