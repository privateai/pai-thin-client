from typing import Callable

from dateutil.relativedelta import relativedelta

from privateai_client.components import AnalyzeTextResponse, TextResponse

EntityProcessor = Callable[[dict], str]


def deidentify_text(
    text: list[str],
    response: AnalyzeTextResponse,
    entity_processors: dict[str, EntityProcessor],
    default_processor: EntityProcessor,
) -> list[str]:
    """
    Deidentifies analyzed text by processing entities with multiple processors, adjusting text dynamically.

    Args:
        text: The original list of text messages used as input in the `PAIClient.analyze_text()` call.
        response: The response object returned by `PAIClient.analyze_text()`, containing detected entities.
        entity_processors: A dictionary mapping entity types to processing functions in the format
            `{ENTITY_TYPE: entity_processor_fn}`, where `entity_processor_fn` takes an entity dictionary
            and returns modified text for all occurrences of that entity type.
        default_processor: A fallback function used to process entities not found in `entity_processors`.


    Returns:
        A list of de-identified text messages, with the same length and order as the `text` argument.

    """
    modified_texts = []
    for t, entities in zip(text, response.entities):
        offset = 0
        modified_text = t
        for entity in sorted(entities, key=lambda e: e["location"]["stt_idx"]):
            start_idx = entity["location"]["stt_idx"] + offset
            end_idx = entity["location"]["end_idx"] + offset

            processor = entity_processors.get(entity["best_label"], default_processor)
            modified_entity_text = processor(entity)

            length_diff = len(modified_entity_text) - len(entity["text"])
            offset += length_diff

            modified_text = (
                modified_text[:start_idx]
                + modified_entity_text
                + modified_text[end_idx:]
            )
        modified_texts.append(modified_text)
    return modified_texts


def age_bucket(response: TextResponse, bin_size: int) -> list[str]:
    """
    Bin age entities found by the process/text endpoint response into consistently sized buckets.

    Args:
        response: The response object returned by `PAIClient.process_text()`, containing detected entities.
        bin_size: the size of each bin (measured in years) used to bucket ages. Buckets start at age zero and
            progress in multiple of the bin_size.

    Returns:
        A list of de-identified text messages, where ages have been bucketed.

    Examples:
        >>> response = {
                "entities":[
                    "processed_text": "[AGE_1]",
                    "text": "32",
                    "best_label":  "AGE".
                    "location": {
                        stt_idx: 2,
                        end_idx: 4,
                        stt_idx_processed: 2,
                        end_idx_processed: 9
                        }
                    ],
                "entities_present": True,
                "characters_processed": 30,
                "languages_detected": {"en": 0.99},
                "processed_text": "A [AGE_1]-year old wants to travel."
                }
        >>> age_bucket(response, 5)
        ["A 30-year old wants to travel."]
    """
    acceptable_entities = ["AGE"]
    pass


def date_shift(
    response: TextResponse,
    date_offset: relativedelta,
    date_format: str = "%Y-%m-%d",
    entity_fields: list[str] = ["DATE"],
) -> list[str]:
    """
    Scales dates returned the repsonse of the process/text endpoint by a defined offset.

    Args:
        response: The response object returned by `PAIClient.process_text()`, containing detected entities.
        date_offset: a date offset to apply to all dates.
        date_format: a python date code used to format the outputted dates.
        entity_fields: a list of entities to apply the date_shift transformation to.

    Returns:
        A list of de-identified text messages, with dates scaled by a defined offset.

    Examples:
        >>> response = {
                "entities":[
                    "processed_text": "[DATE_1]",
                    "text": "Jan 1, 1990",
                    "best_label":  "DATE".
                    "location": {
                        stt_idx: 9,
                        end_idx: 20,
                        stt_idx_processed: 9,
                        end_idx_processed: 17
                        }
                    ],
                "entities_present": True,
                "characters_processed": 20,
                "languages_detected": {"en": 0.99},
                "processed_text": "Today is [DATE_1]. "
                }
        >>> offset = relativedelta(months=3)
        >>> date_shift(response, offset)
        ["today is 1990-04-01".]
    """
    acceptable_entities = ["DATE", "DATE_OF_DEATH"]
    pass


def date_bucket(
    response: TextResponse, date_bins: str, entity_fields: list[str] = ["DATE"]
) -> list[str]:
    """
    Bin date entities found by the process/text endpoint response into defined buckets.

    Args:
        response: The response object returned by `PAIClient.process_text()`, containing detected entities.
        date_bins: date compnents used to bin detected date entities. Acceptable values include "decade",
            "year", and "month".
        entity_fields: a list of entities to apply the date_bucket transformation to.

    Returns:
        A list of de-identified text messages, dates binned by date components.

    Examples:
        >>> response = {
                "entities":[
                    "processed_text": "[DATE_1]",
                    "text": "Jan 1, 1990",
                    "best_label":  "DATE".
                    "location": {
                        stt_idx: 9,
                        end_idx: 20,
                        stt_idx_processed: 9,
                        end_idx_processed: 17
                        }
                    ],
                "entities_present": True,
                "characters_processed": 20,
                "languages_detected": {"en": 0.99},
                "processed_text": "Today is [DATE_1]. "
                }
        >>> date_bucket(response, "year")
        ["today is between 1990-01-01 and 1990-12-31."]
        >>> date_bucket(response, "month")
        ["today is between 1990-01-01 and 1990-01-31."]
        >>> date_bucket(response, "decade")
        ["today is between 1990-01-01 and 1999-12-31."]
    """
    acceptable_entities = ["DATE", "DATE_OF_DEATH"]
    pass


def replace_names(response: TextResponse) -> list[str]:
    """ """
    acceptable_entities = [
        "NAME",
        "NAME_GIVEN",
        "NAME_FAMILY",
        "NAME_MEDICAL_PROFESSIONAL",
    ]
    pass
