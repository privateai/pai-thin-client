from collections import defaultdict


class MaskEntityProcessor:
    def __init__(self, masking_character: str = "#"):
        self.masking_character = masking_character

    def __call__(self, entity: dict) -> str:
        return self.masking_character * len(entity["text"])


class MarkerEntityProcessor:
    def __init__(self):
        self.counts: defaultdict[str, int] = defaultdict(int)

    def __call__(self, entity: dict) -> str:
        key = entity["best_label"]
        self.counts[key] += 1
        return f"[{key}_{self.counts[key]}]"
