import copy
import json
from typing import Callable

import pytest
import requests
from dateutil.relativedelta import relativedelta

from ..components.pai_responses import AnalyzeTextResponse, TextResponse
from ..post_processing import (
    AgeEntityBucketProcessor,
    DateBucketProcessor,
    DateComponentProcessor,
    DateShiftProcessor,
    FuzzyMatchEntityProcessor,
    MarkerEntityProcessor,
    MaskEntityProcessor,
    SyntheticReplacementProcessor,
    deidentify_text,
    post_redacted_text,
    reidentify_process_text,
)
from ..tests.test_files import test_response_body

EntityProcessor = Callable[[dict], str]


# helper functions
def assert_entity_spans_match(response: TextResponse):
    """
    Assert that each entity's processed location points to its processed text, which may be
    stored without the enclosing brackets of a marker.
    """
    for text, entities in zip(response.processed_text, response.entities):
        for entity in entities:
            location = entity["location"]
            span = text[location["stt_idx_processed"] : location["end_idx_processed"]]
            assert span in (entity["processed_text"], f"[{entity['processed_text']}]")


def make_fake_response(response_body: list[dict]) -> requests.Response:
    """
    Make a fake response that is made by the Requests library

    Arg:
        response_body: a json structured list representing a http response body from the DEID container.
    """
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(response_body).encode("utf-8")
    return response


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
    argnames=["entity", "bucket_size", "text_processed"],
    argvalues=[
        (
            test_response_body.age_repsonse_1[0]["entities"][0],
            5,
            "[30-34]",
        ),
        (
            test_response_body.age_repsonse_1[0]["entities"][0],
            2,
            "[32-33]",
        ),
        (
            test_response_body.age_repsonse_1[0]["entities"][0],
            3,
            "[30-32]",
        ),
        (
            test_response_body.age_repsonse_2[0]["entities"][0],
            3,
            "[%-%]",
        ),
    ],
)
def test_age_bucket_processor(
    entity: list[dict], bucket_size: int, text_processed: str
):
    """
    Testing the age bucketing post-processor.

    Args:
        entity: a list of entities found by the DEID container.
        bucket_size: the size of a bucket in years
        text_processed: the expected output text from the AgeEntityBucketProcessor() function
    """
    processor = AgeEntityBucketProcessor(bin_size=bucket_size)
    assert processor(entity) == text_processed


def test_deidentify_text_with_age_bucketing():
    """
    Test de-identifying text and age bucketing post-processors.
    """
    response = make_fake_response(test_response_body.age_repsonse_1)

    text_out = deidentify_text(
        text=["A 32-year old wants to travel."],
        response=AnalyzeTextResponse(response),
        entity_processors={"AGE": AgeEntityBucketProcessor(bin_size=5)},
        default_processor=MaskEntityProcessor(),
    )
    assert text_out == ["A [30-34]-year old wants to travel."]


# Date Shifting
@pytest.mark.parametrize(
    argnames=["entity", "date_offset", "operator", "text_processed"],
    argvalues=[
        (
            test_response_body.date_response_1[0]["entities"][0],
            relativedelta(days=1),
            "add",
            "[1990-01-02]",
        ),
        (
            test_response_body.date_response_1[0]["entities"][0],
            relativedelta(days=1),
            "subtract",
            "[1989-12-31]",
        ),
    ],
)
def test_date_shifting_processor(
    entity: list[dict], date_offset: relativedelta, operator: str, text_processed: str
):
    """
    Testing the date shifting post-processor.

    Args:
        entity: a list of entities found by the DEID container.
        date_offset: the amount of time to change the date by.
        operator: whether to 'add' or 'subtract' the date offset.
        text_processed: the expected output text from the DateShiftProcessor() function
    """
    processor = DateShiftProcessor(date_offset, operator)
    assert processor(entity) == text_processed


def test_date_shifting_processor_wrong_arg():
    """
    Test passing the date shifting post-processor an incorrect argument.
    """
    offset = relativedelta(months=3)
    # checking error handling
    error_msg = (
        "The operation minus does not exist. Unable to initialize DateShiftProcessor."
    )
    with pytest.raises(ValueError, match=error_msg):
        DateShiftProcessor(offset, "minus")


