import json

import pytest
import requests

from ..components.pai_responses import AnalyzeTextResponse
from ..post_processing import (
    FuzzyMatchEntityProcessor,
    MarkerEntityProcessor,
    MaskEntityProcessor,
    deidentify_text,
)


# Deidentify text
def test_deidentify_text__no_entities():
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(
        [
            {
                "entities": [],
                "entities_present": False,
                "characters_processed": 11,
            }
        ]
    ).encode("utf-8")

    text_out = deidentify_text(
        input_texts=["My name is."],
        response=AnalyzeTextResponse(response),
        entity_processors={},
        default_processor=MarkerEntityProcessor(),
    )
    assert text_out == ["My name is."]


def test_deidentify_text__with_default_entities():
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(
        [
            {
                "entities": [
                    {
                        "text": "John",
                        "location": {"stt_idx": 11, "end_idx": 15},
                        "best_label": "NAME_GIVEN",
                        "labels": {
                            "NAME": 0.9030465483665466,
                            "NAME_GIVEN": 0.8891170620918274,
                        },
                    }
                ],
                "entities_present": True,
                "characters_processed": 16,
            }
        ]
    ).encode("utf-8")

    text_out = deidentify_text(
        input_texts=["My name is John."],
        response=AnalyzeTextResponse(response),
        entity_processors={},
        default_processor=MarkerEntityProcessor(),
    )
    assert text_out == ["My name is NAME_GIVEN_1."]


def test_deidentify_text__with_fuzzy_matching():
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(
        [
            {
                "entities": [
                    {
                        "text": "John",
                        "location": {"stt_idx": 11, "end_idx": 15},
                        "best_label": "NAME_GIVEN",
                        "labels": {
                            "NAME": 0.9030465483665466,
                            "NAME_GIVEN": 0.8891170620918274,
                        },
                    }
                ],
                "entities_present": True,
                "characters_processed": 16,
            }
        ]
    ).encode("utf-8")

    text_out = deidentify_text(
        input_texts=["My name is John."],
        response=AnalyzeTextResponse(response),
        entity_processors={
            "NAME_GIVEN": FuzzyMatchEntityProcessor(
                known_words_list=("Josh",),
                threshold=2,
                strategy="BLOCK",
                process_type="MASK",
            )
        },
        default_processor=MarkerEntityProcessor(),
    )
    assert text_out == ["My name is ####."]


# Mask processors
def test_mask_processor():
    entity_text = "John"
    entity = {
        "text": entity_text,
        "location": {"stt_idx": 11, "end_idx": 15},
        "best_label": "NAME_GIVEN",
    }
    processor = MaskEntityProcessor(masking_character="^")
    masked_entity = processor(entity)
    assert masked_entity == "^" * len(entity_text)


# Marker processor
def test_marker_processor():
    entity_1 = {
        "text": "John",
        "best_label": "NAME_GIVEN",
    }

    entity_2 = {
        "text": "France",
        "best_label": "LOCATION_COUNTRY",
    }

    entity_3 = {
        "text": "Josh",
        "best_label": "NAME_GIVEN",
    }
    processor = MarkerEntityProcessor()
    markers = [processor(e) for e in [entity_1, entity_2, entity_3]]
    assert markers == ["NAME_GIVEN_1", "LOCATION_COUNTRY_1", "NAME_GIVEN_2"]


# Fuzzy match processor
@pytest.mark.parametrize(
    argnames=[
        "entity_text",
        "known_words_list",
        "threshold",
        "strategy",
        "process_type",
        "masking_character",
        "ignore_casing",
        "processed_text",
    ],
    argvalues=[
        ("Josh", ["John", "Peter"], 2, "BLOCK", "MASK", "#", True, "####"),
        ("Ian", ["John", "Peter"], 2, "BLOCK", "MASK", "#", True, "Ian"),
        ("Josh", ["John", "Peter"], 2, "ALLOW", "MASK", "#", True, "Josh"),
        ("Ian", ["John", "Peter"], 2, "ALLOW", "MASK", "#", True, "###"),
        ("Josh", ["John", "Peter"], 2, "BLOCK", "MARKER", "#", True, "NAME_GIVEN_1"),
        ("Josh", ["JOSH", "Peter"], 2, "BLOCK", "MARKER", "#", False, "Josh"),
    ],
)
def test_fuzzy_match_entity_processor(
    entity_text,
    known_words_list,
    threshold,
    strategy,
    process_type,
    masking_character,
    ignore_casing,
    processed_text,
):
    processor = FuzzyMatchEntityProcessor(
        known_words_list=known_words_list,
        threshold=threshold,
        strategy=strategy,
        process_type=process_type,
        masking_character=masking_character,
        ignore_casing=ignore_casing,
    )
    entity = {"text": entity_text, "best_label": "NAME_GIVEN"}
    assert processor(entity) == processed_text


@pytest.mark.parametrize(
    argnames=[
        "known_words_list",
        "threshold",
        "strategy",
        "process_type",
        "masking_character",
        "ignore_casing",
        "error",
    ],
    argvalues=[
        (
            {"NAME": ["JOHN"]},
            2,
            "BLOCK",
            "MASK",
            "#",
            True,
            "Invalid value for known_words_list. Accepted are list, tuple or set of strings.",
        ),
        (
            ["John", 25],
            2,
            "BLOCK",
            "MASK",
            "#",
            True,
            "Invalid value for known_words_list. Accepted are list, tuple or set of strings.",
        ),
        (
            ["John", "Peter"],
            "two",
            "BLOCK",
            "MASK",
            "#",
            True,
            "Invalid value for threshold. Accepted value is a valid integer.",
        ),
        (
            ["John", "Peter"],
            2,
            "ENABLE",
            "MASK",
            "#",
            True,
            "Invalid value for strategy. Accepted values: 'BLOCK' and 'ALLOW'",
        ),
        (
            ["John", "Peter"],
            2,
            "ALLOW",
            "HIDE",
            "#",
            True,
            "Invalid value for process_type. Accepted values: 'MARKER' and 'MASK'",
        ),
        (
            ["John", "Peter"],
            2,
            "BLOCK",
            "MARKER",
            [],
            True,
            "Invalid value for masking_character. Accepted value is a valid string",
        ),
        (
            ["JOSH", "Peter"],
            2,
            "BLOCK",
            "MARKER",
            "#",
            "ignore",
            "Invalid value for ignore_casing. Accepted values: True and False",
        ),
    ],
)
def test_fuzzy_match_processor_invalid_attrs(
    known_words_list,
    threshold,
    strategy,
    process_type,
    masking_character,
    ignore_casing,
    error,
):
    with pytest.raises(ValueError, match=error):
        FuzzyMatchEntityProcessor(
            known_words_list=known_words_list,
            threshold=threshold,
            strategy=strategy,
            process_type=process_type,
            masking_character=masking_character,
            ignore_casing=ignore_casing,
        )
