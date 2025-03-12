from typing import Callable

from privateai_client.components import AnalyzeTextResponse

EntityProcessor = Callable[[dict], str]


def deidentify_text(
    input_texts: list[str],
    response: AnalyzeTextResponse,
    entity_processors: dict[str, EntityProcessor],
    default_processor: EntityProcessor,
) -> list[str]:
    """
    Deidentifies analyzed text by processing entities with multiple processors, adjusting text dynamically.

    Args:
        input_texts: The original list of texts used as input in the `PAIClient.analyze_text()` call.
        response: The response object returned by `PAIClient.analyze_text()`, containing detected entities.
        entity_processors: A dictionary mapping entity types to processing functions in the format
            `{ENTITY_TYPE: entity_processor_fn}`, where `entity_processor_fn` takes an entity dictionary
            and returns modified text for all occurrences of that entity type.
        default_processor: A fallback function used to process entities not found in `entity_processors`.


    Returns:
        A list of de-identified texts, with the same length and order as `input_texts`.

    """
    modified_texts = []
    for text, entities in zip(input_texts, response.entities):
        offset = 0
        modified_text = text
        for entity in sorted(entities, key=lambda e: e["location"]["stt_idx"]):
            start_idx = entity["location"]["stt_idx"] + offset
            end_idx = entity["location"]["end_idx"] + offset

            initial_entity_length = entity["text"]

            processor = entity_processors.get(entity["best_label"], default_processor)
            entity["text"] = processor(entity)
            length_diff = len(entity["text"]) - len(initial_entity_length)
            offset += length_diff

            modified_text = (
                modified_text[:start_idx] + entity["text"] + modified_text[end_idx:]
            )
        modified_texts.append(modified_text)
    return modified_texts