def test_deidentify_text_with_date_shifting():
    """
    Test de-identifying text and date shifting post-processors.
    """
    response = make_fake_response(test_response_body.date_response_1)

    text_out = deidentify_text(
        text=["today is 1990-01-01."],
        response=AnalyzeTextResponse(response),
        entity_processors={
            "DOB": DateShiftProcessor(date_offset=relativedelta(months=3)),
            "DATE": DateShiftProcessor(date_offset=relativedelta(months=3)),
        },
        default_processor=MaskEntityProcessor(),
    )
    assert text_out == ["today is [1990-04-01]."]


# Date Bucketing
@pytest.mark.parametrize(
    argnames=["entity", "date_bin", "text_processed"],
    argvalues=[
        (
            test_response_body.date_response_1[0]["entities"][0],
            "decade",
            "[1990-01-01 to 1999-12-31]",
        ),
        (
            test_response_body.date_response_1[0]["entities"][0],
            "year",
            "[1990-01-01 to 1990-12-31]",
        ),
        (
            test_response_body.date_response_1[0]["entities"][0],
            "month",
            "[1990-01-01 to 1990-01-31]",
        ),
    ],
)
def test_date_bucketing_processor(
    entity: list[dict], date_bin: str, text_processed: str
):
    """
    Testing the date bucketing post-processor.

    Args:
        entity: a list of entities found by the DEID container.
        date_bin: a time horizon to bucket dates into, such as month, year, decade.
        text_processed: the expected output text from the DateBucketProcessor() function
    """
    processor = DateBucketProcessor(date_bin)
    assert processor(entity) == text_processed


def test_date_bucketing_processor_wrong_arg():
    """
    Test passing the date bucketing post-processor an incorrect argument.
    """
    # checking error handling
    error_msg = "ate_bin value: millennia is not a valid value. Unable to initialize DateBucketProcessor."
    with pytest.raises(ValueError, match=error_msg):
        DateBucketProcessor("millennia")


def test_deidentify_text_with_date_bucketing():
    """
    Test de-identifying text and date bucketing post-processors.
    """
    response = make_fake_response(test_response_body.date_response_1)

    text_out = deidentify_text(
        text=["today is 1990-01-01."],
        response=AnalyzeTextResponse(response),
        entity_processors={
            "DOB": DateBucketProcessor(date_bin="year"),
            "DATE": DateBucketProcessor(date_bin="year"),
        },
        default_processor=MaskEntityProcessor(),
    )
    assert text_out == ["today is [1990-01-01 to 1990-12-31]."]


# Selective Date Component Redaction
@pytest.mark.parametrize(
    argnames=["entity", "redact_date_comps", "text_processed"],
    argvalues=[
        (
            test_response_body.date_response_1[0]["entities"][0],
            ["DAY"],
            "1990-01-01",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["DAY"],
            "1990-01-##",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["MONTH"],
            "1990-##-01",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["YEAR"],
            "####-01-01",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["DAY", "MONTH"],
            "1990-##-##",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["DAY", "YEAR"],
            "####-01-##",
        ),
        (
            test_response_body.date_response_2[0]["entities"][0],
            ["DAY", "MONTH", "YEAR"],
            "####-##-##",
        ),
    ],
)
def test_date_component_processor(
    entity: list[dict], redact_date_comps: list[str], text_processed: str
):
    """
    Testing the selective date redaction post-processor.

    Args:
        entity: a list of entities found by the DEID container.
        redact_date_comps: a list of date components to redact.
        text_processed: the expected output text from the DateComponentProcessor() function
    """
    processor = DateComponentProcessor(redact_date_comps)
    assert processor(entity) == text_processed


def test_deidentify_text_with_date_comp_redaction():
    """
    Test de-identifying text and selective date redation post-processors.
    """
    response = make_fake_response(test_response_body.date_response_2)

    text_out = deidentify_text(
        text=["today is 1990-01-01."],
        response=AnalyzeTextResponse(response),
        entity_processors={
            "DATE": DateComponentProcessor(redact_components=["DAY"]),
            "DOB": DateComponentProcessor(redact_components=["DAY"]),
        },
        default_processor=MaskEntityProcessor(),
    )
    assert text_out == ["today is 1990-01-##."]


