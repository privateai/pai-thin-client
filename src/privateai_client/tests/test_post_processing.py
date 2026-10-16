import json

import pytest
import requests
from dateutil.relativedelta import relativedelta

from ..components.pai_responses import AnalyzeTextResponse
from ..post_processing import (
    AgeEntityBucketProcessor,
    DateBucketProcessor,
    DateShiftProcessor,
    FuzzyMatchEntityProcessor,
    MarkerEntityProcessor,
    MaskEntityProcessor,
    SyntheticReplacementProcessor,
    deidentify_text,
)


# Deidentify text
def test_deidentify_text_no_entities():
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
        text=["My name is."],
        response=AnalyzeTextResponse(response),
        entity_processors={},
        default_processor=MarkerEntityProcessor(),
    )
    assert text_out == ["My name is."]


def test_deidentify_text_with_default_entities():
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
        text=["My name is John."],
        response=AnalyzeTextResponse(response),
        entity_processors={},
        default_processor=MarkerEntityProcessor(),
    )
    assert text_out == ["My name is [NAME_GIVEN_1]."]


def test_deidentify_text_with_fuzzy_matching():
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
        text=["My name is John."],
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
    assert markers == ["[NAME_GIVEN_1]", "[LOCATION_COUNTRY_1]", "[NAME_GIVEN_2]"]


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
        ("Josh", ["John", "Peter"], 2, "BLOCK", "MARKER", "#", True, "[NAME_GIVEN_1]"),
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
        "error_str",
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
            "Invalid value for threshold. Accepted value is a positive integer.",
        ),
        (
            ["John", "Peter"],
            0,
            "BLOCK",
            "MASK",
            "#",
            True,
            "Invalid value for threshold. Accepted value is a positive integer.",
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
    error_str,
):
    with pytest.raises(ValueError, match=error_str):
        FuzzyMatchEntityProcessor(
            known_words_list=known_words_list,
            threshold=threshold,
            strategy=strategy,
            process_type=process_type,
            masking_character=masking_character,
            ignore_casing=ignore_casing,
        )


# Synthetic replacement processor
def test_synthetic_replacement_processor():
    entity = {
        "text": "John",
        "best_label": "NAME_GIVEN",
        "synthetic_text": "Michael",
    }
    processor = SyntheticReplacementProcessor()
    assert processor(entity) == "Michael"


def test_synthetic_replacement_processor_missing_synthetic_text():
    entity = {
        "text": "John",
        "best_label": "NAME_GIVEN",
    }
    processor = SyntheticReplacementProcessor()
    with pytest.raises(ValueError, match="does not have a `synthetic_text` field"):
        processor(entity)


def test_deidentify_text_with_synthetic_replacements():
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
                            "NAME_GIVEN": 0.9202193021774292,
                            "NAME": 0.9011530876159668,
                        },
                        "coreference_id": "0a82c40c-77cc-42a1-8c3b-5006ddcdc668",
                        "synthetic_text": "Ezekiel",
                    },
                    {
                        "text": "France",
                        "location": {"stt_idx": 27, "end_idx": 33},
                        "best_label": "LOCATION_COUNTRY",
                        "labels": {
                            "LOCATION_COUNTRY": 0.9462521076202393,
                            "LOCATION": 0.9141559600830078,
                        },
                        "coreference_id": "90f6c359-fdbf-4214-a40d-7952a95b7dd5",
                    },
                ],
                "entities_present": True,
                "characters_processed": 34,
                "languages_detected": {"en": 0.9607678651809692},
            }
        ]
    ).encode("utf-8")

    text_out = deidentify_text(
        text=["My name is John. I live in France."],
        response=AnalyzeTextResponse(response),
        entity_processors={"NAME_GIVEN": SyntheticReplacementProcessor()},
        default_processor=MaskEntityProcessor(),
    )
    assert text_out == ["My name is Ezekiel. I live in ######."]


