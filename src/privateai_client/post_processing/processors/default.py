from collections import defaultdict

from .base_processor import BaseProcessor


class MaskEntityProcessor(BaseProcessor):
    def __init__(self, masking_character: str = "#"):
        super().__init__()
        self._can_process_textresp = True
        self.masking_character = masking_character

    def __call__(self, entity: dict) -> str:
        return self.masking_character * len(entity["text"])


class MarkerEntityProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self._can_process_textresp = True
        self.counts: defaultdict[str, int] = defaultdict(int)

    def __call__(self, entity: dict) -> str:
        key = entity["best_label"]
        self.counts[key] += 1
        return f"[{key}_{self.counts[key]}]"