# re-process redacted text from TextProcess
@pytest.mark.parametrize(
    argnames=["response_json", "entity_processors", "text_processed"],
    argvalues=[
        (
            [test_response_body.processed_text_response_3[9]],
            {"DOB": DateBucketProcessor(date_bin="year")},
            "Caller: My date of birth is [1988-01-01 to 1988-12-31]. And my medicaid card expires on [DATE_1]",
        ),
        (
            [test_response_body.processed_text_response_3[9]],
            {
                "DOB": DateBucketProcessor(date_bin="year"),
                "DATE": DateComponentProcessor(redact_components=["DAY"]),
            },
            "Caller: My date of birth is [1988-01-01 to 1988-12-31]. And my medicaid card expires on 2024-06-##",
        ),
        (
            [test_response_body.processed_text_response_3[21]],
            {"AGE": AgeEntityBucketProcessor(bin_size=5)},
            "Caller: I'm [35-39] and have no major medical concerns. I just have a [CONDITION_3].",
        ),
        (
            # SyntheticReplacementProcessor can't process TextResponses, so DATE is left as-is
            [test_response_body.processed_text_response_3[9]],
            {
                "DOB": DateBucketProcessor(date_bin="year"),
                "DATE": SyntheticReplacementProcessor(),
            },
            "Caller: My date of birth is [1988-01-01 to 1988-12-31]. And my medicaid card expires on [DATE_1]",
        ),
    ],
)
def test_post_redacted_text(
    response_json: list[dict],
    entity_processors: dict[str, EntityProcessor],
    text_processed: str,
):
    """
    Test post-processing of TextResponses.

    Args:
        response_json: a json structured list representing a http response body from the DEID container.
        entity_processors: a dictionary associating entity processors with entities.
        text_processed: the expected output text from the post_redacted_text() function
    """
    process_text_response = TextResponse(make_fake_response(response_json))
    response_before = copy.deepcopy(process_text_response)

    # start post-processing of the text response
    reprocessed_redaction = post_redacted_text(process_text_response, entity_processors)

    # test the transformations were done correctly
    assert text_processed == reprocessed_redaction[0]
    # also ensure that the response changed
    assert process_text_response.processed_text != response_before.processed_text
    assert process_text_response.entities != response_before.entities
    # ensure entity locations point to their (bracket-less) processed text
    assert_entity_spans_match(process_text_response)


# rehydrate PII
@pytest.mark.parametrize(
    argnames=["response", "text_processed"],
    argvalues=[
        (
            test_response_body.processed_text_response_1,
            test_response_body.process_text_1[0],
        ),
        (
            test_response_body.processed_text_response_2,
            test_response_body.process_text_1[0],
        ),
    ],
)
def test_rehydrate_PII(response: list[dict], text_processed: str):
    """
    Test for placing PII data back into a redacted text using the process/text endpoint response (TextResponse).

    Args:
        response: a json structured list representing a http response body from the DEID container.
        text_processed: the expected output text from the reidentify_process_text() function
    """
    process_text_response = make_fake_response(response)

    text_out = reidentify_process_text(response=TextResponse(process_text_response))
    assert text_out == [text_processed]


@pytest.mark.parametrize(
    argnames=["text", "response_json", "entity_processors", "default_processor"],
    argvalues=[
        (
            test_response_body.analyze_text_1,
            test_response_body.analyze_response_1,
            {"AGE": AgeEntityBucketProcessor(bin_size=5)},
            MaskEntityProcessor(),
        ),
        (
            test_response_body.analyze_text_1,
            test_response_body.analyze_response_1,
            {
                "AGE": AgeEntityBucketProcessor(bin_size=7),
                "DATE": DateBucketProcessor("month"),
                "DOB": DateComponentProcessor(redact_components=["DAY"]),
            },
            MarkerEntityProcessor(),
        ),
    ],
)
def test_analyze_deidentify_rehydrate_PII(
    text: list[str],
    response_json: list[dict],
    entity_processors: dict[str, EntityProcessor],
    default_processor: EntityProcessor,
):
    """
    Test redacting text using the analyze/text endpoint response (AnalyzeResponse) and rehydrating
    the redacted processed text in the converted AnalyzeResponse back into the original text.

    Args:
        text: the original text that needs to be redacted.
        response_json: a json response returned by the analyze/text endpoint.
        entity_processors: a dictionary associating entity processors with entities.
        default_processor: the processor to use if an entity doesn't have an explicit entity processor associated
            with it.
    """
    response = AnalyzeTextResponse(make_fake_response(response_json))

    redacted_text_out = deidentify_text(
        text=text,
        response=response,
        entity_processors=entity_processors,
        default_processor=default_processor,
        convert_response=True,
    )

    assert_entity_spans_match(response.to_text_response())
    rehydrated_text_out = reidentify_process_text(response)

    assert text == rehydrated_text_out
    assert isinstance(redacted_text_out, list) and all(
        isinstance(text_blk, str) for text_blk in redacted_text_out
    )
