from collections import defaultdict
from typing import Literal

from pyxdameraulevenshtein import damerau_levenshtein_distance


class FuzzyMatchEntityProcessor:
    def __init__(
        self,
        known_words_list: list[str] | tuple[str] | set[str],
        threshold: int,
        strategy: Literal["BLOCK", "ALLOW"] = "BLOCK",
        process_type: Literal["MARKER", "MASK"] = "MARKER",
        masking_character: str = "#",
        ignore_casing: bool = True,
    ):
        self.known_words_list = known_words_list
        self.threshold = threshold
        self.process_type = process_type
        self.strategy = strategy
        self.ignore_casing = ignore_casing
        self.masking_character = masking_character
        self.counts: defaultdict[str, int] = defaultdict(int)
        self._validate_attributes()

    def __call__(self, entity: dict) -> str:
        if self.ignore_casing:
            lower_text = entity["text"].lower()
            min_dist = min(damerau_levenshtein_distance(lower_text, word.lower()) for word in self.known_words_list)
        else:
            min_dist = min(damerau_levenshtein_distance(entity["text"], word) for word in self.known_words_list)
        should_allow = self.strategy == "ALLOW"
        is_similar = min_dist <= self.threshold

        if is_similar == should_allow:
            return entity["text"]
        else:
            if self.process_type == "MASK":
                return self.masking_character * len(entity["text"])
            key = entity["best_label"]
            self.counts[key] += 1
            return f"{key}_{self.counts[key]}"

    def _validate_attributes(self):
        if self.strategy not in ["BLOCK", "ALLOW"]:
            raise ValueError(f"Invalid value for strategy. Accepted values: 'BLOCK' and 'ALLOW'")
        if self.process_type not in ["MARKER", "MASK"]:
            raise ValueError(f"Invalid value for process_type. Accepted values: 'MARKER' and 'MASK'")
        if not (
            isinstance(self.known_words_list, list) or isinstance(self.known_words_list, tuple),
            isinstance(self.known_words_list, set),
        ):
            raise ValueError(f"Invalid value for known_words_list. Accepted are list, tuple or set of strings.")
        if not isinstance(self.masking_character, str):
            raise ValueError(f"Invalid value for masking_character. Accepted value is a valid string")
        if not isinstance(self.ignore_casing, bool):
            raise ValueError(f"Invalid value for ignore_casing. Accepted values: True and False")