# Age Bucketing
@pytest.mark.parametrize(
    argnames=["entity", "bucket_size", "processed_text"],
    argvalues=[
        (
            {
                "text": "32",
                "best_label": "AGE",
                "location": {"stt_idx": 2, "end_idx": 4},
                "labels": {"AGE": 0.9599081873893738},
                "analysis_result": {
                    "formatted": 32,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            },
            5,
            "[30-34]",
        ),
        (
            {
                "text": "32",
                "best_label": "AGE",
                "location": {"stt_idx": 2, "end_idx": 4},
                "labels": {"AGE": 0.9599081873893738},
                "analysis_result": {
                    "formatted": 32,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            },
            2,
            "[32-33]",
        ),
        (
            {
                "text": "32",
                "best_label": "AGE",
                "location": {"stt_idx": 2, "end_idx": 4},
                "labels": {"AGE": 0.9599081873893738},
                "analysis_result": {
                    "formatted": 32,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            },
            3,
            "[30-32]",
        ),
        (
            {
                "text": "32",
                "best_label": "AGE",
                "location": {"stt_idx": 2, "end_idx": 4},
                "labels": {"AGE": 0.9599081873893738},
            },
            3,
            "[%-%]",
        ),
    ],
)
def test_age_bucket_processor(entity, bucket_size, processed_text):
    processor = AgeEntityBucketProcessor(bin_size=bucket_size)
    assert processor(entity) == processed_text


# Date Shifting
@pytest.mark.parametrize(
    argnames=["entity", "date_offset", "operator", "processed_text"],
    argvalues=[
        (
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            },
            relativedelta(days=1),
            "add",
            "[1990-01-02]",
        ),
        (
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            },
            relativedelta(days=1),
            "subtract",
            "[1989-12-31]",
        ),
    ],
)
def test_date_shifting_processor(entity, date_offset, operator, processed_text):
    processor = DateShiftProcessor(date_offset, operator)
    assert processor(entity) == processed_text


def test_date_shifting_processor_wrong_arg():
    entity = {
        "text": "1990-01-01",
        "location": {"stt_idx": 9, "end_idx": 19},
        "best_label": "DOB",
        "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
        "analysis_result": {
            "formatted": "1990-01-01T00:00:00",
            "subtypes": [
                {"formatted": "1", "label": "DAY"},
                {"formatted": "1", "label": "MONTH"},
                {"formatted": "1990", "label": "YEAR"},
            ],
            "validation_assertions": [],
        },
    }
    offset = relativedelta(months=3)
    # checking error handling
    error_msg = (
        "The operation 'minus' does not exist. Unable to initialize DateShiftProcessor."
    )
    with pytest.raises(ValueError, match=error_msg):
        DateShiftProcessor(offset, "minus")


# Date Bucketing
@pytest.mark.parametrize(
    argnames=["entity", "date_bin", "processed_text"],
    argvalues=[
        (
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            },
            "decade",
            "[1990-01-01 and 1999-12-31]",
        ),
        (
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            },
            "year",
            "[1990-01-01 and 1990-12-31]",
        ),
        (
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            },
            "month",
            "[1990-01-01 and 1990-01-31]",
        ),
    ],
)
def test_date_bucketing_processor(entity, date_bin, text_processed):
    processor = DateBucketProcessor(date_bin)
    assert processor(entity) == text_processed


def test_date_bucketing_processor_wrong_arg():
    # checking error handling
    error_msg = "date_bin value: 'millennia' is not a valid value. Unable to initialize DateBucketProcessor."
    with pytest.raises(ValueError, match=error_msg):
        DateBucketProcessor("millennia")


# Selective Date Component Redaction
def test_date_component_processor():
    pass


[
    {
        "entities": [
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            }
        ],
        "entities_present": true,
        "characters_processed": 20,
        "languages_detected": {"en": 0.7509669661521912},
    }
]
